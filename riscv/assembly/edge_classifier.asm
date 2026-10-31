
.data
normal_msg:     .asciz "Machine condition: NORMAL\n"
overheat_msg:   .asciz "Machine condition: OVERHEATING\n"
vibration_msg:  .asciz "Machine condition: ABNORMAL VIBRATION\n"

.text
.globl main

main:
    # Read temperature (scaled by 100)
    li a7, 5
    ecall
    mv s0, a0

    # Read vibration (scaled by 100)
    li a7, 5
    ecall
    mv s1, a0

    # First decision: vibration <= 3.93?
    li t0, 393
    bgt s1, t0, high_vibration

    # Temperature <= 68.76?
    li t0, 6876
    bgt s0, t0, medium_temperature

    # Vibration <= 3.41?
    li t0, 341
    bgt s1, t0, abnormal_vibration

    # Class 0
    j normal

medium_temperature:
    # Temperature <= 71.01?
    li t0, 7101
    bgt s0, t0, high_temperature

    # Temperature <= 69.95?
    li t0, 6995
    bgt s0, t0, normal

    j overheating

high_temperature:
    # Temperature <= 74.28?
    li t0, 7428
    bgt s0, t0, overheating

    j overheating

high_vibration:
    # Temperature <= 85.84?
    li t0, 8584
    bgt s0, t0, overheating

    j abnormal_vibration

normal:
    la a0, normal_msg
    j display_result

overheating:
    la a0, overheat_msg
    j display_result

abnormal_vibration:
    la a0, vibration_msg

display_result:
    li a7, 4
    ecall

    li a7, 10
    ecall
