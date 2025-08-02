import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

# Starting URL
base_url = "https://www.imdb.com/title/tt10676052/reviews"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
}

all_reviews = []

def get_reviews(soup):
    blocks = soup.find_all("div", class_="lister-item-content")
    for b in blocks:
        title = b.find("a", class_="title").text.strip() if b.find("a", class_="title") else ""
        body = b.find("div", class_="text").text.strip() if b.find("div", class_="text") else ""
        all_reviews.append({"title": title, "review": body})

# Initial request
url = base_url
while url:
    print(f"📄 Scraping: {url}")
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "lxml")
    
    get_reviews(soup)

    # Look for the “Load More” button’s data-key
    load_more = soup.find("button", class_="ipl-load-more__button")
    if load_more and load_more.has_attr("data-key"):
        data_key = load_more["data-key"]
        url = f"{base_url}/_ajax?paginationKey={data_key}"
    else:
        url = None  # No more pages

    time.sleep(random.uniform(1.5, 2.5))  # Polite delay

# Save to CSV
df = pd.DataFrame(all_reviews)
df.to_csv("imdb_reviews.csv", index=False)
print(f"✅ Done! Scraped {len(df)} reviews to imdb_reviews.csv")
