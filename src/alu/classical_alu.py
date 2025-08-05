# src/alu/classical_alu.py

from .alu_interface.py import ALUInterface

class ClassicalALU(ALUInterface):
    def __init__(self, bit_width=4):
        self.bit_width = bit_width
        self.max_value = (1 << bit_width) - 1

    def _mask(self, value: int) -> int:
        return value & self.max_value

    def add(self, a: int, b: int) -> (int, int):
        result = a + b
        carry = 1 if result > self.max_value else 0
        return self._mask(result), carry

    def sub(self, a: int, b: int) -> (int, int):
        result = a - b
        borrow = 1 if result < 0 else 0
        return self._mask(result), borrow

    def bitwise_and(self, a: int, b: int) -> int:
        return a & b

    def bitwise_or(self, a: int, b: int) -> int:
        return a | b

    def bitwise_xor(self, a: int, b: int) -> int:
        return a ^ b

    def bitwise_not(self, a: int) -> int:
        return self._mask(~a)

    def inc(self, a: int) -> (int, int):
        return self.add(a, 1)

    def dec(self, a: int) -> (int, int):
        return self.sub(a, 1)
