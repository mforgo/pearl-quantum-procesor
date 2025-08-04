# memory/classical_memory.py

from collections import deque
from .memory_interface import MemoryInterface

class ClassicalMemory(MemoryInterface):
    def __init__(self, max_size=1024):
        self.max_size = max_size
        self.memory = deque(maxlen=max_size)  # FIFO queue with max length
        self.reset()

    def read(self):
        # Address is position in queue, 0 = front
        return self.memory.popleft() if self.memory else None

    def write(self, address, value):
        # Only allow writing to next position if address == current size (append)
        if address == len(self.memory) and len(self.memory) < self.max_size:
            self.memory.append(value)
        elif 0 <= address < len(self.memory):
            self.memory[address] = value
        else:
            raise IndexError("Memory write out of range")

    def reset(self):
        self.memory.clear()
