# Memory Subsystem of Pearl Quantum Processor

This document describes the memory subsystem implemented in the Pearl Quantum Processor, featuring both classical and quantum memory modules with a unified interface. It includes design, usage, and implementation details for developers and users of the system.

---

## Overview

Memory is a critical component of the Pearl Quantum Processor, providing storage for classical data and quantum states as required by quantum and classical instructions.

- **Classical Memory:** Stores classical data values at addressable locations.
- **Quantum Memory:** (Placeholder) Intended for managing quantum data storage, including qubit states — typically integrated with `QuantumRegisters`.

Both memory types conform to the common `MemoryInterface` for interoperability and modular design.

---

## Memory Interface

### Abstraction

The `MemoryInterface` is an abstract base class declaring essential methods to be implemented by any memory type.

#### Interface Methods

| Method    | Description                          |
|-----------|------------------------------------|
| `read(address)`  | Read value from the given address |
| `write(address, value)` | Write the given value to address  |
| `reset()`       | Reset memory contents to default   |

This interface enforces consistent API across classical and quantum memories.

---

## Classical Memory

### Class: `ClassicalMemory`

A dictionary-backed memory store with configurable maximum size.

### Key Features

- Supports random access reads and writes.
- Bounds checking for memory writes.
- Reset method clears the memory.

### API

```

class ClassicalMemory(MemoryInterface):
def __init__(self, max_size=1024):
self.max_size = max_size
self.memory = dict()

    def read(self, address):
        # Returns 0 if address not set
        return self.memory.get(address, 0)
    
    def write(self, address, value):
        if 0 <= address < self.max_size:
            self.memory[address] = value
        else:
            raise IndexError("Memory write out of range")
    
    def reset(self):
        self.memory = dict()
    ```

### Usage

```

mem = ClassicalMemory(max_size=2048)
mem.write(10, 42)
val = mem.read(10)  \# val == 42
mem.reset()

```

---

## Quantum Memory (Placeholder)

### Class: `QuantumMemory`

Currently a skeleton implementation anticipating future integration with quantum registers.

### Design Intent

- To provide `read`, `write`, and `reset` operations on quantum states.
- Typically, quantum memory operations involve state preparation, measurement, and qubit resetting.
- Implementation awaits tight coupling with `QuantumRegisters` and quantum state simulation backend.

### API (Stub)

```

class QuantumMemory(MemoryInterface):
def __init__(self):
self.qubits = None  \# Placeholder for quantum register instance

    def read(self, address):
        # Measurement or readout from quantum memory
        pass
    
    def write(self, address, value):
        # State preparation or quantum data write
        pass
    
    def reset(self):
        # Reset quantum memory states
        pass
    ```

Currently, these methods are unimplemented and will raise `NotImplementedError` or behave as no-ops until fully developed.

---

## Package Initialization (`memory/__init__.py`)

The `memory` package exports interfaces and implementations:

```

from .memory_interface import MemoryInterface
from .classical_memory import ClassicalMemory
from .quantum_memory import QuantumMemory

__all__ = [
"MemoryInterface",
"ClassicalMemory",
"QuantumMemory",
]

```

This enables clients to import memory types directly:

```

from src.memory import ClassicalMemory, QuantumMemory

```

---

## Summary

| Component        | Status       | Key Points                       |
|------------------|--------------|--------------------------------|
| `MemoryInterface`  | Implemented  | Abstract base class defining API |
| `ClassicalMemory`  | Fully implemented | Backed by dict, with bounds check and reset |
| `QuantumMemory`    | Stub / Placeholder | Awaiting integration and quantum backend support |

The modular design allows your Pearl Quantum Processor to extend quantum memory management without affecting classical memory usage and vice versa.

---

## References

- `src/memory/memory_interface.py`  
- `src/memory/classical_memory.py`  
- `src/memory/quantum_memory.py`  
- `src/memory/__init__.py`

---

