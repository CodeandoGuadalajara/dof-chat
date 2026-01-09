"""Service for vector database operations."""

from typing import List, Tuple
from datetime import datetime, timezone
from sqlmodel import select
from models import Chunk, Document
from database import get_readonly_session_context
from config import settings
from utils.logger import logger

class VectorService:
    """Service responsible for vector similarity searches."""
    
    async def search_similar_chunks(self, embedding: List[float], top_k: int = None) -> Tuple[List[Chunk], List[Document]]:
        """Search for chunks similar to the provided embedding vector.
        
        Args:
            embedding: The query embedding vector.
            top_k: Maximum number of results to return.
            
        Returns:
            Tuple containing:
            - List of matching Chunk objects.
            - List of unique Document objects associated with those chunks.
        """
        if top_k is None:
            top_k = settings.max_chunks
        
        # Mock mode support
        if settings.force_mock_mode:
            logger.info("Force mock mode enabled - serving mock data for vector search")
            return self._get_mock_data(top_k)
        
        logger.info(f"Starting vector search in database for top_k={top_k}")
            
        try:
            # Use read-only session with AUTOCOMMIT to avoid transaction overhead
            logger.debug("Obtaining read-only database session (AUTOCOMMIT)")
            async with get_readonly_session_context() as session:
                logger.debug("Database session acquired successfully")
                
                # Vector search using cosine distance
                # Join with Document to fetch metadata in one query
                logger.debug("Building vector similarity query with pgvector")
                statement = (
                    select(Chunk, Document)
                    .join(Document, Document.id == Chunk.document_id)
                    .order_by(Chunk.embedding.cosine_distance(embedding))
                    .limit(top_k)
                )
                
                logger.info("Executing vector similarity search query on PostgreSQL")
                results = await session.execute(statement)
                rows = results.all()
                logger.info(f"Database returned {len(rows)} matching chunks")
                
                chunks = []
                documents = []
                seen_docs = set()
                
                for chunk, doc in rows:
                    chunks.append(chunk)
                    if doc.id not in seen_docs:
                        documents.append(doc)
                        seen_docs.add(doc.id)
                
                logger.info(f"Processed results: {len(chunks)} chunks from {len(documents)} unique documents")
                
                return chunks, documents
                
        except Exception as e:
            logger.error(f"Vector search failed: {e}", exc_info=True)
            return [], []

    def _get_mock_data(self, top_k: int) -> Tuple[List[Chunk], List[Document]]:
        """Return mock chunks and documents for testing without database."""
        # Realistic mock data matching the DOF context
        
        # Mock Documents
        mock_docs_data = [
            {"id": 101, "title": "LEY DEL IMPUESTO SOBRE LA RENTA", "url": "https://dof.gob.mx/isr", "file_path": "/docs/isr.pdf"},
            {"id": 102, "title": "REGLAMENTO DE SEGURIDAD Y SALUD", "url": "https://dof.gob.mx/salud", "file_path": "/docs/salud.pdf"},
            {"id": 103, "title": "NOM-001-SEMARNAT-2021", "url": "https://dof.gob.mx/nom001", "file_path": "/docs/nom001.pdf"}
        ]
        
        documents = [
            Document(**data, created_at=datetime.now(timezone.utc)) 
            for data in mock_docs_data
        ]
        
        # Mock Chunks linked to docs
        mock_chunks_data = [
            {
                "id": 1,
                "text": "LEY DEL IMPUESTO SOBRE LA RENTA - Artículo 1.- Las personas físicas y las morales están obligadas al pago del impuesto sobre la renta en los siguientes casos: I.- Las residentes en México, respecto de todos sus ingresos, cualquiera que sea la ubicación de la fuente de riqueza de donde procedan.",
                "header": "Artículo 1 - Obligaciones fiscales generales",
                "chunk_number": 1,
                "document_id": 101
            },
            {
                "id": 2,
                "text": "REGLAMENTO DE SEGURIDAD Y SALUD EN EL TRABAJO - Artículo 5.- Los patrones deberán implementar un sistema de gestión de seguridad y salud en el trabajo que incluya la identificación de peligros y evaluación de riesgos.",
                "header": "Artículo 5 - Sistemas de gestión laboral",
                "chunk_number": 5,
                "document_id": 102
            },
            {
                "id": 3,
                "text": "NORMA Oficial Mexicana NOM-001-SEMARNAT-2021 - Que establece los límites máximos permisibles de contaminantes en las descargas de aguas residuales en aguas y bienes nacionales.",
                "header": "NOM-001-SEMARNAT-2021 - Límites de contaminantes",
                "chunk_number": 1,
                "document_id": 103
            }
        ]
        
        chunks = []
        for i, data in enumerate(mock_chunks_data[:top_k]):
            chunks.append(Chunk(
                id=data["id"],
                text=data["text"],
                header=data["header"],
                chunk_number=data["chunk_number"],
                document_id=data["document_id"],
                # Use correct method to generate list of floats for mock embedding
                embedding=[0.1 for _ in range(settings.embedding_dimension)]
            ))
        
        return chunks, documents
