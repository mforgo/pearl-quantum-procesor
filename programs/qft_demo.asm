# programs/qft_example.asm
# 3-qubit QFT example: start in |5> = |101>, apply QFT, measure result

# --- Prepare |101> on q2q1q0 ---
# q0 is least significant bit, q2 most
x q0           # Set q0 = 1 (LSB)
# q1 remains 0
x q2           # Set q2 = 1 (MSB)

# --- Apply 3-qubit Quantum Fourier Transform ---
qft q0 q1 q2   # qft instruction applies QFT on [q0,q1,q2] in place

# --- Measure each qubit into classical registers p0,p1,p2 ---
measure q0 p0
measure q1 p1
measure q2 p2

# --- Output measured Fourier components ---
out p0
out p1
out p2
