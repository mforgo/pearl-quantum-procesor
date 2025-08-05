# src/alu/__init__.py

"""
Arithmetic Logic Unit (ALU) package.

This package provides both classical and quantum ALU implementations
following a common interface defined in alu_interface.py.
"""

from .alu_interface import ALUInterface
from .classical_alu import ClassicalALU
from .quantum_alu import QuantumALU

__all__ = [
    "ALUInterface",
    "ClassicalALU",
    "QuantumALU",
]
