"""Configuration module for dof-chat application."""

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Application settings using Pydantic Settings."""
    
    # Pydantic Settings v2 config
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )
    
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
    similarity_threshold: float = 0.7
    
    # Application configuration
    app_name: str = "DOF Chat"
    debug: bool = True

    # Session configuration
    # Only if .env is missing or the variable is not defined, 
    # the default value "change-me" will be used.
    session_secret_key: str = "change-me"

    # OAuth (GitHub) configuration
    github_client_id: str = ""
    github_client_secret: str = ""
    oauth_login_redirect: str = "/demo"
    
    # Authentication database configuration
    auth_echo: bool = False  # Debug SQL queries
    
    # AirSQLModel async database configuration
    database_url: str = "sqlite+aiosqlite:///./auth.db"
    
    # No nested Config; model_config above handles env loading


# Global settings instance
settings = Settings()