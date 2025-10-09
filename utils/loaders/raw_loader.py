from .base import BaseLoader

class RawLoader(BaseLoader):
    def load(self, path: str = None, text: str = None) -> str:
        return text
