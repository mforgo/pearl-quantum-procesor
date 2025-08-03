# src/alu/quantum_alu.py

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, Aer
from qiskit.circuit.library import DraperQFTAdder
from src.alu.alu_interface import ALUInterface

class QuantumALU(ALUInterface):
    def __init__(self, num_qubits: int):
        if num_qubits < 1:
            raise ValueError("num_qubits must be ≥1")
        self.n = num_qubits
        self.qr_a = QuantumRegister(self.n, "a")
        self.qr_b = QuantumRegister(self.n, "b")
        self.cr_b = ClassicalRegister(self.n, "cb")
        self.adder = DraperQFTAdder(self.n, kind="fixed")

    def add(self, a: int, b: int) -> (int, int):
        qc = QuantumCircuit(self.qr_a, self.qr_b, self.cr_b)
        for i in range(self.n):
            if (a >> i) & 1: qc.x(self.qr_a[i])
            if (b >> i) & 1: qc.x(self.qr_b[i])
        qc.append(self.adder.to_gate(), self.qr_a[:] + self.qr_b[:])
        qc.measure(self.qr_b, self.cr_b)
        backend = Aer.get_backend("aer_simulator")
        job = execute(qc, backend, shots=1)
        count = job.result().get_counts()
        bitstr = list(count.keys())[0][: self.n][::-1]
        result = int(bitstr, 2)
        carry = 1 if result < b else 0
        return result, carry

    def sub(self, a: int, b: int) -> (int, int):
        # Implement as a + two's complement of b
        mask = (1 << self.n) - 1
        b_comp = (~b + 1) & mask
        return self.add(a, b_comp)

    def bitwise_and(self, a: int, b: int) -> int:
        # Classical fallback
        return a & b

    def bitwise_or(self, a: int, b: int) -> int:
        return a | b

    def bitwise_xor(self, a: int, b: int) -> int:
        return a ^ b

    def bitwise_not(self, a: int) -> int:
        mask = (1 << self.n) - 1
        return (~a) & mask

    def inc(self, a: int) -> (int, int):
        return self.add(a, 1)

    def dec(self, a: int) -> (int, int):
        return self.sub(a, 1)
