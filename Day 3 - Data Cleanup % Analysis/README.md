# 📊 Day 3 - Data Cleanup & Analysis

## 🧠 Problem Statement

Real-world datasets are often noisy and unstructured. Cleaning and analyzing such data is a crucial step before any modeling or decision-making. The goal of this challenge was to take raw datasets and:
- Clean them (handle missing data, duplicates, invalid formats)
- Extract patterns using visualizations
- Derive insights that could guide business or product decisions

---

## 📂 Datasets Used

### 1. **Ecommerce Orders Dataset**
- Contains transactional data including:
  - `order_id`, `customer_name`, `category`, `item_price`, `quantity`, `order_date`, `region`
- Purpose: Understand purchase trends, quantities sold, and customer regions.

### 2. **Social Media Engagement Dataset**
- Contains post-level social media data:
  - `Post_ID`, `Platform`, `Content_Type`, `Views`, `Likes`, `Shares`, `Comments`, `Engagement_Level`
- Purpose: Analyze content performance across platforms and find what drives engagement.

---

## 🔍 Cleaning Steps
- Checked for and confirmed **no null values** ✅
- Verified absence of **duplicate rows** ✅
- Ensured correct datatypes and logical integrity

---

## 📈 Visualizations Done

### ✅ Ecommerce
- Top 5 categories by quantity sold
- Total revenue by region
- Monthly trend of orders placed

### ✅ Social Media
- Posts per platform
- Average engagement level by platform
- Popular content types
- Correlation heatmap for views, likes, shares, comments

All visualizations are available in the respective Jupyter Notebook.

---

## 📌 Key Learnings
- Hands-on with `pandas`, `matplotlib`, `seaborn` for EDA
- Reinforced the habit of always checking for nulls & duplicates before anything else
- Understood how visual patterns help uncover insights quickly
- Practice in keeping code modular, readable, and GitHub-publishable
