"""
Streamlit frontend for InsightScope.
"""
import streamlit as st
import os
import sys
import time
import numpy as np
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))

# Try direct imports first, then fallback to relative imports
try:
    from insight_scope.models.llm.rag_pipeline import RAGPipeline
    from insight_scope.utils.preprocessing.document_loader import DocumentLoader
    from insight_scope.models.embeddings.embedding_manager import EmbeddingManager
    from insight_scope.models.embeddings.vector_store import VectorStore
except ImportError:
    # Fallback to relative imports for Streamlit Cloud
    from models.llm.rag_pipeline import RAGPipeline
    from utils.preprocessing.document_loader import DocumentLoader
    from models.embeddings.embedding_manager import EmbeddingManager
    from models.embeddings.vector_store import VectorStore

# Page configuration
st.set_page_config(
    page_title="InsightScope - Enterprise Knowledge Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "rag_pipeline" not in st.session_state:
    st.session_state.rag_pipeline = RAGPipeline()

# Sidebar for configuration and file upload
with st.sidebar:
    st.title("🧠 InsightScope")
    st.subheader("Configuration")
    
    # Prompt style selection
    prompt_style = st.selectbox(
        "Select Response Style",
        ["Standard", "Formal Corporate", "Analyst Summary", "Concise Bullets"]
    )
    
    # Update prompt template based on selection
    if prompt_style == "Standard":
        template = """
        You are an intelligent enterprise assistant. Use the provided context to answer the question.
        If the answer is not in the context, say "I don't have enough information."
        
        Context: {context}
        
        Question: {query}
        
        Answer:
        """
    elif prompt_style == "Formal Corporate":
        template = """
        You are a professional corporate assistant. Provide a formal, detailed response based on the context.
        Use professional business language and maintain a corporate tone.
        If the information is not in the context, clearly state that the data is not available.
        
        Context: {context}
        
        Question: {query}
        
        Answer:
        """
    elif prompt_style == "Analyst Summary":
        template = """
        You are a data analyst. Analyze the provided context and give a structured summary with key insights.
        Include relevant metrics and trends if available. Be objective and data-driven.
        If the data is insufficient, acknowledge the limitations.
        
        Context: {context}
        
        Question: {query}
        
        Analysis:
        """
    elif prompt_style == "Concise Bullets":
        template = """
        You are a concise information assistant. Provide a bullet-point response with only the most essential information.
        Be direct and brief. Each bullet should contain a single key point.
        If the information is not available, simply state "Insufficient data" as a single bullet.
        
        Context: {context}
        
        Question: {query}
        
        Key Points:
        """
    
    st.session_state.rag_pipeline.set_prompt_template(template)
    
    # File upload section
    st.subheader("Upload Documents")
    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "txt", "docx"])
    
    if uploaded_file is not None:
        # Save uploaded file
        save_dir = Path("insight_scope/data/raw")
        save_dir.mkdir(parents=True, exist_ok=True)
        file_path = save_dir / uploaded_file.name
        
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        with st.spinner("Processing document..."):
            # Process document
            loader = DocumentLoader()
            
            if uploaded_file.name.endswith(".pdf"):
                chunks = loader.load_pdf(str(file_path))
            elif uploaded_file.name.endswith(".txt"):
                chunks = loader.load_text(str(file_path))
            else:
                st.error("Unsupported file type")
                chunks = []
            
            if chunks:
                # Generate embeddings
                embedding_manager = EmbeddingManager()
                texts = [chunk["text"] for chunk in chunks]
                embeddings = embedding_manager.generate_embeddings(texts)
                
                # Store in vector database
                vector_store = VectorStore()
                vector_store.add_documents(chunks, embeddings)
                
                st.success(f"Document processed: {len(chunks)} chunks extracted and indexed")

# Main chat interface
st.title("🧠 InsightScope: Enterprise Knowledge Assistant")
st.markdown("Ask questions about your company data and get accurate, context-aware responses.")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Display sources if available
        if "sources" in message and message["sources"]:
            with st.expander("View Sources"):
                for i, source in enumerate(message["sources"]):
                    st.markdown(f"**Source {i+1}**")
                    st.markdown(f"*Text:* {source['text']}")
                    st.markdown(f"*Source:* {source['metadata'].get('source', 'Unknown')}")
                    st.markdown(f"*Relevance Score:* {source['score']:.4f}")
                    st.markdown("---")

# Chat input
if prompt := st.chat_input("Ask a question about your company data"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Check if documents have been uploaded
            vector_store = VectorStore()
            # Check if documents exist by trying to search with a dummy query
            has_documents = False
            try:
                # Try using has_documents method if available
                has_documents = vector_store.has_documents()
            except AttributeError:
                # Fallback: Check if search returns any results
                dummy_embedding = np.zeros((1, 768))  # Standard embedding size
                results = vector_store.search(dummy_embedding)
                has_documents = len(results) > 0
                
            if not has_documents:
                st.warning("No documents have been uploaded yet. Please upload documents using the sidebar to enable question answering.")
                response = {
                    "answer": "I don't have any documents to search through. Please upload some documents using the file uploader in the sidebar.",
                    "sources": []
                }
            else:
                response = st.session_state.rag_pipeline.query(prompt)
            
            # Display response
            st.markdown(response["answer"])
            
            # Add sources to message
            if "sources" in response and response["sources"]:
                with st.expander("View Sources"):
                    for i, source in enumerate(response["sources"]):
                        st.markdown(f"**Source {i+1}**")
                        st.markdown(f"*Text:* {source['text']}")
                        st.markdown(f"*Source:* {source['metadata'].get('source', 'Unknown')}")
                        st.markdown(f"*Relevance Score:* {source['score']:.4f}")
                        st.markdown("---")
    
    # Add assistant response to chat history
    st.session_state.messages.append({
        "role": "assistant", 
        "content": response["answer"],
        "sources": response.get("sources", [])
    })