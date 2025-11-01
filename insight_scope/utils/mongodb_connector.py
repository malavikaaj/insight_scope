"""
MongoDB connector for storing and retrieving document data.
"""
from typing import List, Dict, Any, Optional
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from datetime import datetime

from insight_scope.config.config import MONGODB_URI, MONGODB_DB_NAME

class MongoDBConnector:
    """Connector for MongoDB operations."""
    
    def __init__(self, uri: str = MONGODB_URI, db_name: str = MONGODB_DB_NAME):
        """
        Initialize MongoDB connector.
        
        Args:
            uri: MongoDB connection URI
            db_name: Database name
        """
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        
        # Create collections if they don't exist
        self.documents = self.db.documents
        self.queries = self.db.queries
    
    def store_document(self, document: Dict[str, Any]) -> str:
        """
        Store document in MongoDB.
        
        Args:
            document: Document data with metadata
            
        Returns:
            Document ID
        """
        result = self.documents.insert_one(document)
        return str(result.inserted_id)
    
    def store_documents(self, documents: List[Dict[str, Any]]) -> List[str]:
        """
        Store multiple documents in MongoDB.
        
        Args:
            documents: List of document data with metadata
            
        Returns:
            List of document IDs
        """
        result = self.documents.insert_many(documents)
        return [str(id) for id in result.inserted_ids]
    
    def get_document(self, document_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve document by ID.
        
        Args:
            document_id: Document ID
            
        Returns:
            Document data or None if not found
        """
        from bson.objectid import ObjectId
        return self.documents.find_one({"_id": ObjectId(document_id)})
    
    def search_documents(self, query: Dict[str, Any], limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search documents by query.
        
        Args:
            query: MongoDB query
            limit: Maximum number of results
            
        Returns:
            List of matching documents
        """
        return list(self.documents.find(query).limit(limit))
    
    def log_query(self, query_text: str, results: List[str], user_id: Optional[str] = None) -> str:
        """
        Log user query and results.
        
        Args:
            query_text: User query text
            results: List of document IDs returned
            user_id: Optional user identifier
            
        Returns:
            Query log ID
        """
        query_log = {
            "query": query_text,
            "results": results,
            "user_id": user_id,
            "timestamp": datetime.now()
        }
        result = self.queries.insert_one(query_log)
        return str(result.inserted_id)
    
    def close(self):
        """Close MongoDB connection."""
        self.client.close()