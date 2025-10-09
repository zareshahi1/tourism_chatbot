# import pdfplumber
import fitz
from .base import BaseLoader

class PdfLoader(BaseLoader):
    def load(self, path: str = None, text: str = None) -> str:
        result = ""
        # with pdfplumber.open(path) as pdf:
        #     for page in pdf.pages:
        #         result += page.extract_text() + "\n"
        with fitz.open(path) as doc:
            for page in doc:
                result += page.get_text()
        return result
