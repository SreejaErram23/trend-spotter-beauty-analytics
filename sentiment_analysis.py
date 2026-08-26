"""
Trend-Spotter: Sentiment Analysis Script
------------------------------------------
What this script does, step by step:
1. Connects to our SQLite database (trend_spotter.db)
2. Pulls the Reviews table into a pandas DataFrame (a table Python can work with)
3. Uses TextBlob to analyze the sentiment of each review's text
4. Adds new columns for sentiment score and sentiment label (positive/negative/neutral)
5. Saves the results into a NEW table in the same database, so Power BI can use it later
"""

# --- STEP 0: IMPORTS ---
# These lines bring in the outside libraries we installed earlier.
# sqlite3 lets Python talk to a SQLite database file.
# pandas lets Python work with data in table form (like a spreadsheet).
# TextBlob is our sentiment analysis tool.
import sqlite3
import pandas as pd
from textblob import TextBlob


# --- STEP 1: CONNECT TO THE DATABASE ---
# This opens a connection to your trend_spotter.db file.
# Make sure this .db file is in the SAME FOLDER as this script,
# or change the path below to point to wherever it actually is.
DB_PATH = "trend_spotter.db"
conn = sqlite3.connect(DB_PATH)

print("Connected to database successfully.")


# --- STEP 2: PULL THE REVIEWS TABLE INTO PANDAS ---
# pd.read_sql_query() runs a SQL query and puts the result directly into
# a pandas DataFrame (think of it as a spreadsheet living inside Python).
reviews_df = pd.read_sql_query("SELECT * FROM Reviews", conn)

print(f"Pulled {len(reviews_df)} reviews into a DataFrame.")
print(reviews_df.head())  # shows the first 5 rows, just to sanity check


# --- STEP 3: DEFINE A FUNCTION TO ANALYZE SENTIMENT ---
# This function takes one piece of review text and returns:
#   - a polarity score (-1.0 to 1.0)
#   - a simple label: "positive", "negative", or "neutral"
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
# .apply() runs our function on every single row's review_text value.
# Since our function returns TWO values (polarity, label), we use zip(*...)
# to split those pairs out into two separate columns.
reviews_df["sentiment_score"], reviews_df["sentiment_label"] = zip(
    *reviews_df["review_text"].apply(analyze_sentiment)
)

print("\nSentiment analysis complete. Sample results:")
print(reviews_df[["review_text", "sentiment_score", "sentiment_label"]].head(10))


# --- STEP 4.5: CALCULATE AVERAGE SENTIMENT PER PRODUCT ---
# groupby("product_id") clusters all reviews that share the same product_id.
# .agg() lets us calculate multiple summary stats at once for each cluster:
#   - the average sentiment_score
#   - the total number of reviews
#   - the average star_rating
# reset_index() turns product_id back into a normal column instead of an index.
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
# This creates a NEW table called "Reviews_Analyzed" with all the original
# review data PLUS our new sentiment_score and sentiment_label columns.
# if_exists="replace" means: if this table already exists (e.g., we run this
# script again later), overwrite it instead of erroring out.
reviews_df.to_sql("Reviews_Analyzed", conn, if_exists="replace", index=False)

print("\nSaved results to a new table: Reviews_Analyzed")

# Also save the product-level summary as its own table
product_summary_df.to_sql("Product_Sentiment_Summary", conn, if_exists="replace", index=False)
print("Saved results to a new table: Product_Sentiment_Summary")

# --- STEP 6: CLOSE THE CONNECTION ---
# Always close your database connection when you're done, it's good practice.
conn.close()

print("Done! Check trend_spotter.db for the new Reviews_Analyzed table.")
