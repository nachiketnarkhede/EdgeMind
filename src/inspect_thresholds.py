
from pathlib import Path
import joblib

ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = ROOT / "models" / "edge_model.pkl"

model = joblib.load(MODEL_PATH)
tree = model.tree_

feature_names = model.feature_names_in_

print("\n===== EXACT DECISION TREE THRESHOLDS =====\n")

for node in range(tree.node_count):
    if tree.children_left[node] != tree.children_right[node]:
        feature_index = tree.feature[node]
        threshold = tree.threshold[node]

        print(
            f"Node {node}: "
            f"{feature_names[feature_index]} "
            f"<= {threshold:.10f}"
        )

print("\n===== END =====")
