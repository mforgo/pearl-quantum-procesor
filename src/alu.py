# src/alu.py

class ALU:
    def __init__(self, bit_width=4):
        self.bit_width = bit_width
        self.max_value = (1 << bit_width) - 1  # e.g., 0b1111 for 4 bits

    def _mask(self, value):
        """Ensure result stays within bit width via two's-complement wrap."""
        return value & self.max_value

    def add(self, a, b):
        """Return (a + b) mod 2^bit_width, plus carry flag."""
        result = a + b
        carry = 1 if result > self.max_value else 0
        return self._mask(result), carry

    def sub(self, a, b):
        """Return (a - b) mod 2^bit_width, plus borrow flag."""
        result = a - b
        borrow = 1 if result < 0 else 0
        return self._mask(result), borrow

    def bitwise_and(self, a, b):
        return a & b

    def bitwise_or(self, a, b):
        return a | b

    def bitwise_xor(self, a, b):
        return a ^ b

    def bitwise_not(self, a):
        return self._mask(~a)

    def inc(self, a):
        """Increment with wrap and carry."""
        return self.add(a, 1)

    def dec(self, a):
        """Decrement with wrap and borrow."""
        return self.sub(a, 1)
