import pandas as pd
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Load feature-engineered dataset
input_path = "data/processed/music_data_features.csv"
model_path = "model/trend_model.pkl"

df = pd.read_csv(input_path)

print("Feature-engineered dataset loaded successfully!")
print("Shape:", df.shape)

# Create binary target column "trending" (e.g., trend_score > 75)
threshold = 75
df['trending'] = (df['trend_score'] >= threshold).astype(int)
target = "trending"

# Remove columns that are not useful for ML
drop_columns = [
    "track_id",
    "track_name",
    "artists",
    "album_name",
    "trend_score"
]

# Remove rows where target is missing
df = df.dropna(subset=[target])

# Separate features and target
X = df.drop(columns=[target] + drop_columns, errors="ignore")
y = df[target]

# Convert categorical columns into numeric columns
X = pd.get_dummies(X, drop_first=True)

# Fill missing numeric values with median
X = X.fillna(X.median(numeric_only=True))

print("\nMissing values handled successfully!")
print("Remaining missing values:", X.isna().sum().sum())

print("\nFeatures prepared successfully!")
print("Feature shape:", X.shape)

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Create Random Forest model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

# Train model
print("Training model...")
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, y_pred)

print("\n===== TRENVO TREND PREDICTION =====")
print("Accuracy:", accuracy)

print("\nClassification Report:")
print(classification_report(
    y_test,
    y_pred,
    zero_division=0
))

# Save the model and columns for future use
os.makedirs("model", exist_ok=True)
joblib.dump({"model": model, "columns": X.columns.tolist()}, model_path)
print(f"Model saved to {model_path}")
