"""Configuration module for dof-chat application."""

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings using Pydantic Settings."""
    
    # Database configuration
    database_path: str = "dof_db/db.duckdb"
    
    # Gemini API configuration
    gemini_api_key: str = ""
    gemini_model: str = "gemini-1.5-flash"
    
    # Embedding model configuration
    embedding_model: str = "Qwen/Qwen3-Embedding-0.6B"
    embedding_dimension: int = 1024
    model_max_seq_length: int = 1024
    
    # Device configuration (CPU)
    device: str = "cpu" 
    
    # Task description for Qwen model instruction
    task_description: str = "Retrieve relevant legal document fragments including text, image descriptions, and table content that match the query"
    
    # RAG configuration
    max_chunks: int = 5
    
    # Application configuration
    app_name: str = "DOF Chat"
    debug: bool = True
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()