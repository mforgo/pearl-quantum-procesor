# registers/register_interface.py

from abc import ABC, abstractmethod

class RegisterInterface(ABC):
    @abstractmethod
    def get(self, idx):
        pass

    @abstractmethod
    def set(self, idx, value):
        pass

    @abstractmethod
    def reset(self):
        pass
