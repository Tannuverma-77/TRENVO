# TRENVO Project Analysis

## Overview
TRENVO is a data analytics and machine learning pipeline designed to analyze and predict music trends using a Spotify tracks dataset. It processes raw track data, engineers trend-related features, simulates weekly changes, and trains a predictive model. 

## Project Structure
The project is organized into several directories:
- `data/`: Contains the datasets.
  - `raw/`: Stores the original `music_data.csv`.
  - `processed/`: Stores cleaned and feature-engineered datasets (`music_data_clean.csv`, `music_data_features.csv`, `weekly_trends.csv`).
- `src/`: Contains the Python source code for the data pipeline.
- `notebooks/`: Contains Jupyter Notebooks (`analysis.ipynb`) for exploratory data analysis (EDA).
- `database/`, `gui/`, `model/`: Currently empty directories, likely intended for future expansion.

## Data Pipeline & Scripts
1. **`data_colllection.py`** *(Note: typo in filename)*
   - A simple script to load the raw `music_data.csv` dataset and print basic information (number of songs and columns).
2. **`data_cleaning.py`**
   - Cleans the raw dataset by dropping unneeded index columns, removing duplicates (both exact and by `track_id`), and filling missing numeric/text values. Outputs `music_data_clean.csv`.
3. **`feature_engineering.py`**
   - Engineers a custom continuous `trend_score` based on a weighted combination of a track's `popularity`, `danceability`, and `energy`. It also calculates the average trend score grouped by artist and genre. Outputs `music_data_features.csv`.
4. **`weekly_trend_simulation.py`**
   - Since the dataset is static, this script simulates 4 weeks of historical trend data by applying random fluctuations (between -8 and +8) to the `trend_score`. Outputs `weekly_trends.csv`.
5. **`prediction.py`**
   - A script meant to train a `RandomForestClassifier` to predict whether a song is `trending`.

## Notebook Analysis (`analysis.ipynb`)
The Jupyter notebook loads the feature-engineered dataset (`music_data_features.csv`) and performs exploratory analysis. It extracts and displays:
- The top 10 trending songs overall (e.g., *Super Freaky Girl* by Nicki Minaj, *Me Porto Bonito* by Bad Bunny).
- The top 10 artists based on their average `trend_score`.

> [!WARNING] Issues & Bugs Detected in `prediction.py`
> While analyzing the source code, several inconsistencies were found in `prediction.py` that will prevent it from running correctly:
> 1. **Incorrect File Path**: It tries to load `data/processed/featured_music_data.csv`, but the actual engineered file is named `music_data_features.csv`.
> 2. **Missing Target Column**: It attempts to use a target column named `"trending"`, but `feature_engineering.py` only creates a continuous `"trend_score"` column. A binary classification target needs to be created first (e.g., `df['trending'] = df['trend_score'] > threshold`).
> 3. **Mismatched Column Names**: It tries to drop `"song_name"`, `"artist_name"`, and `"release_date"`, but the dataset actually uses the naming conventions: `"track_name"`, `"artists"`.

## Recommendations for Next Steps
1. **Fix `prediction.py`**: Update the script to use the correct dataset, properly define the binary `"trending"` target (or switch to a Regressor to predict the score), and drop the correct columns.
2. **Expand the Notebook**: Add data visualizations (e.g., using `matplotlib` or `seaborn`) to show how features like danceability correlate with the trend score.
3. **Utilize Empty Directories**: Save the trained Random Forest model to the `model/` directory using `joblib` or `pickle`.
