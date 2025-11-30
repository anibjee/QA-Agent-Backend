import os
from typing import List
from backend.core.config import settings
import shutil

class IngestionService:
    def __init__(self):
        self._embeddings = None
        self.persist_directory = settings.CHROMA_PERSIST_DIRECTORY
        
        # Ensure upload directory exists
        os.makedirs(settings.UPLOAD_DIRECTORY, exist_ok=True)

    @property
    def embeddings(self):
        if self._embeddings is None:
            from langchain_huggingface import HuggingFaceEmbeddings
            self._embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        return self._embeddings

    def save_file(self, file, filename: str) -> str:
        file_path = os.path.join(settings.UPLOAD_DIRECTORY, filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return file_path

    def process_document(self, file_path: str):
        from langchain_community.document_loaders import TextLoader, UnstructuredMarkdownLoader, BSHTMLLoader
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        from langchain_chroma import Chroma

        # Determine loader based on extension
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext == ".md":
            # Using TextLoader for simplicity and reliability with markdown
            loader = TextLoader(file_path, encoding='utf-8')
        elif ext == ".txt":
            loader = TextLoader(file_path, encoding='utf-8')
        elif ext == ".html":
            loader = BSHTMLLoader(file_path, open_encoding='utf-8')
        elif ext == ".json":
            loader = TextLoader(file_path, encoding='utf-8')
        else:
            # Fallback for other text based files
            loader = TextLoader(file_path, encoding='utf-8')

        documents = loader.load()
        
        # Add metadata
        for doc in documents:
            doc.metadata["source"] = os.path.basename(file_path)

        # Split text
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        chunks = text_splitter.split_documents(documents)

        # Store in Chroma
        # Note: Chroma automatically persists if persist_directory is set
        vectorstore = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings
        )
        vectorstore.add_documents(chunks)
        
        return len(chunks)

    def clear_knowledge_base(self):
        if os.path.exists(self.persist_directory):
            shutil.rmtree(self.persist_directory)
        if os.path.exists(settings.UPLOAD_DIRECTORY):
            shutil.rmtree(settings.UPLOAD_DIRECTORY)
            os.makedirs(settings.UPLOAD_DIRECTORY, exist_ok=True)

ingestion_service = IngestionService()
