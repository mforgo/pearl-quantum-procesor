# src/memory/__init__.py

"""
Memory management package.

This package provides both classical and quantum memory implementations
with a common interface for the Pearl Quantum Processor.
"""

from .memory_interface import MemoryInterface
from .classical_memory import ClassicalMemory
from .quantum_memory import QuantumMemory

__all__ = [
    "MemoryInterface",
    "ClassicalMemory", 
    "QuantumMemory",
]
