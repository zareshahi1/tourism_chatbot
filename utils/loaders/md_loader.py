from .base import BaseLoader

class MarkdownLoader(BaseLoader):
    def load(self, path: str = None, text: str = None) -> str:
        """خواندن فایل Markdown و برگرداندن متن"""
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
