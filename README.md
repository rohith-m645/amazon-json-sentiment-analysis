**📊 Amazon Review Sentiment Analysis System**

**🚀 Project Overview**

This project implements an Advanced Rule-Based Sentiment Analysis System for Amazon product reviews.

The system:

Reads review data from a JSON dataset

Applies linguistic rules to calculate sentiment score

Classifies reviews as Positive, Negative, or Neutral

Uses multiprocessing for fast large-scale processing

Stores results in a SQLite database

Performs pattern analysis and reporting

Total dataset processed: 194,000+ reviews

**🧠 Features**
🔹 Text Processing

Lowercase normalization

Stop-word filtering

Word frequency analysis

🔹 Rule-Based Sentiment Engine

Weighted positive & negative keywords

Negation handling (e.g., "not good")

Emphasis detection (e.g., "very good")

Long-review boost rule

Threshold-based classification

🔹 Performance Optimization

Multiprocessing using all CPU cores

Bulk database insertion

Execution time measurement

🔹 Pattern Analysis

Sentiment distribution (count + percentage)

Average sentiment score

Rating vs sentiment mismatch detection

Top 10 meaningful word extraction

🛠 Technologies Used

Python 3.12

SQLite3

Multiprocessing

JSON Processing

Collections (Counter)

Standard Library Modules

No external dependencies required.

📂 Project Structure
amazon_review/
│
├── amazon_review.py
├── README.md
├── requirements.txt
└── .gitignore
⚙ How to Run

1️⃣ Place reviews.json in the project folder
2️⃣ Open terminal inside project directory
3️⃣ Run:

py amazon_review.py

**📊 Sample Output**
Total Reviews Loaded: 194439
Using CPU Cores: 16
Parallel Processing Completed.
Data inserted successfully.
Total Inserted: 194439

===== PATTERN ANALYSIS =====

Sentiment Distribution:
Positive : 107027 (55.03%)
Neutral  : 84285 (43.34%)
Negative : 3127 (1.61%)

Average Score: 2.15
Execution Time: 4.59 seconds
🗄 Database Schema

Table: results

Column	Type
id	INTEGER
reviewerID	TEXT
asin	TEXT
rating	REAL
review	TEXT
score	INTEGER
sentiment	TEXT
timestamp	TEXT

**📈 Key Insights**

Majority of reviews are Positive (~55%)

Negative reviews are minimal (~1–2%)

Dataset mainly discusses phone-related products

High efficiency: 194K reviews processed in under 5 seconds

**🎓 Learning Outcomes
**
Implemented rule-based NLP system

Applied multiprocessing for scalability

Designed SQLite data pipeline

Performed real-world pattern mining

Built performance-optimized sentiment engine
