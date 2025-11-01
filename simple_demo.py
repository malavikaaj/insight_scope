"""
Simple demo of InsightScope core functionality.
"""
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parent))

def main():
    """Run a simple demo of InsightScope."""
    print("🧠 InsightScope - Intelligent Enterprise Knowledge Assistant")
    print("=" * 60)
    print("\nThis demo shows the core functionality of InsightScope.")
    
    # Load configuration
    print("\n📋 Loading configuration...")
    import insight_scope.config.config as config
    print(f"✅ Configuration loaded successfully")
    print(f"  - Vector DB: {config.VECTOR_DB_TYPE}")
    print(f"  - Embedding Model: {config.EMBEDDING_MODEL}")
    
    # Create a sample document
    print("\n📄 Creating a sample document...")
    sample_text = """
    InsightScope is an intelligent enterprise knowledge assistant.
    It uses RAG (Retrieval Augmented Generation) to provide accurate answers based on company documents.
    The system integrates with OpenAI models and uses vector databases for efficient retrieval.
    """
    
    sample_file = Path("sample_document.txt")
    with open(sample_file, "w") as f:
        f.write(sample_text)
    print(f"✅ Sample document created at {sample_file.absolute()}")
    
    # Explain the RAG pipeline
    print("\n🔄 RAG Pipeline Explanation:")
    print("1. Document Loading: Documents are loaded and split into chunks")
    print("2. Embedding Generation: Text chunks are converted to vector embeddings")
    print("3. Vector Storage: Embeddings are stored in ChromaDB or FAISS")
    print("4. Query Processing: User questions are converted to embeddings")
    print("5. Retrieval: Similar documents are retrieved from the vector store")
    print("6. Response Generation: OpenAI generates answers based on retrieved context")
    
    # Explain how to run the application
    print("\n🚀 How to Run InsightScope:")
    print("1. Install dependencies: python -m pip install -r requirements.txt")
    print("2. Set up environment variables in .env file (API keys, etc.)")
    print("3. Process documents: python run.py process --dir /path/to/documents")
    print("4. Run the application: python run.py run")
    
    # Clean up
    print("\n🧹 Cleaning up...")
    if sample_file.exists():
        sample_file.unlink()
    print(f"✅ Sample document removed")
    
    print("\n✨ Demo completed!")
    print("=" * 60)

if __name__ == "__main__":
    main()