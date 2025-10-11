import os
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_community.vectorstores import FAISS

from utils.input_adapter import load_input
from utils.text_processing import TextProcessor
from dotenv import load_dotenv

load_dotenv()



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



class FAISSManager:
    def __init__(self, index_path="faiss_index"):
        self.index_path = "./db/" + index_path
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    def add_document(self, file_path: str = None, raw_text: str = None):
        pipeline = DocumentPipeline(file_path, raw_text)
        chunks, doc_id, filename = pipeline.run()

        if os.path.exists(self.index_path):
            vs = FAISS.load_local(self.index_path, self.embeddings, allow_dangerous_deserialization=True)

            for doc in vs.docstore._dict.values():
                if doc.metadata.get("filename") == filename:
                    print("%s file indexed before", filename)
                    return doc.metadata.get("doc_id"), filename

            vs.add_documents(chunks)
        else:
            vs = FAISS.from_documents(chunks, self.embeddings)

        vs.save_local(self.index_path)
        return doc_id, filename

    def list_documents(self):
        if not os.path.exists(self.index_path):
            return []
        vs = FAISS.load_local(self.index_path, self.embeddings, allow_dangerous_deserialization=True)
        docs_info = [
            {"doc_id": d.metadata.get("doc_id"), "filename": d.metadata.get("filename")}
            for d in vs.docstore._dict.values()
        ]
        return list({d["doc_id"]: d for d in docs_info if d["doc_id"]}.values())

    def remove_document(self, file_path: str):
        if not os.path.exists(self.index_path):
            return None

        filename = os.path.basename(file_path)

        vs = FAISS.load_local(
            self.index_path,
            self.embeddings,
            allow_dangerous_deserialization=True
        )

        keys_to_delete = [
            k for k, v in vs.docstore._dict.items()
            if v.metadata.get("filename") == filename
        ]

        if not keys_to_delete:
            return False

        remaining_docs = []
        for k, v in vs.docstore._dict.items():
            if k not in keys_to_delete:
                remaining_docs.append(v)

        if remaining_docs:
            new_vs = FAISS.from_documents(
                remaining_docs,
                self.embeddings
            )
            vs = new_vs
        else:
            vs = FAISS(
                embedding_function=self.embeddings,
                index=None,
                docstore=vs.docstore,
                index_to_docstore_id={}
            )

        vs.save_local(self.index_path)

        if os.path.exists(file_path):
            os.remove(file_path)

        return True

    def search(self, query: str, k=3, doc_id=None, filename=None):
        if not os.path.exists(self.index_path):
            return []
        vs = FAISS.load_local(self.index_path, self.embeddings, allow_dangerous_deserialization=True)

        filter_dict = {}
        if doc_id: filter_dict["doc_id"] = doc_id
        if filename: filter_dict["filename"] = filename

        return vs.similarity_search(query, k=k, filter=filter_dict if filter_dict else None)

