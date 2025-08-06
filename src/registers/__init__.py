# src/registers/__init__.py

# Pouze relativní importy
from .classical_registers import ClassicalRegisters
from .quantum_registers import QuantumRegisters
from .registers_interface import RegisterInterface

__all__ = [
    "RegisterInterface",
    "ClassicalRegisters",
    "QuantumRegisters",
]
