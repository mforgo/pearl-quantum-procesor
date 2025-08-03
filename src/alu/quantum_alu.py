# src/alu.py

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, Aer
from qiskit.circuit.library import DraperQFTAdder

class QuantumALU:
    def __init__(self, num_qubits: int):
        """
        A QFT-based adder ALU performing addition modulo 2**num_qubits.
        Uses Draper’s QFT adder under the hood.
        """
        if num_qubits < 1:
            raise ValueError("num_qubits must be ≥1")
        self.n = num_qubits
        # Prepare registers: two inputs (a,b) and classical bits for measurement.
        self.qr_a = QuantumRegister(self.n, name="a")
        self.qr_b = QuantumRegister(self.n, name="b")
        self.cr_a = ClassicalRegister(self.n, name="ca")
        self.cr_b = ClassicalRegister(self.n, name="cb")
        # Build a reusable QFT adder gate
        self.adder = DraperQFTAdder(self.n, kind="fixed", name=f"qft_adder_{self.n}")

    def add(self, a_val: int, b_val: int) -> int:
        """
        Perform (a_val + b_val) mod 2**n on a quantum circuit and return the result.
        """
        # Build circuit
        qc = QuantumCircuit(self.qr_a, self.qr_b, self.cr_a, self.cr_b)
        # Initialize |a> and |b>
        for i in range(self.n):
            if (a_val >> i) & 1:
                qc.x(self.qr_a[i])
            if (b_val >> i) & 1:
                qc.x(self.qr_b[i])
        # Apply QFT adder: adds register a into b in Fourier space
        qc.append(self.adder.to_gate(), self.qr_a[:] + self.qr_b[:])
        # Measure resulting b register
        qc.measure(self.qr_b, self.cr_b)
        # Execute
        backend = Aer.get_backend("aer_simulator")
        job = execute(qc, backend=backend, shots=1)
        result = job.result().get_counts()
        # Extract measured integer value of b
        bitstr = list(result.keys())[0][: self.n]
        return int(bitstr[::-1], 2)  # reverse for LSB→MSB

# Example usage (in your processor or test script):
if __name__ == "__main__":
    alu = QuantumALU(num_qubits=3)
    res = alu.add(5, 3)
    print(f"Quantum ADD 5 + 3 mod 8 = {res}")  # Expect 0 (8 mod 8)
