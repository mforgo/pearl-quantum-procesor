# memory/memory_interface.py

from abc import ABC, abstractmethod

class MemoryInterface(ABC):
    @abstractmethod
    def read(self, address):
        pass

    @abstractmethod
    def write(self, address, value):
        pass

    @abstractmethod
    def reset(self):
        pass
