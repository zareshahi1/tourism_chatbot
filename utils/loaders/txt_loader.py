from .base import BaseLoader

class TxtLoader(BaseLoader):
    def load(self, path: str = None, text: str = None) -> str:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
