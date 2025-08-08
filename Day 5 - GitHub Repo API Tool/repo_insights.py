import os
import time
import requests
import pandas as pd
from dotenv import load_dotenv

# ---------- Config ----------
load_dotenv()
TOKEN = os.getenv("GITHUB_TOKEN")
OWNER = "Vyshnavkumarp"          # <- change if you want
REPO  = "Shipment_Chatbot"   # <- change if you want
BASE  = "https://api.github.com"

HEADERS = {
    "Accept": "application/vnd.github.v3+json",
    "Authorization": f"Bearer {TOKEN}" if TOKEN else None
}

def get_json(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params, timeout=30)
    if r.status_code != 200:
        raise RuntimeError(f"GitHub API error {r.status_code}: {r.text[:200]}")
    return r.json()

def paginate(url, params=None, max_pages=10):
    """Yield items across pages (per_page=100)"""
    page = 1
    params = dict(params or {})
    params["per_page"] = 100
    while page <= max_pages:
        params["page"] = page
        data = get_json(url, params=params)
        if not data:
            break
        for item in data:
            yield item
        page += 1
        time.sleep(0.3)  # gentle on rate limit

# ---------- 1) Repo summary ----------
repo_url = f"{BASE}/repos/{OWNER}/{REPO}"
repo = get_json(repo_url)

summary = {
    "repo": f"{OWNER}/{REPO}",
    "description": repo.get("description"),
    "visibility": repo.get("visibility"),
    "stars": repo.get("stargazers_count"),
    "forks": repo.get("forks_count"),
    "watchers": repo.get("subscribers_count"),
    "open_issues": repo.get("open_issues_count"),
    "default_branch": repo.get("default_branch"),
    "pushed_at": repo.get("pushed_at"),
    "created_at": repo.get("created_at"),
    "language": repo.get("language"),
}

print("✅ Repo summary fetched.")

# ---------- 2) Latest commits (with pagination) ----------
commits_url = f"{BASE}/repos/{OWNER}/{REPO}/commits"
commits = []
for c in paginate(commits_url, max_pages=3):  # first ~300 commits max
    commit = c.get("commit", {})
    author = commit.get("author") or {}
    commits.append({
        "sha": c.get("sha"),
        "author_name": author.get("name"),
        "author_email": author.get("email"),
        "date": author.get("date"),
        "message": (commit.get("message") or "").split("\n")[0],
        "html_url": c.get("html_url"),
    })

print(f"✅ Collected {len(commits)} commits (paginated).")

# ---------- 3) Open issues (only issues, exclude PRs) ----------
issues_url = f"{BASE}/repos/{OWNER}/{REPO}/issues"
issues = []
for i in paginate(issues_url, params={"state": "open"}, max_pages=2):
    if "pull_request" in i:
        continue  # skip PRs; we only want issues
    issues.append({
        "number": i.get("number"),
        "title": i.get("title"),
        "created_at": i.get("created_at"),
        "user": i.get("user", {}).get("login"),
        "labels": ",".join([lbl["name"] for lbl in i.get("labels", [])]),
        "html_url": i.get("html_url"),
    })

print(f"✅ Open issues (excluding PRs): {len(issues)}")

# ---------- 4) Save a compact CSV ----------
# One row summary + latest 5 commits + issue count
top5 = commits[:5]
records = []

records.append({
    "section": "summary",
    **summary
})

for c in top5:
    records.append({
        "section": "commit",
        "repo": f"{OWNER}/{REPO}",
        "description": None,
        "visibility": None,
        "stars": None,
        "forks": None,
        "watchers": None,
        "open_issues": None,
        "default_branch": None,
        "pushed_at": c["date"],
        "created_at": None,
        "language": None,
        "sha": c["sha"],
        "author_name": c["author_name"],
        "message": c["message"],
        "url": c["html_url"],
    })

records.append({
    "section": "issues",
    "repo": f"{OWNER}/{REPO}",
    "open_issues_listed": len(issues)
})

df = pd.DataFrame(records)
df.to_csv("insights_v2.csv", index=False)
print("📄 Saved insights_v2.csv")

# ---------- 5) Friendly console output ----------
print("\n--- Repo Summary ---")
for k, v in summary.items():
    print(f"{k:>15}: {v}")

print("\n--- Latest 5 commits ---")
for c in top5:
    print(f"{c['date']} | {c['author_name']}: {c['message']}")


#Matplotlib Visualization

# ---------- 6) Plot commits per day (last 30 days) ----------
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Convert commit ISO dates to datetime.date
dates = []
for c in commits:
    try:
        dt = datetime.fromisoformat(c["date"].replace("Z", "+00:00"))
        dates.append(dt.date())
    except Exception:
        pass

if dates:
    cutoff = datetime.utcnow().date() - timedelta(days=30)
    last30 = [d for d in dates if d >= cutoff]

    # Count per day
    from collections import Counter
    counts = Counter(last30)

    # Build ordered series for the last 30 days (zero-fill missing)
    day_list = [cutoff + timedelta(days=i) for i in range(31)]
    y = [counts.get(day, 0) for day in day_list]

    plt.figure(figsize=(10, 4))
    plt.plot(day_list, y, marker="o")
    plt.title(f"Commits per day (last 30 days) — {OWNER}/{REPO}")
    plt.xlabel("Date")
    plt.ylabel("Commits")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("commits_last_30_days.png", dpi=150)
    print("📈 Saved commits_last_30_days.png")
else:
    print("No commit dates found to plot.")
