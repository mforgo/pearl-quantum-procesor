# src/alu/quantum_alu.py

from .alu_interface import ALUInterface
import numpy as np

class QuantumALU(ALUInterface):
    def __init__(self, quantum_registers):
        self.qregs = quantum_registers
        self.num_qubits = quantum_registers.num_qubits
    
    # === JEDNOQUBITOVÉ BRÁNY ===
    
    def x_gate(self, qubit):
        """Pauli-X (NOT) brána"""
        state = self.qregs.get_full_state()
        new_state = np.zeros_like(state)
        
        for i in range(2**self.num_qubits):
            # Flip bit na pozici qubit
            flipped = i ^ (1 << qubit)
            new_state[flipped] = state[i]
        
        self.qregs.set_full_state(new_state)
    
    def y_gate(self, qubit):
        """Pauli-Y brána"""
        state = self.qregs.get_full_state()
        new_state = np.zeros_like(state)
        
        for i in range(2**self.num_qubits):
            flipped = i ^ (1 << qubit)
            if (i >> qubit) & 1:  # |1⟩ -> -i|0⟩
                new_state[flipped] = -1j * state[i]
            else:  # |0⟩ -> i|1⟩
                new_state[flipped] = 1j * state[i]
        
        self.qregs.set_full_state(new_state)
    
    def z_gate(self, qubit):
        """Pauli-Z brána"""
        state = self.qregs.get_full_state()
        new_state = state.copy()
        
        for i in range(2**self.num_qubits):
            if (i >> qubit) & 1:  # |1⟩ -> -|1⟩
                new_state[i] = -state[i]
        
        self.qregs.set_full_state(new_state)
    
    def h_gate(self, qubit):
        """Hadamard brána - vytvoří superpozici"""
        state = self.qregs.get_full_state()
        new_state = np.zeros_like(state)
        sqrt2 = 1.0 / np.sqrt(2)
        
        for i in range(2**self.num_qubits):
            i0 = i & ~(1 << qubit)  # Set qubit to 0
            i1 = i | (1 << qubit)   # Set qubit to 1
            
            if (i >> qubit) & 1 == 0:  # Current state has qubit=0
                new_state[i0] += sqrt2 * state[i]
                new_state[i1] += sqrt2 * state[i]
            else:  # Current state has qubit=1
                new_state[i0] += sqrt2 * state[i]
                new_state[i1] -= sqrt2 * state[i]
        
        self.qregs.set_full_state(new_state)
    
    def s_gate(self, qubit):
        """S brána (fázová brána π/2)"""
        state = self.qregs.get_full_state()
        new_state = state.copy()
        
        for i in range(2**self.num_qubits):
            if (i >> qubit) & 1:  # |1⟩ -> i|1⟩
                new_state[i] = 1j * state[i]
        
        self.qregs.set_full_state(new_state)
    
    def t_gate(self, qubit):
        """T brána (fázová brána π/4)"""
        state = self.qregs.get_full_state()
        new_state = state.copy()
        phase = np.exp(1j * np.pi / 4)
        
        for i in range(2**self.num_qubits):
            if (i >> qubit) & 1:  # |1⟩ -> e^(iπ/4)|1⟩
                new_state[i] = phase * state[i]
        
        self.qregs.set_full_state(new_state)
    
    def rx_gate(self, qubit, theta):
        """Rotace kolem X-osy o úhel theta"""
        state = self.qregs.get_full_state()
        new_state = np.zeros_like(state)
        
        cos_half = np.cos(theta / 2)
        sin_half = -1j * np.sin(theta / 2)
        
        for i in range(2**self.num_qubits):
            i0 = i & ~(1 << qubit)
            i1 = i | (1 << qubit)
            
            if (i >> qubit) & 1 == 0:
                new_state[i0] += cos_half * state[i]
                new_state[i1] += sin_half * state[i]
            else:
                new_state[i0] += sin_half * state[i]
                new_state[i1] += cos_half * state[i]
        
        self.qregs.set_full_state(new_state)
    
    def ry_gate(self, qubit, theta):
        """Rotace kolem Y-osy o úhel theta"""
        state = self.qregs.get_full_state()
        new_state = np.zeros_like(state)
        
        cos_half = np.cos(theta / 2)
        sin_half = np.sin(theta / 2)
        
        for i in range(2**self.num_qubits):
            i0 = i & ~(1 << qubit)
            i1 = i | (1 << qubit)
            
            if (i >> qubit) & 1 == 0:
                new_state[i0] += cos_half * state[i]
                new_state[i1] += sin_half * state[i]
            else:
                new_state[i0] += -sin_half * state[i]
                new_state[i1] += cos_half * state[i]
        
        self.qregs.set_full_state(new_state)
    
    def rz_gate(self, qubit, theta):
        """Rotace kolem Z-osy o úhel theta"""
        state = self.qregs.get_full_state()
        new_state = state.copy()
        
        phase_0 = np.exp(-1j * theta / 2)
        phase_1 = np.exp(1j * theta / 2)
        
        for i in range(2**self.num_qubits):
            if (i >> qubit) & 1 == 0:
                new_state[i] = phase_0 * state[i]
            else:
                new_state[i] = phase_1 * state[i]
        
        self.qregs.set_full_state(new_state)
    
    # === DVOUQUBITOVÉ BRÁNY ===
    
    def cnot_gate(self, control, target):
        """CNOT brána"""
        state = self.qregs.get_full_state()
        new_state = np.zeros_like(state)
        
        for i in range(2**self.num_qubits):
            if (i >> control) & 1:  # Control je |1⟩
                # Flip target bit
                flipped = i ^ (1 << target)
                new_state[flipped] = state[i]
            else:
                new_state[i] = state[i]
        
        self.qregs.set_full_state(new_state)
    
    def cz_gate(self, control, target):
        """Controlled-Z brána"""
        state = self.qregs.get_full_state()
        new_state = state.copy()
        
        for i in range(2**self.num_qubits):
            if ((i >> control) & 1) and ((i >> target) & 1):
                new_state[i] = -state[i]
        
        self.qregs.set_full_state(new_state)
    
    def cy_gate(self, control, target):
        """Controlled-Y brána"""
        state = self.qregs.get_full_state()
        new_state = np.zeros_like(state)
        
        for i in range(2**self.num_qubits):
            if (i >> control) & 1:  # Control je |1⟩
                # Apply Y gate to target
                flipped = i ^ (1 << target)
                if (i >> target) & 1:  # Target |1⟩ -> -i|0⟩
                    new_state[flipped] = -1j * state[i]
                else:  # Target |0⟩ -> i|1⟩
                    new_state[flipped] = 1j * state[i]
            else:
                new_state[i] = state[i]
        
        self.qregs.set_full_state(new_state)
    
    def ccx_gate(self, control1, control2, target):
        """Toffoli (CCX) brána"""
        state = self.qregs.get_full_state()
        new_state = np.zeros_like(state)
        
        for i in range(2**self.num_qubits):
            if ((i >> control1) & 1) and ((i >> control2) & 1):
                # Both controls are |1⟩, flip target
                flipped = i ^ (1 << target)
                new_state[flipped] = state[i]
            else:
                new_state[i] = state[i]
        
        self.qregs.set_full_state(new_state)
    
    # === KVANTOVÉ ALGORITMY ===
    
    def create_bell_state(self, q1, q2):
        """Vytvoří Bell state (maximálně provázaný stav)"""
        self.h_gate(q1)
        self.cnot_gate(q1, q2)
    
    def quantum_fourier_transform(self, qubits):
        """Kvantová Fourierova transformace"""
        n = len(qubits)
        for j in range(n):
            self.h_gate(qubits[j])
            for k in range(j+1, n):
                # Controlled rotation
                angle = np.pi / (2**(k-j))
                self.controlled_rz_gate(qubits[k], qubits[j], angle)
        
        # Reverse order
        for i in range(n//2):
            self.swap_gate(qubits[i], qubits[n-1-i])
    
    def controlled_rz_gate(self, control, target, angle):
        """Controlled RZ brána"""
        state = self.qregs.get_full_state()
        new_state = state.copy()
        
        phase = np.exp(1j * angle)
        
        for i in range(2**self.num_qubits):
            if ((i >> control) & 1) and ((i >> target) & 1):
                new_state[i] = phase * state[i]
        
        self.qregs.set_full_state(new_state)
    
    def swap_gate(self, q1, q2):
        """SWAP brána"""
        self.cnot_gate(q1, q2)
        self.cnot_gate(q2, q1)
        self.cnot_gate(q1, q2)
    
    # === KLASICKÉ FALLBACKY (pro kompatibilitu s ALU interface) ===
    
    def add(self, a, b):
        return a + b, 0
    
    def sub(self, a, b):
        return a - b, 0
    
    def bitwise_and(self, a, b):
        return a & b
    
    def bitwise_or(self, a, b):
        return a | b
    
    def bitwise_xor(self, a, b):
        return a ^ b
    
    def bitwise_not(self, a):
        return ~a
    
    def inc(self, a):
        return self.add(a, 1)
    
    def dec(self, a):
        return self.sub(a, 1)
