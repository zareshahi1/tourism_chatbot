from .base import BaseLoader
from ..docx2md import docx_to_markdown

class DocxLoader(BaseLoader):
    def load(self, path: str = None, text: str = None) -> str:
        return docx_to_markdown(path)
