"""Vector database service for similarity search operations.

Extends the base database manager to provide specialized functionality for
vector similarity search. This service is optimized for retrieving legal document
chunks from DuckDB using cosine similarity on embeddings.
"""

from typing import List, Tuple
from datetime import datetime
from database import DatabaseManager
from schemas import ChunkData, Document
from config import settings
from utils.logger import logger

class VectorDBService(DatabaseManager):
    """Service for vector similarity search operations.
    
    Inherits from DatabaseManager to reuse connection logic.
    Provides methods to search for document chunks that are semantically
    similar to a query embedding.
    """
    
    def __init__(self, db_path: str = None):
        """Initialize the vector database service.
        
        Args:
            db_path: Optional path to the DuckDB database file.
        """
        super().__init__(db_path)
        self._is_healthy = True  # Circuit breaker flag
    
    def search_similar_chunks(self, query_embedding: List[float], top_k: int = None) -> Tuple[List[ChunkData], List[Document]]:
        """Search for chunks with cosine similarity close to the query embedding.
        
        Executes an optimized SQL query using DuckDB's array_cosine_similarity function
        to find the most relevant document chunks. Joins with the documents table
        to return complete context.
        
        Args:
            query_embedding: A list of floats representing the query vector.
            top_k: The number of most similar chunks to retrieve. Defaults to settings.max_chunks.
            
        Returns:
            Tuple[List[ChunkData], List[Document]]: A tuple containing:
                - List of matching ChunkData objects.
                - List of unique Document objects associated with those chunks.
                
        Note:
            Returns mock data if the database query fails.
            Implements a circuit breaker: after the first failure, it switches to mock-only mode.
        """
        top_k = top_k or settings.max_chunks
        
        # If developer forces mock mode in config, always return mock data
        if getattr(settings, "force_mock_mode", False):
            logger.info("Force mock mode enabled - serving mock data for vector search")
            return self._get_mock_data(top_k)

        # Circuit breaker: If DB previously failed, use mocks immediately without retrying SQL
        if not self._is_healthy:
            return self._get_mock_data(top_k)
        
        try:
            conn = self.connect()
            
            # Optimized query: Fetch chunks + doc info in one shot
            query = f"""
                SELECT c.text, c.header, c.document_id,
                       d.id, d.title, d.url, d.file_path, d.created_at
                FROM chunks c
                JOIN documents d ON c.document_id = d.id
                WHERE c.embedding IS NOT NULL
                ORDER BY array_cosine_similarity(c.embedding, ?::FLOAT[{settings.embedding_dimension}]) DESC
                LIMIT ?
            """
            
            rows = conn.execute(query, [query_embedding, top_k]).fetchall()
            
            chunks = []
            documents = []
            seen_docs = set()
            
            for row in rows:
                text, header, doc_id, d_id, d_title, d_url, d_path, d_date = row
                
                chunks.append(ChunkData(text=text or "", header=header or "", document_id=doc_id))
                
                if d_id not in seen_docs:
                    documents.append(Document(
                        id=d_id, title=d_title or "", url=d_url, 
                        file_path=d_path, created_at=d_date
                    ))
                    seen_docs.add(d_id)
            
            logger.info(f"Found {len(chunks)} chunks in {len(documents)} docs")
            return chunks, documents

        except Exception as e:
            logger.warning(f"Vector search failed (disabling DB, using mocks). Error: {e}")
            self._is_healthy = False
            return self._get_mock_data(top_k)

    def _get_mock_data(self, top_k: int) -> Tuple[List[ChunkData], List[Document]]:
        """Provide mock data when DB is unavailable.
        
        Used as a fallback mechanism to ensure the application remains responsive
        even if the vector database is unreachable or has schema issues.
        
        Args:
            top_k: The number of mock chunks to generate.
            
        Returns:
            Tuple[List[ChunkData], List[Document]]: Mock chunks and documents.
        """
        logger.info("Serving mock data")
        
        # Mock Documents
        docs = [
            Document(id=1, title="LEY_ISR_2024", url="https://dof.gob.mx/isr", file_path="/docs/isr.pdf", created_at=datetime.now()),
            Document(id=2, title="REGLAMENTO_SALUD", url="https://dof.gob.mx/salud", file_path="/docs/salud.pdf", created_at=datetime.now())
        ]
        
        # Mock Chunks linked to docs
        chunks = [
            ChunkData(text="Artículo 1 Mock ISR...", header="Art 1 - Obligaciones", document_id=1),
            ChunkData(text="Artículo 5 Mock Salud...", header="Art 5 - Seguridad", document_id=2),
            ChunkData(text="Artículo 10 Mock Agrario...", header="Art 10 - Tierras", document_id=1)
        ]
        
        # Return slice based on top_k
        return chunks[:top_k], docs[:min(len(docs), top_k)]

# Global instance
vector_db_service = VectorDBService()

def get_vector_db_service() -> VectorDBService:
    """Get the singleton instance of VectorDBService."""
    return vector_db_service
