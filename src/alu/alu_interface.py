# src/alu/alu_interface.py

from abc import ABC, abstractmethod

class ALUInterface(ABC):
    """Common interface for all ALU types."""

    @abstractmethod
    def add(self, a: int, b: int) -> (int, int):
        """Return (result, carry/overflow_flag)."""
        pass

    @abstractmethod
    def sub(self, a: int, b: int) -> (int, int):
        """Return (result, borrow/overflow_flag)."""
        pass

    @abstractmethod
    def bitwise_and(self, a: int, b: int) -> int:
        pass

    @abstractmethod
    def bitwise_or(self, a: int, b: int) -> int:
        pass

    @abstractmethod
    def bitwise_xor(self, a: int, b: int) -> int:
        pass

    @abstractmethod
    def bitwise_not(self, a: int) -> int:
        pass

    @abstractmethod
    def inc(self, a: int) -> (int, int):
        """Increment with wrap and carry."""
        pass

    @abstractmethod
    def dec(self, a: int) -> (int, int):
        """Decrement with wrap and borrow."""
        pass
