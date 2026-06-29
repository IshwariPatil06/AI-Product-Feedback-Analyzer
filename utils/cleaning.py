import pandas as pd

# Load dataset
df = pd.read_csv("data/reviews.csv")

# Keep only required columns
df = df[
    [
        "content",
        "score",
        "thumbsUpCount",
        "reviewCreatedVersion",
        "at",
        "appId"
    ]
]

# Remove rows with missing review text
df = df.dropna(subset=["content"])

# Remove duplicate reviews
df = df.drop_duplicates(subset=["content"])

# Reset index
df = df.reset_index(drop=True)

# Print missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Print first five cleaned rows
print("\nFirst Five Rows:")
print(df.head())

# Save cleaned dataset
df.to_csv("data/cleaned_reviews.csv", index=False)

print("\n✅ Cleaned dataset saved successfully!")