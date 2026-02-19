**📊 Amazon JSON Sentiment Analysis using SQLite**

**🚀 Project Overview**

This project performs rule-based sentiment analysis on Amazon review data stored in a JSON file.
Each review is analyzed, assigned a sentiment score, classified as Positive/Negative/Neutral, and stored in a SQLite database with a timestamp.

The goal of this project is to demonstrate:

Text processing

Rule-based sentiment scoring

JSON file handling

SQLite database integration

Exception handling in Python

**📂 Dataset**

Format: JSON (Line-by-line JSON records)

Source: Amazon Reviews Dataset

Total Records Processed: 20,000+

Each JSON record contains:

reviewerID

asin (product ID)

reviewText

rating

reviewTime

**🧠 Sentiment Logic (Rule-Based)**

The scoring system is based on keyword matching.

Positive Keywords:

good

excellent

amazing

happy

great

Negative Keywords:

bad

worst

poor

disappointing

terrible

Sentiment Classification:

**Score       	Sentiment**
> 0          	Positive
< 0          	Negative
= 0          	Neutral

 
**🛠 Technologies Used**

Python 3.12

SQLite3

JSON module

Datetime module

Exception Handling
