import uuid
import re
from langchain_core.documents import Document


class TextProcessor:
    HEADER_KEYWORDS = {'مقدمه', 'اهداف', 'الزامات', 'تعاریف', 'مسئولیت', 'دامنه', 'فصل', 'بخش', 'پیوست'}
    BULLET_PATTERN = re.compile(r'^\s*([*\-–—•]\s+|\d+[\.\)]\s+)')
    TABLE_PATTERN = re.compile(r'^\s*\|.*\|')

    @staticmethod
    def clean(text: str) -> str:
        """Persian Text Cleaning"""
        arabic_to_persian_map = {'ي': 'ی', 'ك': 'ک', 'ة': 'ه', 'ۀ': 'ه', 'ؤ': 'و', 'إ': 'ا', 'أ': 'ا', 'ء': ''}
        for a, p in arabic_to_persian_map.items():
            text = text.replace(a, p)
        text = re.sub(r'[\u064B-\u065F\u0670\u06D6-\u06ED]', '', text)
        text = re.sub(r'[^\u0600-\u06FF0-9\s\n|(){}،#*\-–—•.:]', '', text)
        return text.strip()

    @classmethod
    def is_heading(cls, line: str, min_words=1, max_words=5) -> bool:
        # remove unnecessary spaces
        line = line.strip()
        if not line:
            return False

        # calculate words
        words = line.split()
        n = len(words)

        if n < min_words or n > max_words:
            return False

        # check if this is not a paragraph or sentence
        if re.search(r'[.؟!؛:]$', line) or re.search(cls.BULLET_PATTERN, line) or re.search(cls.TABLE_PATTERN, line):
            return False

        return True

    @classmethod
    def add_headers(cls, text: str) -> str:
        """recognition and adding headers to simple texts"""
        result = []
        for line in text.split("\n"):
            stripped = line.strip()
            if not stripped:
                result.append("");
                continue
            if re.match(r'^\s*#{1,6}', stripped) or stripped.count('|') >= 2:
                result.append(stripped);
                continue
            if cls.is_heading(stripped):
                result.append("## " + stripped)
            else:
                result.append(stripped)
        return "\n".join(result)

    @classmethod
    def chunk(cls, split_text: list[Document]) -> list[Document]:
        """chunk heading split texts (by MarkdownHeaderTextSplitter function) to paragraphs/tables/bullets"""
        result, buffer, curr_type = [], [], None

        def flush(label, split):
            nonlocal buffer
            if buffer:
                metadata = split.metadata.copy()
                if label != 'paragraph':
                    metadata['chunk_type'] = label
                result.append(Document(metadata=metadata, page_content="\n".join(buffer)))
                buffer = []

        for split in split_text:
            for line in split.page_content.split("\n"):
                is_blank = not line.strip()
                if not is_blank and cls.BULLET_PATTERN.match(line.strip()):
                    new_type = 'bullet'
                elif not is_blank and (line.strip().count('|') >= 2 or cls.TABLE_PATTERN.match(line.strip())):
                    new_type = 'table'
                else:
                    new_type = 'paragraph'
                if new_type != curr_type:
                    flush(curr_type if curr_type else 'paragraph', split)
                    curr_type = new_type
                if new_type == 'paragraph':
                    buffer.append(line.rstrip())
                elif not is_blank:
                    buffer.append(line.strip())
            flush(curr_type if curr_type else 'paragraph', split)
        return result

    @staticmethod
    def attach_metadata(chunks: list[Document], doc_id: str, filename: str):
        """add (doc_id and filename) metadata to chunks"""
        for c in chunks:
            c.metadata["doc_id"] = doc_id
            c.metadata["filename"] = filename
        return chunks
