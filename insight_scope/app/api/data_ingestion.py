"""
Data ingestion module for processing and indexing documents.
"""
from typing import List, Dict, Any, Optional
import os
from pathlib import Path

from insight_scope.utils.preprocessing.document_loader import DocumentLoader
from insight_scope.models.embeddings.embedding_manager import EmbeddingManager
from insight_scope.models.embeddings.vector_store import VectorStore
from insight_scope.utils.mongodb_connector import MongoDBConnector
from insight_scope.config.config import RAW_DATA_DIR

class DataIngestionPipeline:
    """Pipeline for ingesting and processing documents."""
    
    def __init__(self):
        """Initialize the data ingestion pipeline."""
        self.document_loader = DocumentLoader()
        self.embedding_manager = EmbeddingManager()
        self.vector_store = VectorStore()
        self.mongodb = MongoDBConnector()
    
    def process_file(self, file_path: str) -> Dict[str, Any]:
        """
        Process a single file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Processing results
        """
        # Check file type and load document
        if file_path.endswith(".pdf"):
            chunks = self.document_loader.load_pdf(file_path)
        elif file_path.endswith(".txt"):
            chunks = self.document_loader.load_text(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_path}")
        
        if not chunks:
            return {"status": "error", "message": "No content extracted from file", "file": file_path}
        
        # Generate embeddings
        texts = [chunk["text"] for chunk in chunks]
        embeddings = self.embedding_manager.generate_embeddings(texts)
        
        # Store in vector database
        self.vector_store.add_documents(chunks, embeddings)
        
        # Store in MongoDB
        doc_ids = self.mongodb.store_documents(chunks)
        
        return {
            "status": "success",
            "file": file_path,
            "chunks": len(chunks),
            "document_ids": doc_ids
        }
    
    def process_directory(self, directory: str = str(RAW_DATA_DIR)) -> List[Dict[str, Any]]:
        """
        Process all files in a directory.
        
        Args:
            directory: Directory path
            
        Returns:
            List of processing results
        """
        results = []
        
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith((".pdf", ".txt")):
                    file_path = os.path.join(root, file)
                    try:
                        result = self.process_file(file_path)
                        results.append(result)
                    except Exception as e:
                        results.append({
                            "status": "error",
                            "file": file_path,
                            "error": str(e)
                        })
        
        return results
    
    def process_batch(self, file_paths: List[str]) -> List[Dict[str, Any]]:
        """
        Process a batch of files.
        
        Args:
            file_paths: List of file paths
            
        Returns:
            List of processing results
        """
        results = []
        
        for file_path in file_paths:
            try:
                result = self.process_file(file_path)
                results.append(result)
            except Exception as e:
                results.append({
                    "status": "error",
                    "file": file_path,
                    "error": str(e)
                })
        
        return results