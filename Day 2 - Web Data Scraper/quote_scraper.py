import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = "https://quotes.toscrape.com"
all_quotes = []

for page in range(1, 11):  # 10 pages
    url = f"{base_url}/page/{page}/"
    print(f"📄 Scraping: {url}")
    res = requests.get(url)

    if res.status_code != 200:
        print("❌ Failed to load page")
        break

    soup = BeautifulSoup(res.text, "lxml")
    quotes = soup.find_all("div", class_="quote")

    for q in quotes:
        text = q.find("span", class_="text").text.strip()
        author = q.find("small", class_="author").text.strip()
        tags = [tag.text for tag in q.find_all("a", class_="tag")]
        all_quotes.append({
            "quote": text,
            "author": author,
            "tags": ", ".join(tags)
        })

# Save to CSV
df = pd.DataFrame(all_quotes)
df.to_csv("quotes.csv", index=False)
print(f"\n✅ Done! Scraped {len(df)} quotes into quotes.csv")
