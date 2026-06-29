import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import re 

# Load cleaned dataset
df = pd.read_csv("data/cleaned_reviews.csv")

# Display first five rows
print(df.head())

# Total reviews
total_reviews = len(df)

# Average rating
average_rating = df["score"].mean()

# Highest rating
highest_rating = df["score"].max()

# Lowest rating
lowest_rating = df["score"].min()

print("\n========== REVIEW ANALYTICS ==========\n")

print(f"Total Reviews : {total_reviews}")

print(f"Average Rating : {round(average_rating,2)}")

print(f"Highest Rating : {highest_rating}")

print(f"Lowest Rating : {lowest_rating}")

rating_distribution = df["score"].value_counts().sort_index()

print("\n========== RATING DISTRIBUTION ==========\n")

for rating, count in rating_distribution.items():
    print(f"{rating} ⭐ : {count} reviews")

print("\n========== RATING PERCENTAGE ==========\n")

for rating, count in rating_distribution.items():
    percentage = (count / total_reviews) * 100
    print(f"{rating} ⭐ : {percentage:.2f}%")

most_common_rating = df["score"].mode()[0]

print(f"\nMost Common Rating : {most_common_rating}")

# ---------------------------------
# Sentiment Analysis
# ---------------------------------

def get_sentiment(rating):

    if rating >= 4:
        return "Positive"

    elif rating == 3:
        return "Neutral"

    else:
        return "Negative"


df["Sentiment"] = df["score"].apply(get_sentiment)
sentiment_counts = df["Sentiment"].value_counts()

print("\n========== SENTIMENT DISTRIBUTION ==========\n")

print(sentiment_counts)
print("\n========== SENTIMENT PERCENTAGE ==========\n")

for sentiment, count in sentiment_counts.items():

    percentage = (count / len(df)) * 100

    print(f"{sentiment} : {percentage:.2f}%")
    overall_sentiment = sentiment_counts.idxmax()

print("\nOverall User Sentiment :", overall_sentiment)
# ---------------------------------
# Combine all reviews into one text
# ---------------------------------

all_reviews = " ".join(df["content"].astype(str))

print("\nTotal Characters :", len(all_reviews))
all_reviews = all_reviews.lower()

print("\nFirst 200 characters:\n")
print(all_reviews[:200])
words = all_reviews.split()

print("\nTotal Words :", len(words))
word_counts = Counter(words)
print("\n========== TOP 10 MOST COMMON WORDS ==========\n")

for word, count in word_counts.most_common(10):
    print(f"{word} : {count}")
    # ---------------------------------
# Stop Words
# ---------------------------------

stop_words = {
    "the","to","and","a","i","it","is","of","for","in","my",
    "this","that","on","was","with","are","have","had","be",
    "as","at","an","or","if","but","so","we","you","your",
    "our","they","their","them","he","she","his","her",
    "from","by","about","after","before","very","can",
    "will","would","should","could","has","been"
}
filtered_words = []

for word in words:

    if word not in stop_words:

        filtered_words.append(word)

print("\nWords After Removing Stop Words :", len(filtered_words))
filtered_counts = Counter(filtered_words)
# ===============================
# TOP 10 WORDS BAR CHART
# ===============================

top_words = filtered_counts.most_common(10)

words = []
counts = []

for word, count in top_words:
    words.append(word)
    counts.append(count)

plt.figure(figsize=(10,6))

plt.barh(words, counts)

plt.title("Top 10 Most Frequent Words")

plt.xlabel("Frequency")

plt.ylabel("Words")

plt.tight_layout()

plt.savefig("charts/top_words.png")

plt.show()

print("\n✅ Top Words Chart Saved Successfully!")
print("\n========== TOP 20 IMPORTANT WORDS ==========\n")

for word, count in filtered_counts.most_common(20):
    print(f"{word} : {count}")
    # ---------------------------------
# Rating Distribution Bar Chart
# ---------------------------------

rating_counts = df["score"].value_counts().sort_index()

plt.figure(figsize=(8,5))

plt.bar(
    rating_counts.index.astype(str),
    rating_counts.values
)

plt.title("Rating Distribution")

plt.xlabel("Star Rating")

plt.ylabel("Number of Reviews")

plt.savefig("charts/rating_distribution.png")

plt.close()

print("\n✅ Rating Distribution Chart Saved!")
# -------------------------------
# Sentiment Pie Chart
# -------------------------------

sentiment_counts = df["Sentiment"].value_counts()

plt.figure(figsize=(7,7))

plt.pie(
    sentiment_counts,
    labels=sentiment_counts.index,
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Sentiment Distribution")

plt.axis("equal")

plt.savefig("charts/sentiment_pie.png")

plt.show()
# ===========================
# REVIEW TREND CHART
# ===========================

# Convert to datetime
df["at"] = pd.to_datetime(df["at"])

# Extract only date
df["date"] = df["at"].dt.date

# Count reviews per day
review_trend = df.groupby("date").size()

print(review_trend.head())

# Create chart
plt.figure(figsize=(12,6))

plt.plot(review_trend.index,
         review_trend.values)

plt.title("Review Trend Over Time")

plt.xlabel("Date")

plt.ylabel("Number of Reviews")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig("charts/review_trend.png")

plt.show()

