
import pandas as pd
import joblib

from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# Locate and load dataset
BASE_DIR = Path(__file__).resolve().parent.parent
data = pd.read_csv(BASE_DIR / "data" / "sensor_data.csv")

# Separate input features and target labels
X = data[["temperature", "vibration"]]
y = data["label"]

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Create the decision tree
model = DecisionTreeClassifier(
    max_depth=4,
    random_state=42
)

# Train the model
model.fit(X_train, y_train)

# Make predictions
predictions = model.predict(X_test)

# Evaluate performance
print("\n--- MODEL PERFORMANCE ---")
print("Accuracy:", accuracy_score(y_test, predictions))

print("\n--- CLASSIFICATION REPORT ---")
print(classification_report(y_test, predictions))

print("\n--- CONFUSION MATRIX ---")
print(confusion_matrix(y_test, predictions))

# Save trained model
model_path = BASE_DIR / "models" / "edge_model.pkl"
joblib.dump(model, model_path)

print("\nModel saved successfully:", model_path)
