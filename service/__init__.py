"""Modular services for DOF Chat RAG system."""

from .embedding_service import EmbeddingService, get_embedding_service

__all__ = [
    "EmbeddingService",
    "get_embedding_service"
]