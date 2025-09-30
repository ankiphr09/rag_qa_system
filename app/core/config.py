from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "Enterprise Document Q&A"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["*"]
    
    # Vector DB
    PINECONE_API_KEY: str
    PINECONE_ENVIRONMENT: str
    PINECONE_INDEX_NAME: str
    
    # Document Store
    MONGODB_URL: str
    MONGODB_DB_NAME: str
    
    # Cache
    REDIS_URL: str
    
    # LLM
    OPENAI_API_KEY: str
    
    class Config:
        env_file = ".env"

settings = Settings()