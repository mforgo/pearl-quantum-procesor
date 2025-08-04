# registers/quantum_registers.py
from registers_interface import RegisterInterface

class QuantumRegisters(RegisterInterface):
    def __init__(self, num_qubits=8):
        # Import třeba až při skutečné simulaci: např. z qiskit
        self.num_qubits = num_qubits
        self.quantum_state = None  # Lze propojit s Qiskit, Cirq atd.
        self.init_state()

    def init_state(self):
        from qiskit import QuantumRegister, QuantumCircuit
        self.qr = QuantumRegister(self.num_qubits)
        self.circuit = QuantumCircuit(self.qr)

    def get(self, idx):
        # Vrací stav qubitu idx, placeholder (skutečný stav získáte až měřením)
        return f"qubit_{idx}"

    def set(self, idx, value):
        # Pro reálné použití nastavujete stav qubitu (FALSE/TRUE nebo operace)
        pass

    def reset(self):
        self.init_state()
