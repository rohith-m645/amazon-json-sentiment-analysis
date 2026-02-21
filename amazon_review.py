import sqlite3
import json
import time
from datetime import datetime
from multiprocessing import Pool, cpu_count
from collections import Counter

# ==========================================
# KEYWORDS (Weighted)
# ==========================================

positive_words = {
    "good": 1,
    "great": 2,
    "excellent": 3,
    "amazing": 3,
    "happy": 1,
    "love": 2,
    "perfect": 3,
    "awesome": 3
}

negative_words = {
    "bad": -1,
    "poor": -2,
    "worst": -3,
    "terrible": -3,
    "hate": -2,
    "disappointed": -2,
    "useless": -3
}

# Stop words for better pattern detection
stop_words = {
    "the", "is", "a", "and", "to", "of", "for",
    "it", "this", "i", "in", "that", "was",
    "on", "with", "as", "but"
}

# ==========================================
# SCORE FUNCTION
# ==========================================

def calculate_score(text):
    score = 0
    text = text.lower()

    # Negation handling
    if "not good" in text:
        score -= 2
    if "not bad" in text:
        score += 1

    # Emphasis handling
    if "very good" in text:
        score += 2
    if "very bad" in text:
        score -= 2

    # Weighted scoring
    for word, value in positive_words.items():
        if word in text:
            score += value

    for word, value in negative_words.items():
        if word in text:
            score += value

    # Long review boost
    if len(text.split()) > 50:
        score += 1

    return score


def classify(score):
    if score > 1:
        return "Positive"
    elif score < -1:
        return "Negative"
    else:
        return "Neutral"


# ==========================================
# PROCESS REVIEW (Multiprocessing Worker)
# ==========================================

def process_review(line):
    try:
        data = json.loads(line)

        review_text = data.get("reviewText", "")
        reviewer_id = data.get("reviewerID", "")
        asin = data.get("asin", "")

        score = calculate_score(review_text)
        sentiment = classify(score)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return (reviewer_id, asin, review_text, score, sentiment, timestamp)

    except:
        return None


# ==========================================
# MAIN FUNCTION
# ==========================================

def main():

    start_time = time.time()

    # Load JSON
    try:
        with open("reviews.json", "r", encoding="utf-8") as file:
            lines = file.readlines()

        print("Total Reviews Loaded:", len(lines))

    except FileNotFoundError:
        print("Error: reviews.json not found.")
        return

    # Multiprocessing
    print("Using CPU Cores:", cpu_count())

    with Pool(cpu_count()) as pool:
        results = pool.map(process_review, lines)

    results = [r for r in results if r is not None]

    print("Parallel Processing Completed.")

    # Database
    try:
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

        # CLEAR OLD DATA (Important Fix)
        cursor.execute("DELETE FROM results")
        conn.commit()

        cursor.executemany("""
        INSERT INTO results
        (reviewerID, asin, review, score, sentiment, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
        """, results)

        conn.commit()

        print("Data inserted successfully.")
        print("Total Inserted:", len(results))

    except sqlite3.Error as e:
        print("Database error:", e)
        return

    # ======================================
    # PATTERN ANALYSIS
    # ======================================

    print("\n===== PATTERN ANALYSIS =====")

    cursor.execute("SELECT COUNT(*) FROM results")
    total = cursor.fetchone()[0]
    print("Total Reviews in DB:", total)

    cursor.execute("""
        SELECT sentiment, COUNT(*)
        FROM results
        GROUP BY sentiment
    """)

    print("\nSentiment Distribution:")
    for row in cursor.fetchall():
        print(row[0], ":", row[1])

    cursor.execute("SELECT AVG(score) FROM results")
    avg_score = cursor.fetchone()[0]
    print("\nAverage Score:", round(avg_score, 2))

    # Word frequency without stop words
    cursor.execute("SELECT review FROM results")
    word_counter = Counter()

    for row in cursor.fetchall():
        words = row[0].lower().split()
        filtered_words = [w for w in words if w not in stop_words]
        word_counter.update(filtered_words)

    print("\nTop 10 Meaningful Words:")
    for word, count in word_counter.most_common(10):
        print(word, ":", count)

    conn.close()

    end_time = time.time()
    print("\nExecution Time:", round(end_time - start_time, 2), "seconds")
    print("\nProcess Completed Successfully.")


# Entry Point
if __name__ == "__main__":
    main()