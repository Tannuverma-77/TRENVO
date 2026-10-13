"""
weekly_trend_simulation.py
-----------------------------
Simulates how song trend scores change week to week.
Since we only have a single snapshot of data (not live streaming data),
this creates 4 realistic "weeks" (Week 1 = 3 weeks ago ... Week 4 = current)
by applying small random changes to each song's trend_score - similar to
how real trends rise and fall over time.

Input:  data/processed/music_data_features.csv
Output: data/processed/weekly_trends.csv
"""

import pandas as pd
import numpy as np
import os

input_path = "data/processed/music_data_features.csv"
output_path = "data/processed/weekly_trends.csv"

os.makedirs("data/processed", exist_ok=True)

df = pd.read_csv(input_path)

base = df[["track_name", "artists", "trend_score"]].copy()

np.random.seed(42)  # same result every time we run it

weekly_frames = []
current_scores = base["trend_score"].copy()

for week in range(1, 5):  # Week 1 (oldest) to Week 4 (current)
    change = np.random.uniform(-8, 8, size=len(base))
    current_scores = (current_scores + change).round(2).clip(lower=0, upper=100)

    week_df = base[["track_name", "artists"]].copy()
    week_df["trend_score"] = current_scores.values
    week_df["week"] = f"Week {week}"
    weekly_frames.append(week_df)

weekly_trends = pd.concat(weekly_frames, ignore_index=True)
weekly_trends.to_csv(output_path, index=False)

print("Weekly trend simulation completed!")
print("Shape:", weekly_trends.shape)
print("Saved to:", output_path)