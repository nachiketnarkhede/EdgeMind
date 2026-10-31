
import pandas as pd
from pathlib import Path

# Locate the dataset
data_path = Path(__file__).resolve().parent.parent / "data" / "sensor_data.csv"

# Load dataset
data = pd.read_csv(data_path)

# Display basic information
print("\n--- DATASET OVERVIEW ---")
print("Total readings:", len(data))
print("Columns:", list(data.columns))

# Display sample readings
print("\n--- FIRST 5 READINGS ---")
print(data.head())

# Check missing values
print("\n--- MISSING VALUES ---")
print(data.isnull().sum())

# Statistical summary
print("\n--- STATISTICAL SUMMARY ---")
print(data.describe())

# Machine condition distribution
print("\n--- MACHINE CONDITION DISTRIBUTION ---")
print(data["label"].value_counts().sort_index())
