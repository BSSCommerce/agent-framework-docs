# Overview
BSS Agent Framework is a comprehensive AI Agent Development Framework designed for production-ready AI applications. Built on top of LangChain and LangGraph, it provides a robust foundation for creating intelligent agents with enterprise-grade features.

This framework addresses common challenges in AI agent development by offering:
- **Production-Ready Infrastructure**: Built-in support for authentication, security, and deployment
- **Multi-Model Support**: Seamless integration with multiple LLM providers
- **Advanced RAG Capabilities**: Comprehensive retrieval-augmented generation pipeline
- **Enterprise Security**: Rate limiting, data privacy, and input sanitization
- **Scalable Architecture**: Support for multiple databases and cloud providers

## Main Components

- **Core Framework**: Base agent implementation and multi-user session management
- **Database Integration**: Multi-database support for checkpoints and long-term memory
- **RAG Pipeline**: Advanced retrieval-augmented generation with multiple data sources
- **Security**: Rate limiting, data privacy protection, and prompt sanitization
- **Authentication**: API key management and client access control
- **Server API**: FastAPI-based REST API with streaming support
- **MCP Integration**: Model Context Protocol for enhanced tool integration
- **Environment Management**: Configuration and environment handling

# Technologies Usage

## Core Framework
- **LangChain** (>=0.3.26) - Core AI framework
- **LangGraph** (>=0.5.3) - State management and workflow orchestration
- **FastAPI** (>=0.100.0) - Web framework for API development
- **Pydantic** (>=2.0.0) - Data validation and settings management

## LLM Providers
- **OpenAI**: GPT-4o, GPT-4o-mini, GPT-4o-1106
- **Anthropic**: Claude 3.5 Sonnet
- **Google**: Gemini 1.5 Flash, Gemini 1.5 Pro
- **DeepSeek**: DeepSeek R1
- **Ollama**: Llama 3.8B variants (local deployment)

## Database Support
### Checkpoint Databases (LangGraph)
- **PostgreSQL** - Production-ready relational database
- **MySQL** - Popular open-source database
- **MongoDB** - NoSQL document database
- **Redis** - In-memory data structure store
- **SQLite** - Lightweight file-based database

### Vector Databases
- **Chroma** - Open-source embedding database
- **Weaviate** - Vector search engine
- **In-Memory** - Fast development and testing
- **File-based** - Persistent local storage

## Data Extraction & Processing
### Document Formats
- **PDF**: PyPDF2 for text extraction
- **Microsoft Office**: 
  - Word documents (python-docx, docx2txt)
  - Excel files (pandas, openpyxl, xlrd)
  - PowerPoint (python-pptx)
- **RTF**: Rich text format parsing
- **Web Content**: BeautifulSoup4, Trafilatura, Selenium, Playwright

### Data Processing
- **Parquet**: PyArrow for columnar data
- **Avro**: FastAvro for serialization
- **CSV/JSON**: Pandas for data manipulation
- **Text Processing**: NLTK, spaCy, TextStat

## Development Tools
### Testing
- **Pytest**: Testing framework
- **Coverage**: Code coverage analysis
- **Mock**: Test mocking utilities

### Code Quality
- **Black**: Code formatting
- **isort**: Import sorting
- **Flake8**: Linting
- **MyPy**: Type checking
- **Pre-commit**: Git hooks


## Embedding Models
### Cloud Providers
- **OpenAI**: text-embedding-3-small, text-embedding-3-large
- **Google AI**: gemini-embedding-exp-03-07
- **Azure OpenAI**: Azure-hosted OpenAI embeddings
- **AWS Bedrock**: Amazon's embedding models
- **Cohere**: Cohere embedding models
- **Jina**: Jina AI embeddings
- **Vectara**: Vectara embeddings
- **Voyage**: Voyage AI embeddings

### Local Models
- **Ollama**: Local embedding models
- **GPT4All**: Local GPT4All embeddings
- **HuggingFace**: Open-source embedding models
