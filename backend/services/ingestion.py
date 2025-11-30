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
            if settings.HUGGINGFACEHUB_API_TOKEN:
                from langchain_huggingface import HuggingFaceEndpointEmbeddings
                print("DEBUG: Using HuggingFace Inference API for Embeddings (Low RAM)")
                self._embeddings = HuggingFaceEndpointEmbeddings(
                    model="sentence-transformers/all-MiniLM-L6-v2",
                    huggingfacehub_api_token=settings.HUGGINGFACEHUB_API_TOKEN
                )
            else:
                from langchain_huggingface import HuggingFaceEmbeddings
                print("DEBUG: Using Local HuggingFace Embeddings (High RAM)")
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

        print(f"DEBUG: Loading file {file_path} with extension {ext}")
        documents = loader.load()
        print(f"DEBUG: Loaded {len(documents)} documents")
        
        # Add metadata
        for doc in documents:
            doc.metadata["source"] = os.path.basename(file_path)

        # Split text
        print("DEBUG: Splitting text...")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        chunks = text_splitter.split_documents(documents)
        print(f"DEBUG: Split into {len(chunks)} chunks")

        # Store in Chroma
        print("DEBUG: Initializing ChromaDB...")
        # Note: Chroma automatically persists if persist_directory is set
        vectorstore = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings
        )
        print("DEBUG: Adding documents to ChromaDB...")
        vectorstore.add_documents(chunks)
        print("DEBUG: Successfully added to ChromaDB")
        
        return len(chunks)

    def clear_knowledge_base(self):
        if os.path.exists(self.persist_directory):
            shutil.rmtree(self.persist_directory)
        if os.path.exists(settings.UPLOAD_DIRECTORY):
            shutil.rmtree(settings.UPLOAD_DIRECTORY)
            os.makedirs(settings.UPLOAD_DIRECTORY, exist_ok=True)

ingestion_service = IngestionService()
