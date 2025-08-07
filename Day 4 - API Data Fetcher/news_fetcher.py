import requests
import pandas as pd
from dotenv import load_dotenv
import os

# Load .env variables
load_dotenv()
API_KEY = os.getenv("API_KEY")

# API request details
url = "https://newsapi.org/v2/everything"
params = {
    "q": "Artificial Intelligence",
    "language": "en",
    "sortBy": "publishedAt",
    "pageSize": 100,
    "apiKey": API_KEY
}

# Fetch the data
response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    articles = data["articles"]

    # Parse useful fields
    records = []
    for article in articles:
        records.append({
            "title": article["title"],
            "source": article["source"]["name"],
            "author": article["author"],
            "publishedAt": article["publishedAt"],
            "url": article["url"],
            "description": article["description"]
        })

    # Save to CSV
    df = pd.DataFrame(records)
    df.to_csv("ai_news.csv", index=False)
    print("✅ Saved to ai_news.csv")
else:
    print(f"❌ Failed with status: {response.status_code}")
