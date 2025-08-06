# quantum_bell.asm
# Create and measure a Bell state

h q0             # Hadamard on q0 
cx q0 q1         # CNOT q0 → q1 (entangle)
measure q0 p0    # measure q0 into p0
measure q1 p1    # measure q1 into p1

out p0           # OUT: 0 or 1
out p1           # OUT: should match p0
