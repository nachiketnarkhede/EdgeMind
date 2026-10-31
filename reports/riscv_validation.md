# EdgeMind — RISC-V Classifier Validation

## 1. Overview

EdgeMind implements a machine-learning-based sensor classifier in Python and translates its decision logic into an RV32I assembly implementation.

This validation stage checks whether the assembly classifier produces the expected class labels for representative sensor inputs. It also documents register-level observations made using the Venus RISC-V Simulator.

## 2. Execution Environment

- **Simulator:** Venus RISC-V Simulator
- **Development Environment:** Visual Studio Code
- **Instruction Set:** RV32I
- **Assembly Source:** `riscv/assembly/edge_classifier_core.S`
- **Input Representation:** Integer values scaled by 100

## 3. Input and Output Convention

To avoid floating-point operations in the assembly classifier, sensor values are represented as integers scaled by 100.

Examples:

- Temperature 68.76 → 6876
- Vibration 2.00 → 200

The classifier receives:

| Register | Description |
|---|---|
| `a0` (`x10`) | Temperature × 100 |
| `a1` (`x11`) | Vibration × 100 |

The predicted class is returned in `a0`.

### Class Labels

| Class ID | Classification |
|---:|---|
| 0 | Normal |
| 1 | Overheating |
| 2 | Abnormal Vibration |

## 4. Assembly Test Results

The assembly test harness executes three representative test cases and checks each returned class against its expected result.

| Test | Temperature | Vibration | Expected Class | Result |
|---|---:|---:|---|---|
| 1 | 68.76 | 2.00 | 1 — Overheating | PASS |
| 2 | 69.95 | 2.00 | 0 — Normal | PASS |
| 3 | 68.76 | 5.00 | 2 — Abnormal Vibration | PASS |

**Result: 3 out of 3 tests passed.**

## 5. Register-Level Verification

The Venus debugger was used to inspect register values during execution.

The automated test harness stores individual test results in:

- `s0` — Test 1 result
- `s1` — Test 2 result
- `s2` — Test 3 result
- `s3` — Total number of passed tests

At the final `ebreak` instruction:

- `s0 = 1`
- `s1 = 1`
- `s2 = 1`
- `s3 = 3`
- `a0 = 3`

The value `3` in `a0` confirms that all three test cases passed.

## 6. Python-to-RISC-V Rule Comparison

A separate Python comparison script evaluates the translated decision rules against the Python classifier over 10,000 generated test inputs.

Recorded comparison results:

- **Total test inputs:** 10,000
- **Matching predictions:** 10,000
- **Mismatches:** 0
- **Agreement:** 100.00%

These results are recorded in `reports/riscv_comparison.csv`.

This comparison is separate from the three assembly tests executed in Venus.

## 7. Conclusion and Validation Scope

The RV32I assembly implementation passed all three representative test cases in the Venus simulator. The separate Python-to-RISC-V rule comparison also recorded 100% agreement across 10,000 generated inputs.

Together, these results provide evidence that the translated decision logic reproduces the Python classifier's predictions for the tested inputs.

**Limitations:** The three Venus tests are representative functional checks, not exhaustive verification of all possible inputs or decision boundaries. The 10,000-case comparison is also limited to its generated test inputs and does not constitute formal verification of the assembly program.