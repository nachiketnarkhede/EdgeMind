
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Load dataset
data_path = Path(__file__).resolve().parent.parent / "data" / "sensor_data.csv"
data = pd.read_csv(data_path)

# Give labels readable names
condition_names = {
    0: "Normal",
    1: "Overheating",
    2: "Abnormal Vibration"
}

data["condition"] = data["label"].map(condition_names)

# Create scatter plot
plt.figure(figsize=(10, 6))

for condition, group in data.groupby("condition"):
    plt.scatter(
        group["temperature"],
        group["vibration"],
        label=condition,
        alpha=0.5
    )

plt.title("EdgeMind - Machine Sensor Analysis")
plt.xlabel("Temperature")
plt.ylabel("Vibration")
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
