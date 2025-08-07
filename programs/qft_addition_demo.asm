# programs/qft_addition_demo.asm
# QFT-based addition of A=1 and B=2 (mod 4) on a 2-qubit A-register

# --- Prepare A = |01> ---
reset q0
reset q1
x q0           # A = 1 → |01>

# --- Prepare B = |10> ---
reset q2
reset q3
x q3           # B = 2 → |10>

# --- QFT on A-register (q0 LSB, q1 MSB) ---
qft q0 q1

# --- Phase rotations to add B into A ---
# Controlled by B’s LSB (q2):
#   angle on q0 = π/2
#   angle on q1 = π
cz q2 q0       # CZ imparts π conditional phase on q0
rz 1.5708 q0   # +π/2 rotation on q0

cz q2 q1       # CZ imparts π conditional phase on q1
rz 3.14159 q1  # +π rotation on q1

# Controlled by B’s MSB (q3):
#   angle on q0 = π
cz q3 q0       # conditional π phase on q0

# (No rotation on q1 since angle 2π ≡ 0)

# --- Inverse QFT on A-register ---
swap q0 q1
h q1
rz -1.5708 q0
cz q1 q0
h q0

# --- Measure and output result ---
measure q0 p0   # LSB of sum
measure q1 p1   # MSB of sum
out p1          # print MSB
out p0          # print LSB

# Expected output: OUT: 1, OUT: 1  (binary 11 = decimal 3)
