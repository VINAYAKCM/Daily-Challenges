## 📌 Problem Statement
A messy JSON file containing customer feedback collected from a beta e-commerce app needs to be cleaned, analyzed, and summarized. The feedback includes multiple languages, emojis, inconsistent formatting, and missing fields.

## 🎯 Goals
- Clean real-world, messy user feedback
- Perform sentiment analysis on short, casual text
- Extract actionable insights from feedback

## 🛠️ Tech Stack & Tools
- **pandas** – data loading, cleaning, transformation
- **re (regex)** – remove emojis, tags, and symbols
- **VADER** (from NLTK) – sentiment analysis
- **TextBlob** – initially tested, but VADER chosen for final result
- **langdetect** – (optional) for future multilingual detection
- **collections.Counter** – keyword frequency extraction

## 🔍 What I Did
- Loaded and explored JSON dataset
- Cleaned feedback text using regex (emojis, HTML, casing, spacing)
- Ran sentiment scoring using VADER
- Classified into Positive / Negative / Neutral
- Extracted top praise and complaint keywords

## ✅ Outcome
- Cleaned + sentiment-tagged feedback
- Found that:
  - 50 entries were Negative
  - 39 entries were Positive
  - 11 entries were Neutral
- Top Complaints: `damaged`, `late`, `worst`, etc.
- Top Praise: `great`, `quality`, `fast`, `loved`

## 💡 Learnings
- Cleaning real-world data is a critical skill
- VADER handles casual/social feedback better than basic models
- Preprocessing pipelines are essential for any AI/NLP task
