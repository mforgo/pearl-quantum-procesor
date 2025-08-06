# classical_arith.asm
# Compute (10 – 4) × 2 and store in memory[0]

mov 10 p0         # p0 ← 10
mov 4  p1         # p1 ← 4
sub p0 p1         # p0 ← p0 – p1    ; 6
mov p0 h0         # memory[0] ← 6
mov 2  p2         # p2 ← 2
mul p0 p2         # p0 ← p0 × p2    ; 12
mov p0 h1         # memory[1] ← 12

# Read back and output
mov h0 p3         # p3 ← memory[0]
out p3            # OUT: 6
mov h1 p4         # p4 ← memory[1]
out p4            # OUT: 12
