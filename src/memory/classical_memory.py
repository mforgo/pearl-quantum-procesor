from collections import deque
from .memory_interface import MemoryInterface

class ClassicalMemory(MemoryInterface):
    def __init__(self, max_size=1024):
        self.max_size = max_size
        self.memory = dict()
        self.queue = deque()

    def read(self, address):
        return self.memory.get(address, 0)

    def write(self, address, value):
        if 0 <= address < self.max_size:
            self.memory[address] = value
        else:
            raise IndexError("Memory write out of range")

    def reset(self):
        self.memory = dict()
        self.queue.clear()

    def push(self, value):
        self.queue.append(value)
        # Optionally keep in sync with the dict for status
        self.memory['_queue'] = list(self.queue)

    def pop(self):
        if self.queue:
            value = self.queue.pop()
            self.memory['_queue'] = list(self.queue)
            return value
        else:
            raise IndexError("Pop from empty queue")

    def popleft(self):
        if self.queue:
            value = self.queue.popleft()
            self.memory['_queue'] = list(self.queue)
            return value
        else:
            raise IndexError("Popleft from empty queue")

    def dump(self):
        """For status(), returns dict containing both memory and queue."""
        mem_copy = dict(self.memory)
        mem_copy['_queue'] = list(self.queue)
        return mem_copy
