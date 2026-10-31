
import numpy as np
import pandas as pd
from pathlib import Path

# Make results reproducible
np.random.seed(42)

# Number of samples for each machine condition
samples = 1000

# 1. Normal machine operation
normal_temp = np.random.normal(55, 5, samples)
normal_vibration = np.random.normal(2, 0.5, samples)

# 2. Machine overheating
overheat_temp = np.random.normal(90, 8, samples)
overheat_vibration = np.random.normal(2.2, 0.6, samples)

# 3. Abnormal vibration
vibration_temp = np.random.normal(58, 6, samples)
vibration_level = np.random.normal(7, 1.2, samples)

# Combine sensor readings
temperature = np.concatenate([
    normal_temp,
    overheat_temp,
    vibration_temp
])

vibration = np.concatenate([
    normal_vibration,
    overheat_vibration,
    vibration_level
])

# Assign labels
labels = np.concatenate([
    np.zeros(samples),
    np.ones(samples),
    np.full(samples, 2)
])

# Create dataset
data = pd.DataFrame({
    "temperature": temperature,
    "vibration": vibration,
    "label": labels.astype(int)
})

# Shuffle the dataset
data = data.sample(frac=1, random_state=42).reset_index(drop=True)

# Save CSV in the data folder
output_path = Path(__file__).resolve().parent.parent / "data" / "sensor_data.csv"
data.to_csv(output_path, index=False)

print("Sensor dataset generated successfully!")
print(data.head())
print("\nDataset shape:", data.shape)
print("\nClass distribution:")
print(data["label"].value_counts().sort_index())
