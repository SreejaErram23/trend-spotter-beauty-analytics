Trend Spotter: Beauty Product Sentiment Dashboard 

Stack: SQLite, Python(pandas, TextBlob), Power BI

A data analytics platform that helps retail buyers understand how customers really feel about beauty products. It combines sales related data (star ratings) with automated sentiment analysis of customers reviews, all visualized in an interactive Power BI dashboard 

The Problem

Retail buyers at beauty companies make constant decisions about what to restock, discontinue, or market harder. Star ratings alone only tell part of the story, they don't explain why a product is succeeding or struggling. Reading through hundreds of individual reviews to find that “why” doesn't scale. 

This project automates that process. It takes raw customer review text, scores its sentiment using natural language processing, and surfaces the results in a dashboard a buyer can scan in seconds, with no manual reading required.

Tech Stack

Layer
Tool
database
SQLite (via DB Browser for SQLite)
Data Processing
Python, pandas
Sentiment Analysis
TextBlob
Visualization
Power BI


How It Works
SQL: A relational database (trend_spotter.db) stores core tables. Products holds 12 beauty products across nails, makeup, and skincare. Reviews holds 48 mock customer reviews, 4 per product, with star ratings and dates 
Python: A script (sentiment_analysis.py) connects to the database, pulls the reviews into a pandas DataFrame, and runs each review through TextBlob to generate a sentiment polarity score ( from negative 1 to positive 1) and a positive, negative, or neutral label. It then aggregates sentiment by product using groupby, and writes both the details and summarized results back into the database as new tables 
(Reviews_Analyzed and Product_Sentiment_Summary).

Power BI: The data is visualized in an interactive dashboard with two charts (average sentiment by product, average star rating by product) and a category slicer that lets a viewer filter by nails, makeup, or skincare

Key Insight

Star ratings and sentiment scores don't always agree. Several products with solidly “average” star ratings (around 3.5) showed clearly negative sentiment scores once the actual review text was analyzed. This means customers were expressing real dissatisfactions that a simple star number, from one to five, did not fully capture. That's the core value, sentiment analysis surfaces problems that star ratings alone can hide.

Design Decisions

Mock and synthetic data: All product and review data was generated for this project since real company review data is proprietary. Product names and trends were chosen from real, current beauty and nail trends (glazed donut nails, cat eye magnetic polish, peptide glazing fluid) to keep the dataset realistic and personally meaningful.

Scope: this project is diagnostic and descriptive, not predictive. It shows what's currently trending and why, not a forecast of future performance

What I’d Add Next
Cross reference sentiment with a price column to see if theres a relationship between price point and sentiment, such as whether a cheaper product gets harsher reviews relative to expectations 
Expand the review data sent with more reviews per product (currently 4) so sentiment averages are more statistically meaningful and less swayed by a single outlier review
Compare TextBlobs results against VADER, a sentiment tool built specifically for casual and social language, since TextBlob occasionally misjudged enthusiastic slang in the reviews like “obsessed”. 
