"""Configuration module for dof-chat application."""

from pydantic import field_validator
try:
    from pydantic_settings import BaseSettings
except ImportError:
    # Fallback for older pydantic versions or missing pydantic-settings
    from pydantic import BaseModel as BaseSettings

class Settings(BaseSettings):
    """Application settings using Pydantic Settings."""
    
    # Database configuration
    database_path: str = "dof_db/db.duckdb"
    
    # Gemini API configuration
    # TODO: Enable API key validation for production deployment
    # For development, allow empty API key to test system without real Gemini calls
    gemini_api_key: str = ""  # Will use mock responses in development
    gemini_model: str = "gemini-1.5-flash"
    
    # NOTE: Uncomment validator below for production deployment
    # @field_validator('gemini_api_key')
    # @classmethod
    # def validate_gemini_api_key(cls, v):
    #     """Validate that Gemini API key is provided and not empty."""
    #     if not v or v.strip() == "":
    #         raise ValueError(
    #             "Gemini API key is required. Please set GEMINI_API_KEY environment variable "
    #             "or provide it in the .env file. Get your API key from: "
    #             "https://makersuite.google.com/app/apikey"
    #         )
    #     return v.strip()
    
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
    session_secret_key: str = "change-me-in-production"
    
    @field_validator('session_secret_key')
    @classmethod
    def validate_session_secret(cls, v):
        """Warn if using default session secret in production."""
        if v == "change-me-in-production" and not cls.model_config.get("debug", True):
            import warnings
            warnings.warn(
                "Using default session secret key in production. "
                "Please set SESSION_SECRET_KEY environment variable with a secure random value.",
                UserWarning
            )
        return v
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()