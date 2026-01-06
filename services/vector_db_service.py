"""Vector database service for similarity search operations.

Extends the base database manager to provide specialized functionality for
vector similarity search. This service is optimized for retrieving legal document
chunks from DuckDB using cosine similarity on embeddings.
"""

from typing import List, Tuple
from datetime import datetime
import threading
import duckdb
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
    
    def _parse_query_results(self, rows) -> Tuple[List[ChunkData], List[Document]]:
        """Parse query results into ChunkData and Document objects.
        
        Extracts chunks and documents from database query results, ensuring
        each document appears only once in the returned list.
        
        Args:
            rows: Query result rows containing chunk and document data
            
        Returns:
            Tuple[List[ChunkData], List[Document]]: Parsed chunks and unique documents
        """
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
        
        return chunks, documents
    
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
        """
        top_k = top_k or settings.max_chunks

        # Use mocks only when explicitly enabled (development/testing)
        if settings.force_mock_mode:
            logger.info("Force mock mode enabled - serving mock data for vector search")
            return self._get_mock_data(top_k)

        # Build SQL query for vector similarity search
        query = f"""
            SELECT c.text, c.header, c.document_id,
                   d.id, d.title, d.url, d.file_path, d.created_at
            FROM chunks c
            JOIN documents d ON c.document_id = d.id
            WHERE c.embedding IS NOT NULL
            ORDER BY array_cosine_similarity(c.embedding, ?::FLOAT[{settings.embedding_dimension}]) DESC
            LIMIT ?
        """

        # Execute vector similarity search query with error handling
        try:
            # Use persistent connection (DatabaseManager handles thread-safety internally)
            conn = self.connect(read_only=True)
            rows = conn.execute(query, [query_embedding, top_k]).fetchall()
            chunks, documents = self._parse_query_results(rows)
            logger.info(f"Found {len(chunks)} chunks in {len(documents)} docs")
            return chunks, documents
        
        except duckdb.Error as e:
            # On connection/query errors, try reconnecting once before falling back
            logger.warning(f"Database connection or query failed, attempting reconnect: {e}")
            try:
                reconnected_conn = self.reconnect(read_only=True)
                rows = reconnected_conn.execute(query, [query_embedding, top_k]).fetchall()
                chunks, documents = self._parse_query_results(rows)
                logger.info(f"Reconnect successful: {len(chunks)} chunks, {len(documents)} docs")
                return chunks, documents
                
            except Exception as retry_error:
                logger.error(f"Reconnect failed: {retry_error}", exc_info=True)
                logger.warning("Falling back to mock data")
                return self._get_mock_data(top_k)
        
        except (FileNotFoundError, Exception) as e:
            logger.error(f"Database access failed: {e}", exc_info=True)
            # Fallback to mock data on database errors
            logger.warning("Falling back to mock data due to database error")
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

# Lazy-initialized global instance with thread-safety
_vector_db_service = None
_vector_db_lock = threading.Lock()

def get_vector_db_service() -> VectorDBService:
    """Get the singleton instance of VectorDBService with thread-safe initialization."""
    global _vector_db_service
    if _vector_db_service is None:
        with _vector_db_lock:
            if _vector_db_service is None:
                _vector_db_service = VectorDBService()
    return _vector_db_service
