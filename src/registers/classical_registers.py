# registers/classical_registers.py

from .registers_interface import RegisterInterface

class ClassicalRegisters(RegisterInterface):
    def __init__(self):
        self.regs = [0] * 8   # p0–p7
        self.pc = 0           # program counter
        self.b = False        # boolean flag

    def get(self, idx):
        if idx == "b":
            return self.b
        elif idx == "pc":
            return self.pc
        elif 0 <= idx < 8:
            return self.regs[idx]
        else:
            raise IndexError("Neplatný registr")

    def set(self, idx, value):
        if idx == "b":
            self.b = bool(value)
        elif idx == "pc":
            self.pc = int(value)
        elif 0 <= idx < 8:
            self.regs[idx] = value
        else:
            raise IndexError("Neplatný registr")

    def reset(self):
        self.regs = [0] * 8
        self.pc = 0
        self.b = False
