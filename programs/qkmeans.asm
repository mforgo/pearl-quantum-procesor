# programs/qkmeans_single_step.asm
# Quantum K-Means: single distance estimation step
#
# Registers:
# p0 = new data point theta (angle in radians)
# p1 = new data point phi (angle in radians)
# p2 = centroid theta (angle in radians)
# p3 = centroid phi (angle in radians)
# p4 = measurement result

mov 17394 p0     # newPoint θ ≈ 1.7394 * 10000
mov 20828 p1     # newPoint φ ≈ 2.0828 * 10000
mov 20420 p2     # centroid θ
mov 18500 p3     # centroid φ

ry p0 q0
rz p1 q0
ry p2 q1
rz p3 q1


# Controlled Swap between q0 and q1 using ancilla q2
# Since direct CSWAP might not be in your ALU, assume "cswap q2 q0 q1" is supported
cswap q2 q0 q1

# Interference
h q2

# Measure ancilla qubit to classical register p4
measure q2 p4

# Output measurement result
out p4
