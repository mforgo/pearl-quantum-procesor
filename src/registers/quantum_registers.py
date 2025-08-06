# src/registers/quantum_registers.py

from .registers_interface import RegisterInterface
import numpy as np

class QuantumRegisters(RegisterInterface):
    def __init__(self, num_qubits=8):
        self.num_qubits = num_qubits
        self.reset()
    
    def reset(self):
        """Reset všech qubitů do |00...0⟩"""
        self.state = np.zeros(2**self.num_qubits, dtype=complex)
        self.state[0] = 1.0  # |00...0⟩
    
    def get(self, idx):
        """Vrátí popis stavu qubitu (nelze přímo číst kvantový stav)"""
        return f"qubit_{idx}"
    
    def set(self, idx, value):
        """Nastavení qubitu do základního stavu"""
        if value == 0:
            self._project_to_zero(idx)
        elif value == 1:
            self._project_to_one(idx)
    
    def get_full_state(self):
        """Vrátí celý kvantový stav (pro debugging)"""
        return self.state.copy()
    
    def set_full_state(self, new_state):
        """Nastaví nový kvantový stav (používá ALU)"""
        self.state = new_state.copy()
    
    def get_probability(self, qubit, outcome):
        """Pravděpodobnost měření konkrétního qubitu"""
        prob = 0.0
        for i in range(2**self.num_qubits):
            if (i >> qubit) & 1 == outcome:
                prob += abs(self.state[i])**2
        return prob
    
    def measure(self, qubit):
        """Změří qubit a vrátí 0 nebo 1"""
        prob_0 = self.get_probability(qubit, 0)
        outcome = 0 if np.random.random() < prob_0 else 1
        self._collapse_to_outcome(qubit, outcome)
        return outcome
    
    def _collapse_to_outcome(self, qubit, outcome):
        """Kolaps vlnové funkce po měření"""
        new_state = np.zeros_like(self.state)
        norm = 0.0
        
        for i in range(2**self.num_qubits):
            if (i >> qubit) & 1 == outcome:
                new_state[i] = self.state[i]
                norm += abs(self.state[i])**2
        
        if norm > 0:
            self.state = new_state / np.sqrt(norm)
    
    def _project_to_zero(self, qubit):
        """Projekce qubitu do |0⟩"""
        self._collapse_to_outcome(qubit, 0)
    
    def _project_to_one(self, qubit):
        """Projekce qubitu do |1⟩"""
        self._collapse_to_outcome(qubit, 1)
