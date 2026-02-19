import sqlite3
import json
from datetime import datetime

# =============================
# KEYWORDS
# =============================

positive_words = ["good", "excellent", "amazing", "great", "happy", "love"]
negative_words = ["bad", "worst", "poor", "terrible", "irritating", "hate"]

# =============================
# SCORE FUNCTION
# =============================

def calculate_score(text):
    score = 0
    text = text.lower()

    for word in positive_words:
        if word in text:
            score += 1

    for word in negative_words:
        if word in text:
            score -= 1

    return score

def classify(score):
    if score > 0:
        return "Positive"
    elif score < 0:
        return "Negative"
    else:
        return "Neutral"

# =============================
# DATABASE SETUP
# =============================

conn = sqlite3.connect("amazon_json_sentiment.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reviewerID TEXT,
    asin TEXT,
    review TEXT,
    score INTEGER,
    sentiment TEXT,
    timestamp TEXT
)
""")

print("Database ready.")

# =============================
# READ JSON FILE (LINE BY LINE)
# =============================

try:
    with open("reviews.json", "r", encoding="utf-8") as file:

        for line in file:
            data = json.loads(line)

            review_text = data["reviewText"]
            reviewer_id = data["reviewerID"]
            asin = data["asin"]

            score = calculate_score(review_text)
            sentiment = classify(score)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute("""
            INSERT INTO results (reviewerID, asin, review, score, sentiment, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (reviewer_id, asin, review_text, score, sentiment, timestamp))

    conn.commit()
    print("All 20K reviews processed successfully.")

except FileNotFoundError:
    print("JSON file not found.")

except sqlite3.Error as e:
    print("Database error:", e)

except Exception as e:
    print("Unexpected error:", e)

finally:
    conn.close()
    print("Database closed.")
