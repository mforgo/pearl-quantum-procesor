# programs/hybrid_demo.asm
# Hybrid Quantum-Classical Test Program
# Creates Bell pairs, measures them, and performs classical processing

# === Classical Setup ===
mov 0 p0         # Initialize counter
mov 10 p1        # Number of experiments

# === Main Loop ===
# Label: loop (instruction 2)
cmp p0 p1        # Compare counter with limit
jmpif 15         # Jump to end if p0 >= p1

# === Quantum Bell State Creation ===
reset q0         # Reset qubits to |0⟩
reset q1
h q0             # Create superposition on q0
cx q0 q1         # Entangle q0 and q1 (Bell state)

# === Quantum Measurements ===
measure q0 p2    # Measure q0 → p2
measure q1 p3    # Measure q1 → p3

# === Classical Processing ===
eqq p2 p3        # Check if measurements are equal
and 1            # AND with 1 (always true)
jmpif 12         # If equal, increment success counter
jmp 13           # Skip increment

# Success case (instruction 12)
add p4 1         # Increment success counter (p4)

# Continue loop (instruction 13)
add p0 1         # Increment loop counter
jmp 2            # Jump back to loop start

# === End of Program (instruction 15) ===
out p0           # Output total experiments
out p4           # Output successful correlations

# === Calculate Success Percentage ===
mul p4 100       # p4 = successes * 100
dvd p4 p1        # p4 = (successes * 100) / total
out p4           # Output success percentage

# === Memory Test ===
push p4          # Push success rate to queue
mov 42 p5        # Test value
push p5          # Push test value
pop p6           # Pop into p6 (should be 42)
pop p7           # Pop into p7 (should be success rate)
out p6           # Should output 42
out p7           # Should output success rate again
