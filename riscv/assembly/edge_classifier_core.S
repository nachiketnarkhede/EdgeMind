
.text
.globl main
.globl edge_classifier

main:
    # Test 1: Overheating
    # Temperature = 68.76, Vibration = 2.00
    lui  a0, 2
    addi a0, a0, -1316
    addi a1, x0, 200
    jal  ra, edge_classifier

    addi t3, a0, 0
    addi t4, x0, 1
    bne  t3, t4, test1_fail
    addi s0, x0, 1
    jal  x0, test2

test1_fail:
    addi s0, x0, 0

test2:
    # Test 2: Normal
    # Temperature = 69.95, Vibration = 2.00
    lui  a0, 2
    addi a0, a0, -1197
    addi a1, x0, 200
    jal  ra, edge_classifier

    addi t3, a0, 0
    addi t4, x0, 0
    bne  t3, t4, test2_fail
    addi s1, x0, 1
    jal  x0, test3

test2_fail:
    addi s1, x0, 0

test3:
    # Test 3: Abnormal Vibration
    # Temperature = 68.76, Vibration = 5.00
    lui  a0, 2
    addi a0, a0, -1316
    addi a1, x0, 500
    jal  ra, edge_classifier

    addi t3, a0, 0
    addi t4, x0, 2
    bne  t3, t4, test3_fail
    addi s2, x0, 1
    jal  x0, finish_tests

test3_fail:
    addi s2, x0, 0

finish_tests:
    # s0, s1, s2 contain individual test results.
    # Each is 1 for PASS and 0 for FAIL.
    add  s3, s0, s1
    add  s3, s3, s2

    # s3 = total passed tests (0 to 3)
    # a0 = total passed tests
    addi a0, s3, 0
    ebreak


# ==========================================
# EDGE CLASSIFIER
# ==========================================

edge_classifier:

    # Check vibration <= 3.92
    addi t0, x0, 392
    bge  t0, a1, vibration_low
    jal  x0, vibration_high

vibration_low:
    # Check temperature <= 68.75
    lui  t0, 2
    addi t0, t0, -1317
    bge  t0, a0, temperature_low
    jal  x0, temperature_high

temperature_low:
    # Check vibration <= 3.41
    addi t0, x0, 341
    bge  t0, a1, result_normal
    jal  x0, result_abnormal

temperature_high:
    # Check temperature <= 69.94
    lui  t0, 2
    addi t0, t0, -1198
    bge  t0, a0, result_overheating

    # Check temperature <= 71.01
    lui  t0, 2
    addi t0, t0, -1091
    bge  t0, a0, result_normal
    jal  x0, result_overheating

vibration_high:
    # Check temperature <= 85.84
    lui  t0, 2
    addi t0, t0, 392
    bge  t0, a0, result_abnormal
    jal  x0, result_overheating

result_normal:
    addi a0, x0, 0
    jalr x0, 0(ra)

result_overheating:
    addi a0, x0, 1
    jalr x0, 0(ra)

result_abnormal:
    addi a0, x0, 2
    jalr x0, 0(ra)
