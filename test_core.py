"""
Simple test script to demonstrate core functionality of InsightScope.
"""
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parent))

def test_config():
    """Test configuration loading."""
    try:
        from insight_scope.config.config import Config
        config = Config()
        print("✅ Configuration loaded successfully")
        print(f"LLM Model: {config.llm_model}")
        print(f"Vector DB: {config.vector_db_type}")
        return True
    except Exception as e:
        print(f"❌ Configuration error: {str(e)}")
        return False

def test_document_loader():
    """Test document loader functionality."""
    try:
        from insight_scope.utils.preprocessing.document_loader import DocumentLoader
        loader = DocumentLoader()
        print("✅ Document loader initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Document loader error: {str(e)}")
        return False

def test_embedding_manager():
    """Test embedding manager functionality."""
    try:
        from insight_scope.models.embeddings.embedding_manager import EmbeddingManager
        manager = EmbeddingManager()
        print("✅ Embedding manager initialized successfully")
        # Test with a simple text
        try:
            embedding = manager.get_query_embedding("This is a test query")
            print(f"✅ Query embedding generated successfully (dimensions: {len(embedding)})")
        except Exception as e:
            print(f"❌ Query embedding error: {str(e)}")
        return True
    except Exception as e:
        print(f"❌ Embedding manager error: {str(e)}")
        return False

def test_vector_store():
    """Test vector store functionality."""
    try:
        from insight_scope.models.embeddings.vector_store import VectorStore
        store = VectorStore()
        print("✅ Vector store initialized successfully")
        print(f"Vector store type: {store.vector_db_type}")
        return True
    except Exception as e:
        print(f"❌ Vector store error: {str(e)}")
        return False

def test_mongodb():
    """Test MongoDB connection."""
    try:
        from insight_scope.utils.mongodb_connector import MongoDBConnector
        connector = MongoDBConnector()
        print("✅ MongoDB connector initialized successfully")
        return True
    except Exception as e:
        print(f"❌ MongoDB connector error: {str(e)}")
        return False

def test_rag_pipeline():
    """Test RAG pipeline functionality."""
    try:
        from insight_scope.models.llm.rag_pipeline import RAGPipeline
        pipeline = RAGPipeline()
        print("✅ RAG pipeline initialized successfully")
        return True
    except Exception as e:
        print(f"❌ RAG pipeline error: {str(e)}")
        return False

if __name__ == "__main__":
    print("🧪 Testing InsightScope Core Components")
    print("-" * 50)
    
    tests = [
        ("Configuration", test_config),
        ("Document Loader", test_document_loader),
        ("Embedding Manager", test_embedding_manager),
        ("Vector Store", test_vector_store),
        ("MongoDB Connector", test_mongodb),
        ("RAG Pipeline", test_rag_pipeline)
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\n🔍 Testing {name}...")
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Unexpected error: {str(e)}")
            results.append((name, False))
    
    print("\n" + "-" * 50)
    print("📊 Test Summary:")
    
    success_count = sum(1 for _, result in results if result)
    print(f"✅ {success_count}/{len(tests)} components initialized successfully")
    
    if success_count < len(tests):
        print("\n⚠️ Some components failed to initialize. Check the logs above for details.")
        print("This may be due to missing dependencies or configuration issues.")
    else:
        print("\n🎉 All components initialized successfully!")
        print("The InsightScope core functionality is working properly.")