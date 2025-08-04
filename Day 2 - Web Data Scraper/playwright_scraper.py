from playwright.sync_api import sync_playwright
import pandas as pd
import time

movie_url = "https://www.imdb.com/title/tt10676052/reviews"
all_reviews = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(movie_url)

    print(f"📄 Scraping IMDB reviews from: {movie_url}")
    
    for i in range(5):  # scrape 5 loads
        print(f"🔁 Scraping batch {i+1}...")
        time.sleep(2)

        review_blocks = page.locator(".lister-item-content")
        count = review_blocks.count()

        for j in range(count):
            try:
                block = review_blocks.nth(j)
                title = block.locator("a.title").inner_text()
                text = block.locator("div.text.show-more__control").inner_text()
                all_reviews.append({
                    "title": title.strip(),
                    "review": text.strip()
                })
            except Exception:
                continue

        # Try to click "Load More"
        try:
            load_more = page.locator("button.ipl-load-more__button")
            if load_more.is_visible():
                load_more.click()
                time.sleep(2)
            else:
                print("🚫 No more reviews to load.")
                break
        except:
            print("⚠️ Load More not found or failed.")
            break

    browser.close()

# Save to CSV
df = pd.DataFrame(all_reviews)
df.to_csv("imdb_reviews_playwright.csv", index=False)
print(f"✅ Scraped {len(df)} reviews into imdb_reviews_playwright.csv")
