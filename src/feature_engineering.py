"""
feature_engineering.py
------------------------
Creates trend-analysis features from the cleaned dataset.

What it does:
- Calculates a trend_score per song (popularity + danceability + energy)
- Calculates average trend_score per artist
- Calculates average trend_score per genre

Input:  data/processed/music_data_clean.csv
Output: data/processed/music_data_features.csv
"""
import pandas as pd
import os

# Paths
input_path = "data/processed/music_data_clean.csv"
output_path = "data/processed/music_data_features.csv"

# Make sure output folder exists
os.makedirs("data/processed", exist_ok=True)

# Load the cleaned dataset
df = pd.read_csv(input_path)

print("Loaded dataset shape:", df.shape)

# --- Create trend_score ---
# Combines popularity (main signal) with danceability and energy
# (songs that are popular AND high-energy/danceable tend to trend more)
df["trend_score"] = (
    df["popularity"] * 0.6 +
    df["danceability"] * 100 * 0.2 +
    df["energy"] * 100 * 0.2
)

# Round trend_score to 2 decimal places for readability
df["trend_score"] = df["trend_score"].round(2)

# --- Artist-level aggregation ---
# Average trend_score per artist (helps for "Top Artists" and comparison feature)
artist_avg = df.groupby("artists")["trend_score"].mean().round(2)
df["artist_avg_trend_score"] = df["artists"].map(artist_avg)

# --- Genre-level aggregation ---
# Average trend_score per genre
genre_avg = df.groupby("track_genre")["trend_score"].mean().round(2)
df["genre_avg_trend_score"] = df["track_genre"].map(genre_avg)

# Save the new dataset with features
df.to_csv(output_path, index=False)

print("Feature engineering completed successfully!")
print("New columns added: trend_score, artist_avg_trend_score, genre_avg_trend_score")
print("Final dataset shape:", df.shape)
print("Saved to:", output_path)

# Quick preview: Top 10 trending songs
print("\nTop 10 Trending Songs:")
print(df.sort_values("trend_score", ascending=False)[["track_name", "artists", "trend_score"]].head(10))