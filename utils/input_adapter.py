import os
from .loaders.docx_loader import DocxLoader
from .loaders.pdf_loader import PdfLoader
from .loaders.txt_loader import TxtLoader
from .loaders.raw_loader import RawLoader
from .loaders.md_loader import MarkdownLoader
from .loaders.html_loader import HtmlLoader

LOADERS = {
    ".docx": DocxLoader(),
    ".pdf": PdfLoader(),
    ".txt": TxtLoader(),
    ".md": MarkdownLoader(),
    ".html": HtmlLoader(),
    ".htm": HtmlLoader(),
    "raw": RawLoader()
}


def load_input(file_path: str = None, raw_text: str = None) -> str:
    if raw_text:
        return LOADERS["raw"].load(text=raw_text)

    if not file_path:
        raise ValueError("file path or raw text required")

    ext = os.path.splitext(file_path)[1].lower()
    if ext in LOADERS:
        return LOADERS[ext].load(path=file_path)
    else:
        raise ValueError(f"{ext} is not supported format")
