# Day 2 – Web Data Scraper 🌐

### 🧩 Problem Statement:
Explore practical web scraping techniques by extracting structured data from real websites.

---

### 🛠️ What I Tried:
- Built a working scraper using `requests + BeautifulSoup` for [quotes.toscrape.com](https://quotes.toscrape.com)
- Attempted scraping IMDB reviews using `Playwright` (but faced dynamic content blocks)
- Debugged common scraping challenges: timeout, missing selectors, headless rendering issues

---

### ✅ What Worked:
- Successfully scraped 100+ quotes including text, author, and tags
- Structured and stored the data as a CSV using `pandas`

---

### 📚 What I Learned:
- The HTML parsing and scraping pipeline
- Handling pagination with both requests and browser automation
- Why some websites require dynamic scrapers like Selenium or Playwright
- What real scraping failures look like — and how to troubleshoot them

---

### 🚀 Tools Used:
- `requests`, `beautifulsoup4`, `pandas`
- `playwright` (attempted dynamic scraping)
