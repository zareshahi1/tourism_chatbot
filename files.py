import os, uuid
from langchain_openai import OpenAIEmbeddings
from utils.input_adapter import load_input
from utils.text_processing import TextProcessor
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain.vectorstores.chroma import Chroma


class DocumentPipeline:
    def __init__(self, file_path: str = None, raw_text: str = None):
        self.file_path = file_path
        self.raw_text = raw_text
        self.filename = os.path.basename(file_path) if file_path else "raw_text"
        self.doc_id = self.filename + "_" + str(uuid.uuid4())

    def run(self):
        raw_text = load_input(self.file_path, self.raw_text)
        cleaned = TextProcessor.clean(raw_text)
        inferred = TextProcessor.add_headers(cleaned)
        splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=[("#", "Header1"), ("##", "Header2"), ("###", "Header3")],
            strip_headers=True
        )
        docs = splitter.split_text(inferred)
        chunks = TextProcessor.chunk(docs)
        chunks = TextProcessor.attach_metadata(chunks, self.doc_id, self.filename)

        return chunks, self.doc_id, self.filename


class ChromaManager:
    def __init__(self, chroma_path: str = "db"):
        self.embedding = OpenAIEmbeddings(model="text-embedding-3-small")
        self.db = Chroma(persist_directory=chroma_path, embedding_function=self.embedding)

    def add_document(self, file_path: str = None, raw_text: str = None):
        pipeline = DocumentPipeline(file_path, raw_text)
        chunks, doc_id, filename = pipeline.run()

        # Add or Update the documents.
        existing_items = self.db.get(include=[])  # IDs are always included by default
        existing_ids = set(existing_items["ids"])
        print(f"Number of existing documents in DB: {len(existing_ids)}")

        # Only add documents that don't exist in the DB.
        new_chunks = []
        for chunk in chunks_with_ids:
            if chunk.metadata["id"] not in existing_ids:
                new_chunks.append(chunk)

        if len(new_chunks):
            print(f"👉 Adding new documents: {len(new_chunks)}")
            new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
            db.add_documents(new_chunks, ids=new_chunk_ids)
            db.persist()
        else:
            print("✅ No new documents to add")
