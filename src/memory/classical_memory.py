# memory/classical_memory.py

from collections import deque
from .memory_interface import MemoryInterface

class ClassicalMemory(MemoryInterface):
    def __init__(self, max_size=1024):
        self.max_size = max_size
        self.memory = dict()
    
    def read(self, address):
        return self.memory.get(address, 0)

    def write(self, address, value):
        if 0 <= address < self.max_size:
            self.memory[address] = value
        else:
            raise IndexError("Memory write out of range")
    
    def reset(self):
        self.memory = dict()
