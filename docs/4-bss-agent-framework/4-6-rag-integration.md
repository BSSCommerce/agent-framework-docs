# RAG Integration

## Overview

The RAG (Retrieval-Augmented Generation) integration provides a complete pipeline for building intelligent question-answering systems. It combines text extraction, embedding generation, vector storage, and retrieval capabilities to create powerful knowledge-based AI applications.

## Basic Concepts

### Embedding Models

Embedding models convert text into numerical vectors that capture semantic meaning. These vectors enable similarity search and retrieval operations.

**Key Features:**
- **Semantic Understanding**: Captures meaning beyond exact word matches
- **Dimensionality**: Typically 384-1536 dimensions depending on model
- **Normalization**: Vectors are normalized for cosine similarity
- **Multi-language Support**: Many models support multiple languages

### Vector Databases

Vector databases store and index embedding vectors for efficient similarity search and retrieval.

**Types:**
- **In-Memory**: FAISS, Chroma (fast, temporary)
- **File-Based**: Persistent local storage
- **Cloud-Based**: Pinecone, Weaviate Cloud (scalable)
- **Self-Hosted**: Weaviate, Qdrant, Milvus (control)
- **Database Extensions**: PostgreSQL pgvector, Redis (integrated)

### Text Extractor

The text extractor processes various data sources into clean, structured text for embedding.

**Supported Sources:**
- **Files**: PDF, DOCX, TXT, code files, spreadsheets
- **Web Pages**: HTML content extraction with metadata
- **APIs**: REST API responses (JSON, XML, text)
- **Mixed Sources**: Combined processing pipeline

## Supported Models

### Embedding Models

#### OpenAI Models
```python
OPENAI_EMBEDDING_MODELS = {
    "TEXT_EMBEDDING_ADA_002": "text-embedding-ada-002",
    "TEXT_EMBEDDING_3_SMALL": "text-embedding-3-small",
    "TEXT_EMBEDDING_3_LARGE": "text-embedding-3-large",
}
```

#### Google AI Models
```python
GOOGLE_AI_EMBEDDING_MODELS = {
    "GEMINI_EMBEDDING_EXP_03_07": "models/gemini-embedding-exp-03-07",
}
```

#### HuggingFace Models
```python
HUGGINGFACE_EMBEDDING_MODELS = {
    "ALL_MINI_LM_L6_V2": "sentence-transformers/all-MiniLM-L6-v2",
    "ALL_MPNET_BASE_V2": "sentence-transformers/all-mpnet-base-v2",
    "BGE_SMALL_EN_V1_5": "BAAI/bge-small-en-v1.5",
    "BGE_BASE_EN_V1_5": "BAAI/bge-base-en-v1.5",
    "BGE_LARGE_EN_V1_5": "BAAI/bge-large-en-v1.5",
}
```

#### Cohere Models
```python
COHERE_EMBEDDING_MODELS = {
    "EMBED_ENGLISH_V3_0": "embed-english-v3.0",
    "EMBED_MULTILINGUAL_V3_0": "embed-multilingual-v3.0",
}
```

#### Local Models
```python
LOCAL_EMBEDDING_MODELS = {
    "INSTRUCTOR_LARGE": "hkunlp/instructor-large",
    "E5_LARGE_V2": "intfloat/e5-large-v2",
    "GTE_LARGE": "thenlper/gte-large",
}
```

### Vector Databases

#### In-Memory & File-Based
```python
IN_MEMORY_VECTOR_DBS = {
    "FAISS": "faiss",
    "CHROMA": "chroma",
    "HNSWLIB": "hnswlib",
}
```

#### Cloud-Based
```python
CLOUD_VECTOR_DBS = {
    "PINECONE": "pinecone",
    "WEAVIATE_CLOUD": "weaviate_cloud",
    "QDANT_CLOUD": "qdrant_cloud",
    "VECTARA": "vectara",
}
```

#### Self-Hosted
```python
SELF_HOSTED_VECTOR_DBS = {
    "WEAVIATE": "weaviate",
    "QDANT": "qdrant",
    "MILVUS": "milvus",
    "CHROMA": "chroma",
}
```

#### Database Extensions
```python
DATABASE_EXTENSION_VECTOR_DBS = {
    "POSTGRESQL_PGVECTOR": "postgresql_pgvector",
    "REDIS": "redis",
    "ELASTICSEARCH": "elasticsearch",
}
```

## Core Functions

### Text Extractor Functions

#### Extract from Files
```python
from bssagent.rag.text_extractor import extract_text_from_files

# Extract from single or multiple files
results = extract_text_from_files([
    "path/to/document.pdf",
    "path/to/code.py",
    "path/to/data.csv"
])
```

#### Extract from URLs
```python
from bssagent.rag.text_extractor import extract_text_from_urls

# Extract from web pages
results = extract_text_from_urls([
    "https://example.com",
    "https://api.example.com/data"
])
```

#### Extract from Mixed Sources
```python
from bssagent.rag.text_extractor import extract_text_from_mixed_sources

# Mixed source configuration
sources = [
    {"type": "file", "path": "document.pdf"},
    {"type": "url", "url": "https://example.com"},
    {"type": "api", "url": "https://api.example.com", "api_key": "key"}
]

results = extract_text_from_mixed_sources(sources)
```

### RAG Pipeline Functions

#### Create RAG Pipeline
```python
from bssagent.rag.rag import create_rag_pipeline, RAGConfig
from bssagent.rag.embedding_models import GOOGLE_AI_EMBEDDING_MODELS

# Basic pipeline creation
pipeline = create_rag_pipeline(
    sources=sources,
    embedding_model_name=GOOGLE_AI_EMBEDDING_MODELS['GEMINI_EMBEDDING_EXP_03_07'],
    vector_db_type="chroma"
)
```

#### Query RAG System
```python
# Query with LLM integration
result = pipeline.query("What is the main topic of the document?")
print(f"Answer: {result.answer}")
print(f"Sources: {len(result.sources)}")
print(f"Confidence: {result.confidence}")
```

#### Similarity Search
```python
# Search without LLM
documents = pipeline.similarity_search("search query", k=5)
for doc, score in documents:
    print(f"Score: {score}, Content: {doc.page_content[:100]}...")
```

## Code Examples

### Basic RAG Pipeline

```python
from typing import Any, Dict, List
from langchain_google_genai import ChatGoogleGenerativeAI
from bssagent.rag.embedding_models import GOOGLE_AI_EMBEDDING_MODELS
from bssagent.rag.rag import create_rag_pipeline
from bssagent.environment import setup_environment_variables

# Setup environment
setup_environment_variables()

def create_and_query_pipeline():
    """Create a complete RAG pipeline and query it."""
    
    # Define sources
    sources = [
        {"type": "url", "url": "https://www.example.com"},
        {"type": "file", "path": "path/to/document.pdf"},
    ]
    
    # Create pipeline with LLM
    pipeline = create_rag_pipeline(
        sources=sources,
        embedding_model_name=GOOGLE_AI_EMBEDDING_MODELS['GEMINI_EMBEDDING_EXP_03_07'],
        vector_db_type="chroma",
        llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    )

    # Query the system
    result = pipeline.query("What is the main topic of the content?")
    
    print(f"Query: {result.query}")
    print(f"Answer: {result.answer}")
    print(f"Sources: {len(result.sources)}")
    print(f"Confidence: {result.confidence:.2f}")
    print(f"Processing Time: {result.processing_time:.2f}s")
    
    return result
```

### Advanced Configuration

```python
from bssagent.rag.rag import RAGConfig

def create_advanced_pipeline():
    """Create a pipeline with custom configuration."""
    
    # Custom configuration
    config = RAGConfig(
        embedding_model_name=GOOGLE_AI_EMBEDDING_MODELS['GEMINI_EMBEDDING_EXP_03_07'],
        vector_db_type='chroma',
        chunk_size=500,           # Smaller chunks for detailed retrieval
        chunk_overlap=100,        # Overlap to maintain context
        max_workers=10,           # Parallel processing
        timeout=30,               # Request timeout
        retry_attempts=3,         # Retry failed requests
        include_metadata=True,    # Include source metadata
        persist_directory='./vector_store',  # Persistent storage
        collection_name='my_documents'
    )
    
    sources = [
        {"type": "url", "url": "https://www.example.com"},
    ]
    
    # Create pipeline without LLM for similarity search only
    pipeline = create_rag_pipeline(
        sources=sources,
        embedding_model_name=config.embedding_model_name,
        vector_db_type=config.vector_db_type,
        config=config
    )
    
    # Perform similarity search
    results = pipeline.similarity_search("What is the main topic?", k=3)
    
    for i, (doc, score) in enumerate(results):
        print(f"Result {i+1} (Score: {score:.3f}):")
        print(f"Content: {doc.page_content[:200]}...")
        print(f"Source: {doc.metadata.get('source_path', 'Unknown')}")
        print()
    
    return pipeline
```

### Complete Working Example

```python
import os
from typing import Any, Dict, List
from langchain_google_genai import ChatGoogleGenerativeAI
from bssagent.rag.embedding_models import GOOGLE_AI_EMBEDDING_MODELS
from bssagent.rag.rag import create_rag_pipeline, RAGConfig
from bssagent.rag.text_extractor import extract_text_from_mixed_sources
from bssagent.environment import setup_environment_variables

def main():
    """Complete RAG integration example."""
    
    # Setup environment variables
    setup_environment_variables()
    
    # Define data sources
    sources = [
        {
            "type": "url", 
            "url": "https://www.example.com"
        },
        {
            "type": "file", 
            "path": "path/to/document.pdf"
        },
        {
            "type": "api",
            "url": "https://api.example.com/data",
            "api_key": os.getenv("API_KEY"),
            "headers": {"Authorization": f"Bearer {os.getenv('API_KEY')}"}
        }
    ]
    
    # Create RAG configuration
    config = RAGConfig(
        embedding_model_name=GOOGLE_AI_EMBEDDING_MODELS['GEMINI_EMBEDDING_EXP_03_07'],
        vector_db_type="chroma",
        chunk_size=1000,
        chunk_overlap=200,
        persist_directory="./vector_store",
        include_metadata=True
    )
    
    # Initialize LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0
    )
    
    # Create and setup pipeline
    pipeline = create_rag_pipeline(
        sources=sources,
        embedding_model_name=config.embedding_model_name,
        vector_db_type=config.vector_db_type,
        config=config,
        llm=llm
    )
    
    # Example queries
    queries = [
        "What is the main topic of the content?",
        "What are the key points discussed?",
        "Can you summarize the information?"
    ]
    
    # Process queries
    for query in queries:
        print(f"\n{'='*50}")
        print(f"Query: {query}")
        print(f"{'='*50}")
        
        result = pipeline.query(query)
        
        print(f"Answer: {result.answer}")
        print(f"Confidence: {result.confidence:.2f}")
        print(f"Processing Time: {result.processing_time:.2f}s")
        print(f"Sources Found: {len(result.sources)}")
        
        # Show source details
        for i, source in enumerate(result.sources[:2]):  # Show first 2 sources
            print(f"\nSource {i+1}:")
            print(f"  Title: {source.get('title', 'N/A')}")
            print(f"  Path: {source.get('source', 'N/A')}")
            print(f"  Content: {source.get('content', '')[:100]}...")

if __name__ == "__main__":
    main()
```

## Environment Setup

### Required Environment Variables

```bash
# OpenAI (if using OpenAI models)
export OPENAI_API_KEY="your-openai-api-key"

# Google AI (if using Google models)
export GOOGLE_API_KEY="your-google-api-key"

# Cohere (if using Cohere models)
export COHERE_API_KEY="your-cohere-api-key"

# Vector Database Credentials (if using cloud services)
export PINECONE_API_KEY="your-pinecone-api-key"
export PINECONE_ENVIRONMENT="your-pinecone-environment"
export QDRANT_API_KEY="your-qdrant-api-key"
export POSTGRESQL_CONNECTION_STRING="your-postgresql-connection-string"
```

### Installation

```bash
# Install required packages
pip install -r requirements-rag.txt

# Or install specific packages
pip install langchain langchain-google-genai chromadb sentence-transformers
```

## Best Practices

### Model Selection
- **Production**: Use cloud-based models (OpenAI, Google AI) for reliability
- **Development**: Use local models (HuggingFace) for cost efficiency
- **Multilingual**: Choose models with multilingual support for global applications

### Vector Database Selection
- **Development**: Use Chroma or FAISS for simplicity
- **Production**: Use cloud services (Pinecone, Weaviate) for scalability
- **Integration**: Use database extensions (PostgreSQL pgvector) for existing infrastructure

### Performance Optimization
- **Chunk Size**: 500-1000 tokens for balanced retrieval
- **Overlap**: 10-20% of chunk size for context preservation
- **Workers**: 5-10 for parallel processing
- **Timeout**: 30-60 seconds for web requests

### Security Considerations
- **API Keys**: Store securely in environment variables
- **Rate Limiting**: Implement request throttling
- **Content Filtering**: Sanitize extracted content
- **Access Control**: Implement proper authentication for vector stores
