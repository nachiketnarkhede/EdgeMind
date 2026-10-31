# EdgeMind
### A Python-to-RISC-V Edge Classification Project

EdgeMind explores how a machine-learning model trained in Python can be translated into a low-level RV32I assembly implementation for sensor classification.

The project uses temperature and vibration data to classify three operating conditions. It connects model training, decision-rule extraction, integer-based inference, assembly implementation, and cross-implementation validation.

## Project Overview

The project follows this workflow:

1. Generate and inspect a labelled sensor dataset.
2. Train a Decision Tree classifier using Python.
3. inspect the trained model and its decision thresholds.
4. Translate the classifier's decision logic into RV32I assembly.
5. Compare the Python and RISC-V implementations.
6. Validate representative assembly test cases using the Venus simulator.

## Classification Classes

| Class ID | Label |
|---:|---|
| 0 | Normal |
| 1 | Overheating |
| 2 | Abnormal Vibration |

## Project Structure

```text
EdgeMind/
├── .vscode/
│   └── launch.json
├── data/
│   └── sensor_data.csv
├── models/
│   └── edge_model.pkl
├── reports/
│   ├── riscv_comparison.csv
│   └── riscv_validation.md
├── riscv/
│   └── assembly/
│       ├── edge_classifier.asm
│       └── edge_classifier_core.S
└── src/
    ├── compare_riscv.py
    ├── generate_data.py
    ├── inspect_data.py
    ├── inspect_model.py
    ├── inspect_thresholds.py
    ├── train_model.py
    ├── verify_rules.py
    └── visualize_data.py
```

## Technical Implementation

### Python Machine Learning

- Dataset generation and inspection
- Decision Tree model training
- Model inspection and threshold extraction
- Prediction-rule verification
- Data visualization

### RV32I Assembly

The extracted decision logic is implemented in RV32I assembly.

Sensor inputs are represented as integers scaled by 100 to avoid floating-point operations in the classifier.

| Register | Input |
|---|---|
| `a0` | Temperature × 100 |
| `a1` | Vibration × 100 |

The predicted class is returned in `a0`.

### Validation

Two separate validation approaches are included:

**Assembly simulation**
- Three representative test cases executed in Venus.
- All three test cases passed.
- Final test harness result: `a0 = 3`.

**Python-to-RISC-V comparison**
- 10,000 generated test inputs.
- 10,000 matching predictions.
- Zero mismatches.
- Recorded agreement: 100.00%.

See [`reports/riscv_validation.md`](reports/riscv_validation.md) and [`reports/riscv_comparison.csv`](reports/riscv_comparison.csv) for the recorded results and validation scope.

## Technologies

- Python
- scikit-learn
- pandas
- NumPy
- Matplotlib
- RISC-V RV32I Assembly
- Venus RISC-V Simulator
- Visual Studio Code

## Scope and Limitations

This is an experimental software-level implementation and validation project.

The reported comparison results apply to the generated test inputs and the implemented decision rules. They do not establish exhaustive correctness, hardware-level performance, or real-world sensor reliability.

The project currently focuses on translating and validating classifier logic rather than deploying it on physical RISC-V hardware.

## Project Status

**Current stage:** Python model implementation, RV32I translation, and simulator-based validation completed.

Further work can explore execution efficiency, memory usage, hardware deployment, and validation with measured sensor data.

## Reference

The assembly implementation follows the RV32I base integer instruction set. See the [official RISC-V specifications](https://docs.riscv.org/reference/isa/unpriv/rv32.html).