# import pdfplumber
from pypdf import PdfReader
from .base import BaseLoader

class PdfLoader(BaseLoader):
    def load(self, path: str = None, text: str = None) -> str:
        result = ""
        reader = PdfReader("example.pdf")
        for page in reader.pages:
            result += page.extract_text()
        return result
