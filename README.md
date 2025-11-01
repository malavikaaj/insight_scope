# InsightScope – Intelligent Enterprise Knowledge Assistant

**Turning organizational data chaos into cognitive clarity — powered by OpenAI, LangChain, and ChromaDB/FAISS.**

## Overview

InsightScope is a Retrieval-Augmented Generation (RAG) based AI assistant that allows users to query company documents, reports, and emails in natural language — and receive accurate, context-aware responses backed by real data.

Think of it as ChatGPT, but it knows your organization's internal data.

## Features

- **Natural Language Queries**: Ask questions about your company data in plain English
- **Document Processing**: Upload and process PDFs, text files, and more
- **Smart Retrieval**: Finds the most relevant information using vector search
- **Context-Aware Responses**: Generates answers based on your actual data
- **Source Citations**: View the exact sources used to generate responses
- **Prompt Engineering Playground**: Customize response styles and formats
- **Local Deployment**: Runs entirely on your local machine for data privacy

## Use Case Examples

- "Summarize last quarter's financial highlights."
- "What are the main cybersecurity recommendations in the IT audit report?"
- "Which policy documents mention 'remote work compliance'?"
- "Draft an executive summary for the sustainability report."

## System Architecture

```
           ┌────────────────────┐ 
           │  Streamlit UI       │ 
           └────────┬───────────┘ 
                    │ Query 
                    ▼ 
           ┌────────────────────┐ 
           │ LangChain / LlamaIndex│ 
           │  (Query Orchestration)│ 
           └────────┬───────────┘ 
                    │ 
          ┌─────────┴────────────┐ 
          │ ChromaDB/FAISS        │ ← indexed embeddings 
          └─────────┬────────────┘ 
                    │ 
          ┌─────────┴────────────┐ 
          │ OpenAI (GPT-4o)       │ ← generates final answer 
          └─────────┬────────────┘ 
                    │ 
          ┌─────────┴────────────┐ 
          │ Response Formatter     │ 
          │ + Confidence Scoring   │ 
          └─────────┬────────────┘ 
                    │ 
                    ▼ 
           ┌────────────────────┐ 
           │  Streamlit Frontend │ 
           └────────────────────┘ 
```

## Tech Stack

- **Language**: Python
- **NLP/ML**: Hugging Face Transformers, PyTorch
- **Orchestration**: LangChain / LlamaIndex
- **LLM**: OpenAI (GPT-4o / GPT-4-turbo)
- **Retrieval**: ChromaDB/FAISS
- **Storage**: MongoDB
- **Frontend**: Streamlit

## Getting Started

### Prerequisites

- Python 3.8+
- MongoDB (already configured)
- OpenAI API key

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/insight_scope.git
   cd insight_scope
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file based on `.env.example` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

### Running the Application

1. Start the Streamlit frontend:
   ```
   python run.py run
   ```

2. Process documents (optional):
   ```
   python run.py process --dir /path/to/your/documents
   ```

## Project Structure

```
insight_scope/
├── app/
│   ├── frontend/       # Streamlit UI
│   └── api/            # Backend API
├── data/
│   ├── raw/            # Original documents
│   └── processed/      # Processed data
├── models/
│   ├── embeddings/     # Embedding models
│   └── llm/            # LLM integration
├── utils/
│   ├── preprocessing/  # Document processing
│   └── evaluation/     # Performance metrics
└── config/             # Configuration
```

## Deployment

### Quick Start with Docker

The easiest way to deploy InsightScope:

```bash
# Run the deployment script
./deploy.sh
```

The application will be available at `http://localhost:8501`

### Manual Deployment

1. **Configure environment**:
   ```bash
   cp .env.production .env
   # Edit .env with your settings
   ```

2. **Deploy with Docker Compose**:
   ```bash
   docker-compose up -d
   ```

3. **Validate deployment**:
   ```bash
   python validate_deployment.py
   ```

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

### LLM Provider Options

- **GPT4All** (default): No API key required, runs locally
- **OpenAI**: Requires API key, best quality responses
- **Ollama**: Local deployment with various models

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.