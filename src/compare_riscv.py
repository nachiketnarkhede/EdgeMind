from pathlib import Path
import csv

import numpy as np
import pandas as pd
import joblib


# --------------------------------------------------
# PATHS
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_PATH = PROJECT_ROOT / "models" / "edge_model.pkl"
REPORT_PATH = PROJECT_ROOT / "reports" / "riscv_comparison.csv"


# --------------------------------------------------
# LOAD TRAINED PYTHON MODEL
# --------------------------------------------------

if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Trained model not found: {MODEL_PATH}\n"
        "Run your model-training script first."
    )

model = joblib.load(MODEL_PATH)


# --------------------------------------------------
# RISC-V EQUIVALENT CLASSIFIER
# Inputs are scaled by 100 to use integers.
#
# Class 0 = Normal
# Class 1 = Overheating
# Class 2 = Abnormal Vibration
# --------------------------------------------------

def riscv_equivalent_classifier(temperature, vibration):

    if vibration <= 392:

        if temperature <= 6875:

            if vibration <= 341:
                return 0
            else:
                return 2

        else:

            if temperature <= 6994:
                return 1

            elif temperature <= 7101:
                return 0

            else:
                return 1

    else:

        if temperature <= 8584:
            return 2
        else:
            return 1


# --------------------------------------------------
# GENERATE TEST INPUTS
# --------------------------------------------------

rng = np.random.default_rng(42)

number_of_tests = 10000

temperatures = rng.integers(
    2000, 11001, size=number_of_tests
)

vibrations = rng.integers(
    0, 801, size=number_of_tests
)


# --------------------------------------------------
# PYTHON MODEL PREDICTIONS
# --------------------------------------------------

X = pd.DataFrame({
    "temperature": temperatures / 100.0,
    "vibration": vibrations / 100.0
})

python_predictions = model.predict(X)


# --------------------------------------------------
# RISC-V RULE PREDICTIONS
# --------------------------------------------------

riscv_predictions = np.array([
    riscv_equivalent_classifier(int(t), int(v))
    for t, v in zip(temperatures, vibrations)
])


# --------------------------------------------------
# COMPARE BOTH IMPLEMENTATIONS
# --------------------------------------------------

matches = python_predictions == riscv_predictions

match_count = int(np.sum(matches))
mismatch_count = number_of_tests - match_count

agreement = (match_count / number_of_tests) * 100


# --------------------------------------------------
# DISPLAY RESULTS
# --------------------------------------------------

print("\n======================================")
print("       EDGEMIND VALIDATION")
print("======================================")

print("Total test inputs:       ", number_of_tests)
print("Matching predictions:   ", match_count)
print("Mismatching predictions: ", mismatch_count)

print(f"Agreement:                {agreement:.2f}%")

if mismatch_count == 0:
    print("\nSUCCESS: All predictions match.")
else:
    print("\nWARNING: Some predictions do not match.")


# --------------------------------------------------
# SAVE MISMATCH REPORT
# --------------------------------------------------

REPORT_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)

with open(REPORT_PATH, "w", newline="") as file:

    writer = csv.writer(file)

    writer.writerow([
        "temperature",
        "vibration",
        "python_prediction",
        "riscv_rule_prediction"
    ])

    for i in range(number_of_tests):

        if not matches[i]:

            writer.writerow([
                temperatures[i] / 100.0,
                vibrations[i] / 100.0,
                int(python_predictions[i]),
                int(riscv_predictions[i])
            ])


print("\nMismatch report saved to:")
print(REPORT_PATH)

print("\n======================================")
