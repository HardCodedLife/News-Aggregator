import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # App Info
    PROJECT_NAME: str = "News RAG Production"
    API_V1_STR: str = "/api/v1"

    # Database (Defaults to Docker service names)
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "user")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "password")
    POSTGRES_DB: str = os.getenv("POSTGRES_SERVER", "vectordb")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "db")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")

    # AI Configuration
    # We use a standard OpenAI-compatible URL structure for Ollama
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_API_URL", "http://ollama:11434")
    
    # Models
    # LLM: The brain that answers
    MODEL_NAME: str = "gemini-3-pro-preview:latest" 
    # Embedding: The translator (Text -> Numbers)
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    EMBED_DIM: int = 384

settings = Settings()
