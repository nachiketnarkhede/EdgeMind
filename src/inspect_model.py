
import joblib

from pathlib import Path
from sklearn.tree import export_text

# Locate saved model
BASE_DIR = Path(__file__).resolve().parent.parent
model_path = BASE_DIR / "models" / "edge_model.pkl"

# Load trained model
model = joblib.load(model_path)

# Extract decision rules
rules = export_text(
    model,
    feature_names=["temperature", "vibration"]
)

print("\n--- EDGEMIND DECISION RULES ---")
print(rules)
