"""
data_cleaning.py
------------------
Cleans the raw Spotify Tracks Dataset.

What it does:
- Removes duplicate rows (including duplicate track_ids)
- Fills missing numeric values with 0
- Fills missing text values (track name, artist, genre) with "Unknown"

Input:  data/raw/music_data.csv
Output: data/processed/music_data_clean.csv
""" 
import pandas as pd
import os

# Paths
input_path = "data/raw/music_data.csv"
output_path = "data/processed/music_data_clean.csv"

# Make sure output folder exists
os.makedirs("data/processed", exist_ok=True)

# Load the dataset
df = pd.read_csv(input_path)

print("Original dataset shape:", df.shape)
print("Columns:", df.columns.tolist())

# Drop the unnamed index column if it exists (Kaggle datasets often have this)
if df.columns[0].startswith("Unnamed"):
    df = df.drop(columns=[df.columns[0]])

# Remove exact duplicate rows
df = df.drop_duplicates()

# Remove duplicates based on track_id (same song can appear more than once)
df = df.drop_duplicates(subset="track_id")

# Define numeric columns actually present in this dataset
numeric_columns = [
    "popularity", "duration_ms", "danceability", "energy", "key",
    "loudness", "mode", "speechiness", "acousticness",
    "instrumentalness", "liveness", "valence", "tempo", "time_signature"
]

# Convert numeric columns to proper numeric type (invalid values become NaN)
for column in numeric_columns:
    if column in df.columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

# Fill missing numeric values with 0
df[numeric_columns] = df[numeric_columns].fillna(0)

# Fill missing text values with "Unknown"
df["track_name"] = df["track_name"].fillna("Unknown")
df["artists"] = df["artists"].fillna("Unknown")
df["album_name"] = df["album_name"].fillna("Unknown")
df["track_genre"] = df["track_genre"].fillna("Unknown")

# Save cleaned dataset
df.to_csv(output_path, index=False)

print("Data cleaning completed successfully!")
print("Cleaned dataset shape:", df.shape)
print("Saved to:", output_path)


