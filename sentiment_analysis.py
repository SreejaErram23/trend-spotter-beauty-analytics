"""
Trend-Spotter: Sentiment Analysis Script
------------------------------------------
What this script does, step by step:
1. Connects to SQLite database (trend_spotter.db)
2. Pulls the Reviews table into a pandas DataFrame 
3. Uses TextBlob to analyze the sentiment of each review's text
4. Adds new columns for sentiment score and sentiment label (positive/negative/neutral)
5. Saves the results into a NEW table in the same database, so Power BI can use it later
"""

# --- STEP 0: IMPORTS ---
# TextBlob is the sentiment analysis tool.
import sqlite3
import pandas as pd
from textblob import TextBlob


# --- STEP 1: CONNECT TO THE DATABASE ---
# Ensure .db file is in the SAME FOLDER as this script,
DB_PATH = "trend_spotter.db"
conn = sqlite3.connect(DB_PATH)

print("Connected to database successfully.")


# --- STEP 2: PULL THE REVIEWS TABLE INTO PANDAS ---
reviews_df = pd.read_sql_query("SELECT * FROM Reviews", conn)

print(f"Pulled {len(reviews_df)} reviews into a DataFrame.")
print(reviews_df.head())  

# --- STEP 3: DEFINE A FUNCTION TO ANALYZE SENTIMENT ---
def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity  # a number between -1 and 1

    if polarity > 0.1:
        label = "positive"
    elif polarity < -0.1:
        label = "negative"
    else:
        label = "neutral"

    return polarity, label


# --- STEP 4: APPLY THE FUNCTION TO EVERY REVIEW ---
reviews_df["sentiment_score"], reviews_df["sentiment_label"] = zip(
    *reviews_df["review_text"].apply(analyze_sentiment)
)

print("\nSentiment analysis complete. Sample results:")
print(reviews_df[["review_text", "sentiment_score", "sentiment_label"]].head(10))


# --- STEP 4.5: CALCULATE AVERAGE SENTIMENT PER PRODUCT ---
product_summary_df = reviews_df.groupby("product_id").agg(
    avg_sentiment_score=("sentiment_score", "mean"),
    review_count=("sentiment_score", "count"),
    avg_star_rating=("star_rating", "mean")
).reset_index()

# Round the averages to 2 decimal places, just for readability
product_summary_df["avg_sentiment_score"] = product_summary_df["avg_sentiment_score"].round(2)
product_summary_df["avg_star_rating"] = product_summary_df["avg_star_rating"].round(2)

print("\nProduct-level sentiment summary:")
print(product_summary_df)


# --- STEP 5: SAVE THE ENRICHED DATA BACK TO THE DATABASE ---
reviews_df.to_sql("Reviews_Analyzed", conn, if_exists="replace", index=False)

print("\nSaved results to a new table: Reviews_Analyzed")

# Save the product-level summary as its own table
product_summary_df.to_sql("Product_Sentiment_Summary", conn, if_exists="replace", index=False)
print("Saved results to a new table: Product_Sentiment_Summary")

# --- STEP 6: CLOSE THE CONNECTION ---
conn.close()

print("Done! Check trend_spotter.db for the new Reviews_Analyzed table.")
