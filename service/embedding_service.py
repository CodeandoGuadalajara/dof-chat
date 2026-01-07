"""Embedding service for text vectorization using Qwen models.

Uses Qwen/Qwen3-Embedding-0.6B model for high-quality embeddings
optimized for legal document retrieval tasks.
"""

import threading
import random
from typing import List, Optional
import torch
from sentence_transformers import SentenceTransformer
from config import settings
from utils.logger import logger


class EmbeddingService:
    """Thread-safe singleton service for text embedding operations.

    Manages model initialization and inference with thread safety guarantees 
    using PyTorch inference mode and double-checked locking for instance creation.
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        # Thread-safe singleton pattern using double-checked locking
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    instance = super().__new__(cls)
                    # Initialize instance attributes once, under lock, to avoid races
                    instance.initialized = False
                    instance._model = None
                    instance._init_lock = threading.Lock()  # Lock for initialization only
                    cls._instance = instance
        return cls._instance
    
    def __init__(self):
        # Initialization of singleton state is handled in __new__ to ensure thread safety.
        # __init__ is intentionally left as a no-op to avoid racing re-initialization.
        pass

    def initialize(self):
        """Load and configure the embedding model.

        Initializes the Qwen/Qwen3 model with settings optimized for legal retrieval.
        Thread-safe implementation ensuring single model loading.
        """
        # Fast path without lock
        if self.initialized:
            return
        
        # Slow path with lock for initialization
        with self._init_lock:
            # Double-check after acquiring lock
            if self.initialized:
                return
            
            # Check if mock mode is forced
            if settings.force_mock_mode:
                logger.info("Force mock mode enabled - skipping embedding model initialization")
                self._model = None
                self.initialized = True
                return
            
            try:
                logger.info(f"Loading embedding model: {settings.embedding_model}")
                
                # Initialize model with optimized config
                self._model = SentenceTransformer(
                    settings.embedding_model, 
                    truncate_dim=settings.embedding_dimension,
                    model_kwargs={"device_map": settings.device},
                    trust_remote_code=False
                )
                
                # Set sequence length limits
                self._model.max_seq_length = settings.model_max_seq_length
                if hasattr(self._model.tokenizer, 'model_max_length'):
                    self._model.tokenizer.model_max_length = settings.model_max_seq_length
                
                # Safely set max_position_embeddings if model structure allows
                try:
                    first_module = self._model[0]
                    if hasattr(first_module, 'max_position_embeddings'):
                        first_module.max_position_embeddings = settings.model_max_seq_length
                except (TypeError, IndexError, KeyError):
                    pass
                
                # Optimize model for inference
                self._model.to(settings.device)
                self._model.eval()
                torch.set_grad_enabled(False)
                
                self.initialized = True
                logger.info(f"Embedding service ready ({settings.device}, max_seq: {settings.model_max_seq_length})")
                
            except Exception as e:
                logger.error(f"Failed to initialize embedding service: {e}", exc_info=True)
                logger.warning("Falling back to mock embedding mode")
                self._model = None
                self.initialized = True
    
    def embed_query(self, text: str) -> List[float]:
        """Convert input text to a normalized embedding vector.

        Applies task-specific formatting and executes thread-safe inference.

        Args:
            text: Input query string.

        Returns:
            List[float]: L2-normalized embedding vector.
        """
        if not self.initialized:
            self.initialize()
        
        # Fallback to mock on load failure
        if self._model is None:
            logger.info(f"MOCK: Generating embedding for text: '{text[:50]}...'")
            return self._generate_mock_embedding(text)
        
        try:
            logger.info(f"REAL MODEL: Generating embedding for text: '{text[:50]}...'")
            
            # Apply task formatting
            formatted_text = f"query: {text}"
            if settings.task_description:
                formatted_text = f"{settings.task_description}: {text}"
            
            # Thread-safe inference mode
            with torch.inference_mode():
                embedding = self._model.encode(
                    formatted_text,
                    convert_to_numpy=True,
                    normalize_embeddings=True,  # L2 normalization for cosine similarity
                    show_progress_bar=False
                )
            
            # Serialize to list
            result = embedding.tolist()
            logger.info(f"Embedding generated successfully ({len(result)} dimensions)")
            return result
            
        except Exception as e:
            logger.error(f"Embedding generation failed: {e}", exc_info=True)
            logger.warning("Falling back to mock embedding")
            # Fall back to mock for robustness
            return self._generate_mock_embedding(text)
    
    def _generate_mock_embedding(self, text: str) -> List[float]:
        """Generate deterministic mock embedding for testing.

        Args:
            text: Input source text for seed generation.

        Returns:
            List[float]: Randomized vector with fixed seed.
        """
        random.seed(hash(text) % 2147483647)  # Deterministic based on text
        mock_embedding = [random.uniform(-0.1, 0.1) for _ in range(settings.embedding_dimension)]
        return mock_embedding
    
    def get_model_info(self) -> dict:
        """Retrieve current model configuration and status.

        Returns:
            dict: Metadata including status, model name, and parameters.
        """
        if not self.initialized:
            return {"status": "not_initialized"}
        
        if settings.force_mock_mode:
            return {"status": "forced_mock_mode", "reason": "force_mock_mode_enabled"}
        
        if self._model is None:
            return {"status": "mock_mode", "reason": "model_not_available"}
        
        return {
            "status": "ready",
            "model_name": settings.embedding_model,
            "device": settings.device,
            "max_seq_length": getattr(self._model, 'max_seq_length', 'unknown'),
            "embedding_dimension": settings.embedding_dimension
        }


# Global singleton instance (lazily instantiated)
embedding_service = None


def get_embedding_service() -> EmbeddingService:
    """Retrieve the initialized EmbeddingService singleton."""
    global embedding_service
    if embedding_service is None:
        embedding_service = EmbeddingService()
    
    if not embedding_service.initialized:
        embedding_service.initialize()
    return embedding_service