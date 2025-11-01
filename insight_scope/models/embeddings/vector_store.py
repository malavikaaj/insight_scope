"""
Vector store module for managing document embeddings.
"""
from typing import List, Dict, Any, Optional, Union
import os
import numpy as np
import chromadb
import faiss
import pickle
from pathlib import Path

from insight_scope.config.config import VECTOR_DB_TYPE, VECTOR_DB_PATH

class VectorStore:
    """Vector database for storing and retrieving document embeddings."""
    
    def __init__(self, db_type: str = VECTOR_DB_TYPE, db_path: str = VECTOR_DB_PATH):
        """
        Initialize the vector store.
        
        Args:
            db_type: Type of vector database ('chroma' or 'faiss')
            db_path: Path to store the vector database
        """
        self.db_type = db_type.lower()
        self.db_path = db_path
        
        if self.db_type == "chroma":
            self._init_chroma()
        elif self.db_type == "faiss":
            self._init_faiss()
        else:
            raise ValueError(f"Unsupported vector database type: {db_type}")
            
    def has_documents(self) -> bool:
        """
        Check if the vector store has any documents.
        
        Returns:
            bool: True if documents exist, False otherwise
        """
        if self.db_type == "chroma":
            return self.collection.count() > 0
        elif self.db_type == "faiss":
            if not os.path.exists(self.index_path) or not os.path.exists(self.metadata_path):
                return False
            try:
                with open(self.metadata_path, "rb") as f:
                    metadata = pickle.load(f)
                return len(metadata.get("documents", [])) > 0
            except:
                return False
        return False
    
    def _init_chroma(self):
        """Initialize ChromaDB."""
        self.client = chromadb.PersistentClient(path=self.db_path)
        # Create collection if it doesn't exist
        try:
            self.collection = self.client.get_collection("documents")
        except:
            self.collection = self.client.create_collection("documents")
    
    def _init_faiss(self):
        """Initialize FAISS index."""
        self.index_path = os.path.join(self.db_path, "faiss_index.bin")
        self.metadata_path = os.path.join(self.db_path, "faiss_metadata.pkl")
        
        # Load existing index or create new one
        if os.path.exists(self.index_path) and os.path.exists(self.metadata_path):
            self.index = faiss.read_index(self.index_path)
            with open(self.metadata_path, 'rb') as f:
                self.metadata = pickle.load(f)
        else:
            # Will be initialized when first embeddings are added
            self.index = None
            self.metadata = {"ids": [], "documents": [], "metadata": []}

    def reset(self):
        """Clear all stored documents and reinitialize the vector store."""
        if self.db_type == "chroma":
            # Delete the existing collection and recreate
            try:
                self.client.delete_collection("documents")
            except Exception:
                pass
            try:
                self.collection = self.client.create_collection("documents")
            except Exception:
                # If creation fails because it exists, get it
                try:
                    self.collection = self.client.get_collection("documents")
                except Exception:
                    # As a last resort, reinitialize the client and collection
                    self._init_chroma()
        elif self.db_type == "faiss":
            # Remove index and metadata files
            try:
                if os.path.exists(self.index_path):
                    os.remove(self.index_path)
                if os.path.exists(self.metadata_path):
                    os.remove(self.metadata_path)
            except Exception:
                pass
            # Reset in-memory structures
            self.index = None
            self.metadata = {"ids": [], "documents": [], "metadata": []}
    
    def add_documents(self, documents: List[Dict[str, Any]], embeddings: np.ndarray, ids: Optional[List[str]] = None):
        """
        Add documents and their embeddings to the vector store.
        
        Args:
            documents: List of document chunks with text and metadata
            embeddings: Document embeddings
            ids: Optional list of document IDs
        """
        if ids is None:
            ids = [f"doc_{i}" for i in range(len(documents))]
        
        if self.db_type == "chroma":
            texts = [doc["text"] for doc in documents]
            metadatas = [doc["metadata"] for doc in documents]
            
            # Add documents to ChromaDB
            self.collection.add(
                documents=texts,
                embeddings=embeddings.tolist(),
                metadatas=metadatas,
                ids=ids
            )
        
        elif self.db_type == "faiss":
            # Initialize index if not already done
            if self.index is None:
                dimension = embeddings.shape[1]
                self.index = faiss.IndexFlatL2(dimension)
            
            # Add embeddings to FAISS index
            self.index.add(embeddings)
            
            # Store document data and metadata
            for i, (doc, doc_id) in enumerate(zip(documents, ids)):
                self.metadata["ids"].append(doc_id)
                self.metadata["documents"].append(doc["text"])
                self.metadata["metadata"].append(doc["metadata"])
            
            # Save index and metadata
            faiss.write_index(self.index, self.index_path)
            with open(self.metadata_path, 'wb') as f:
                pickle.dump(self.metadata, f)
    
    def search(self, query_embedding: np.ndarray, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar documents using query embedding.
        
        Args:
            query_embedding: Query embedding vector
            top_k: Number of results to return
            
        Returns:
            List of similar documents with scores and metadata
        """
        if self.db_type == "chroma":
            results = self.collection.query(
                query_embeddings=[query_embedding.tolist()],
                n_results=top_k
            )
            
            documents = []
            for i in range(len(results["documents"][0])):
                documents.append({
                    "text": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i],
                    "id": results["ids"][0][i],
                    "score": results["distances"][0][i]
                })
            
            return documents
        
        elif self.db_type == "faiss":
            if self.index is None or self.index.ntotal == 0:
                return []
            
            # Search FAISS index
            scores, indices = self.index.search(query_embedding.reshape(1, -1), top_k)
            
            documents = []
            for i, idx in enumerate(indices[0]):
                if idx < len(self.metadata["documents"]):
                    documents.append({
                        "text": self.metadata["documents"][idx],
                        "metadata": self.metadata["metadata"][idx],
                        "id": self.metadata["ids"][idx],
                        "score": float(scores[0][i])
                    })
            
            return documents