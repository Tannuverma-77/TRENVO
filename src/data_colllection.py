import pandas as pd

file_path = "data/raw/music_data.csv"

df = pd.read_csv(file_path)

print("TRENVO Dataset Loaded Successfully!")
print("Number of songs:", len(df))
print("\nColumns:")
print(df.columns.tolist())