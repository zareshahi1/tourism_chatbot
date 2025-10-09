from abc import ABC, abstractmethod

class BaseLoader(ABC):
    @abstractmethod
    def load(self, path: str = None, text: str = None) -> str:
        pass
