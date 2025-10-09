from bs4 import BeautifulSoup
from .base import BaseLoader

class HtmlLoader(BaseLoader):
    def load(self, path: str = None, text: str = None) -> str:
        """استخراج متن از فایل یا رشته HTML"""
        if path:
            with open(path, "r", encoding="utf-8") as f:
                html = f.read()
        else:
            html = text

        soup = BeautifulSoup(html, "html.parser")

        # حذف اسکریپت‌ها و استایل‌ها
        for tag in soup(["script", "style", "noscript"]):
            tag.extract()

        # گرفتن متن تمیز
        return soup.get_text(separator="\n")
