
import joblib
import pandas as pd

from pathlib import Path
from sklearn.model_selection import train_test_split

BASE_DIR = Path(__file__).resolve().parent.parent

# Load dataset and trained model
data = pd.read_csv(BASE_DIR / "data" / "sensor_data.csv")
model = joblib.load(BASE_DIR / "models" / "edge_model.pkl")

X = data[["temperature", "vibration"]]
y = data["label"]

# Recreate the original test split
_, X_test, _, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Predictions from the trained model
model_predictions = model.predict(X_test)

# Predictions using extracted decision rules
def classify_machine(temperature, vibration):

    if vibration <= 3.93:

        if temperature <= 68.76:

            if vibration <= 3.41:

                if temperature <= 66.01:
                    return 0
                else:
                    return 0

            else:
                return 2

        else:

            if temperature <= 71.01:

                if temperature <= 69.95:
                    return 1
                else:
                    return 0

            else:

                if temperature <= 74.28:
                    return 1
                else:
                    return 1

    else:

        if temperature <= 85.84:
            return 2
        else:
            return 1


# Run extracted rules on test data
rule_predictions = [
    classify_machine(row.temperature, row.vibration)
    for row in X_test.itertuples(index=False)
]

# Compare both prediction sets
matches = sum(
    a == b
    for a, b in zip(model_predictions, rule_predictions)
)

print("Total test samples:", len(X_test))
print("Matching predictions:", matches)
print("Rule agreement:", matches / len(X_test) * 100, "%")

if matches == len(X_test):
    print("\nSUCCESS: Extracted rules match the model!")
else:
    print("\nSome predictions differ. Further inspection needed.")
