# Extract text from a file using textextractor
from typing import Any, Dict, List

from langchain_google_genai import ChatGoogleGenerativeAI
from bssagent.rag.embedding_models import GOOGLE_AI_EMBEDDING_MODELS
from bssagent.rag.rag import RAGConfig, create_rag_pipeline
from bssagent.rag.text_extractor import extract_text_from_files, extract_text_from_urls, extract_text_from_mixed_sources

from bssagent.environment import setup_environment_variables

setup_environment_variables()

# Extract text from a file
def extract_text_from_file(file_path: str) -> List[Dict[str, Any]]:
    return extract_text_from_files([file_path])

# Extract text from a URL
def extract_text_from_url(url: str) -> List[Dict[str, Any]]:
    return extract_text_from_urls([url])

# Extract text from a API
def extract_text_from_api(api_url: str) -> List[Dict[str, Any]]:
    return extract_text_from_urls([api_url])

# Extract text from a mixed source
def extract_text_from_mixed_source(mixed_source: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return extract_text_from_mixed_sources(mixed_source)
"""
 Create a pipeline using create_rag_pipeline
Sources is a list of dictionaries with the following keys:
- type: str, the type of the source, can be "file", "url", "api"
- path: str, the path to the file, if type is "file"
- url: str, the url to the file, if type is "url"
for example:
sources = [
    {"type": "file", "path": "path/to/file.txt"},
    {"type": "url", "url": "https://www.example.com"},
    {"type": "api", "url": "https://api.example.com", "api_key": "1234567890"}
]
"""
def create_and_query_pipeline():
    sources = [
        {"type": "url", "url": "https://www.example.com"},
    ]
    pipeline = create_rag_pipeline(
        sources=sources,
        embedding_model_name=GOOGLE_AI_EMBEDDING_MODELS['GEMINI_EMBEDDING_EXP_03_07'],
        vector_db_type="chroma",
        # If you want to use a different LLM, you can pass it here
        # If llm is not passed, the pipeline will be created without QA chain
        llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    )

    result = pipeline.query("What is the main topic of the page?")
    print(result)

"""
Load vector store and retrieve documents using similarity search
"""
def retrieve_documents():
    config = RAGConfig(
        embedding_model_name=GOOGLE_AI_EMBEDDING_MODELS['GEMINI_EMBEDDING_EXP_03_07'],
        vector_db_type='chroma',
        chunk_size=500,
        chunk_overlap=100,
        persist_directory='./vector_store',
        include_metadata=True
    )
    sources = [
        {"type": "url", "url": "https://www.example.com"},
    ]
    """ No need pass LLM here, Vector store will be used for similarity search """
    pipeline = create_rag_pipeline(
        sources=sources,
        embedding_model_name=config.embedding_model_name,
        vector_db_type=config.vector_db_type,
        config=config
    )
    # vector_store = pipeline.load_vector_store(config.persist_directory or "./vector_store")
    print(pipeline.similarity_search("What is the main topic of the page?"))

if __name__ == "__main__":
    # create_and_query_pipeline()
    retrieve_documents()




