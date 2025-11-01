"""
Document loader module for processing various document types.
"""
import os
from typing import List, Dict, Any, Optional
import fitz  # PyMuPDF
import pandas as pd
from pathlib import Path

class DocumentLoader:
    """Handles loading and preprocessing of various document types."""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize the document loader.
        
        Args:
            chunk_size: Size of text chunks for processing
            chunk_overlap: Overlap between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def load_pdf(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Load and chunk a PDF document.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            List of document chunks with metadata
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"PDF file not found: {file_path}")
        
        doc = fitz.open(file_path)
        chunks = []
        
        # Extract document metadata
        metadata = {
            "source": file_path,
            "title": os.path.basename(file_path),
            "pages": len(doc),
            "file_type": "pdf"
        }
        
        text_content = ""
        for page_num, page in enumerate(doc):
            text = page.get_text()
            text_content += text
            
            # Create chunks when text_content exceeds chunk_size
            if len(text_content) >= self.chunk_size:
                chunks.extend(self._create_chunks(text_content, metadata, page_num))
                # Keep the overlap for the next chunk
                text_content = text_content[-self.chunk_overlap:]
        
        # Add any remaining text as a chunk
        if text_content:
            chunks.extend(self._create_chunks(text_content, metadata, len(doc)-1))
            
        return chunks
    
    def load_text(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Load and chunk a text document.
        
        Args:
            file_path: Path to the text file
            
        Returns:
            List of document chunks with metadata
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Text file not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as file:
            text_content = file.read()
        
        metadata = {
            "source": file_path,
            "title": os.path.basename(file_path),
            "file_type": "text"
        }
        
        return self._create_chunks(text_content, metadata)
    
    def _create_chunks(self, text: str, metadata: Dict[str, Any], page_num: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Split text into chunks of specified size.
        
        Args:
            text: Text to split into chunks
            metadata: Document metadata
            page_num: Page number (optional)
            
        Returns:
            List of chunks with metadata
        """
        chunks = []
        
        # Simple chunking by character count
        for i in range(0, len(text), self.chunk_size - self.chunk_overlap):
            chunk_text = text[i:i + self.chunk_size]
            if len(chunk_text) < 100:  # Skip very small chunks
                continue
                
            chunk_metadata = metadata.copy()
            if page_num is not None:
                chunk_metadata["page"] = page_num
            
            chunks.append({
                "text": chunk_text,
                "metadata": chunk_metadata
            })
        
        return chunks