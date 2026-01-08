"""RAG service for document querying - Mock implementation for integration testing.

Mock RAG pipeline for DOF Chat: demonstrates component integration without real models.
Tests: query embedding → vector search → LLM generation → Air component rendering.

Current mode: Full simulation for testing component connectivity.
"""

import time
import random
import threading
from typing import List, Tuple
from config import settings
from services.vector_service import VectorService
from models import Document
from schemas import EnrichedChatResponse, ChunkData, DocumentSource
from utils.logger import logger
from utils.context_renderer import render_embedded_sources


class RAGService:
    """Mock RAG service for testing component integration.
    
    Thread-safe singleton pattern with mock implementations for all operations.
    Tests connectivity between components without real model dependencies.
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        # Double-checked locking pattern for thread safety
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        # Only initialize once using instance attribute check
        if not hasattr(self, '_initialized'):
            self._initialized = False
            self.vector_service = VectorService()
    
    def initialize(self):
        """Initialize service with mock implementations."""
        if self._initialized:
            return
        
        logger.info("Initializing RAG service (mock mode for embeddings/LLM)")
        
        # TODO: Initialize embedding model (Qwen/Qwen3-Embedding-0.6B)
        # TODO: Initialize Gemini API client
        # TODO: Validate API keys and model availability
        
        # Database connection is handled by AirSQLModel session pooling
        logger.info("Database connection configured via AirSQLModel")
        
        self._initialized = True
        logger.info("RAG service ready (mock embeddings/LLM, real database)")
    
    def embed_query(self, text: str) -> List[float]:
        """Convert query text to embedding vector (mock implementation).
        
        Args:
            text: Query text to embed
            
        Returns:
            List[float]: Mock embedding vector
        """
        if not self._initialized:
            self.initialize()
        
        # TODO: Replace with real embedding model (Qwen/Qwen3-Embedding-0.6B)
        # TODO: Initialize embedding model in initialize() method
        # TODO: Process text through real embedding model
        
        # Generate mock embedding for integration testing
        logger.debug(f"Processing embedding for text: '{text[:50]}...'")
        logger.info("MOCK: Generating fixed embedding vector")
        
        # Fixed mock embedding - results will be pseudo-random since DB has real embeddings
        random.seed(42)
        mock_embedding = [random.uniform(-0.1, 0.1) for _ in range(settings.embedding_dimension)]
        
        logger.debug(f"Generated mock embedding with {len(mock_embedding)} dimensions")
        return mock_embedding
    
    async def search_chunks(self, embedding: List[float], top_k: int = None) -> Tuple[List[ChunkData], List[Document]]:
        """Search for similar chunks using VectorService.
        
        Args:
            embedding: Query embedding vector
            top_k: Number of results to return
            
        Returns:
            Tuple[List[ChunkData], List[Document]]: Chunk data objects and their source documents
        """
        if top_k is None:
            top_k = settings.max_chunks
        
        logger.info(f"Initiating vector search for top_k={top_k} chunks")
        
        try:
            # Execute real vector search
            chunks, documents = await self.vector_service.search_similar_chunks(embedding, top_k)
            
            logger.info(f"Vector search completed: retrieved {len(chunks)} chunks from {len(documents)} documents")
            
            # Map database models to schema objects
            chunk_objects = []
            for chunk in chunks:
                chunk_obj = ChunkData(
                    text=chunk.text,
                    header=chunk.header or "Sección sin título",
                    document_id=chunk.document_id
                )
                chunk_objects.append(chunk_obj)
            
            logger.debug(f"Returning {len(chunk_objects)} chunks from vector search")
            return chunk_objects, documents
            
        except Exception as e:
            logger.error(f"Vector search failed: {e}", exc_info=True)
            return [], []
    
    def generate_answer(self, query: str, context_chunks: List[ChunkData]) -> str:
        """Generate answer (mock implementation).
        
        Args:
            query: User query
            context_chunks: Retrieved context chunks
            
        Returns:
            str: Mock generated answer text
        """
        # TODO: Replace with real Gemini API integration
        # TODO: Initialize Gemini client with API key
        # TODO: Build context prompt from chunks
        # TODO: Send query + context to Gemini and return response
        
        # Generate mock response for integration testing
        logger.debug(f"Generating answer for query: '{query[:50]}...'")
        logger.info("MOCK: Generating structured response")
        
        # Extract information from chunks for realistic simulation
        chunk_summaries = []
        for i, chunk in enumerate(context_chunks):
            chunk_summaries.append(f"• {chunk.header}")
        
        # Generate a realistic simulated response
        if context_chunks:
            simulated_answer = f"""Basándome en la información encontrada en los documentos del DOF, puedo ayudarte con tu consulta sobre: "{query}"

He encontrado {len(context_chunks)} documentos relevantes:
{chr(10).join(chunk_summaries)}

NOTA: Esta es una respuesta simulada para pruebas de integración. En el modo de producción, aquí se generaría una respuesta detallada utilizando inteligencia artificial basada en el contenido específico de los documentos encontrados.

Los documentos analizados contienen información oficial publicada en el Diario Oficial de la Federación que puede ser relevante para tu consulta.""".strip()
        else:
            simulated_answer = f"""No encontré documentos específicos relacionados con tu consulta: "{query}"

NOTA: Esta es una respuesta simulada para pruebas de integración. En el modo de producción, el sistema buscaría en la base de datos completa de documentos del DOF y proporcionaría información relevante o sugerencias alternativas.""".strip()
        
        logger.debug(f"Generated response with {len(simulated_answer)} characters")
        return simulated_answer
    
    async def query(self, text: str) -> EnrichedChatResponse:
        """Complete RAG pipeline from user query to enriched response with accordion HTML.
        
        Pipeline: text → embedding → search → generate → structure → render → JSON response
        Handles errors gracefully and returns user-friendly responses on failures.
        
        Args:
            text: User query in natural language (Spanish)
            
        Returns:
            EnrichedChatResponse: Complete response with answer, context HTML, and sources
        """
        try:
            logger.info(f"Starting RAG pipeline for query: '{text[:50]}...'")
            
            if not self._initialized:
                logger.info("Initializing RAG service")
                self.initialize()
            
            # Step 1: Embed query
            embedding = self.embed_query(text)
            
            # Step 2: Search for relevant chunks and documents
            chunks, documents = await self.search_chunks(embedding)
            
            # Step 3: Generate answer
            answer = self.generate_answer(text, chunks)
            
            # Step 4: Create document sources for context rendering
            document_sources = self._create_document_sources(chunks, documents)
            
            # Step 5: Render context HTML using Air components
            query_id = f"q{int(time.time())}"
            context_component = render_embedded_sources(document_sources, query_id)
            
            # Render Air component to HTML string - ensure it's a proper string
            if context_component:
                try:
                    rendered_html = context_component.render()
                    # Ensure we have a proper string, not an Air object
                    context_html = str(rendered_html) if rendered_html else ""
                    logger.debug(f"Successfully rendered context HTML: {len(context_html)} chars")
                except Exception as e:
                    logger.error(f"Failed to render Air component: {e}")
                    context_html = ""
            else:
                context_html = ""
                logger.warning("No context component generated")
            
            # Step 6: Extract simple sources list as fallback
            sources = [chunk.header for chunk in chunks if chunk.header]
            
            # Create enriched response
            response = EnrichedChatResponse(
                answer=answer,
                context_html=context_html,
                sources=sources
            )
            
            logger.info(f"RAG pipeline completed - Answer: {len(answer)} chars, Context HTML: {len(context_html)} chars, Sources: {len(sources)}")
            
            return response
            
        except Exception as e:
            # Log detailed error with stack trace for debugging
            logger.error(f"Query processing failed: {e}", exc_info=True)
            
            # Return generic user-friendly error message
            return EnrichedChatResponse(
                answer="Lo siento, hubo un error al procesar tu consulta. Por favor, inténtalo de nuevo más tarde.",
                context_html="",
                sources=[]
            )
    
    def _create_document_sources(self, chunks: List[ChunkData], documents: List[Document]) -> List[DocumentSource]:
        """Create DocumentSource objects from ChunkData for Air rendering.
        
        Groups chunks by document ID and creates structured DocumentSource objects
        with metadata for accordion display.
        
        Args:
            chunks: List of chunk data objects
            documents: List of Document objects retrieved from the database
            
        Returns:
            List[DocumentSource]: Document sources grouped by document ID
        """
        # Create lookup map: document_id -> Document (for titles, URLs, dates)
        doc_map = {d.id: d for d in documents}

        # Group chunks by their source document id (only valid document_ids)
        doc_groups = {}
        orphan_chunks = []  # Chunks without valid document_id
        
        for chunk in chunks:
            doc_id = chunk.document_id
            if doc_id is None or doc_id not in doc_map:
                # Collect orphan chunks separately
                orphan_chunks.append(chunk)
            else:
                if doc_id not in doc_groups:
                    doc_groups[doc_id] = []
                doc_groups[doc_id].append(chunk)

        document_sources = []
        
        # Process chunks with valid documents
        for doc_id, doc_chunks in doc_groups.items():
            doc = doc_map[doc_id]
            title = doc.title or f"Documento {doc.id}"
            
            # Format date for display (age metadata to be calculated later)
            pub_date = doc.created_at.isoformat() if doc.created_at else None
            age_desc = None
            age_emoji = None
            
            url = doc.url

            doc_source = DocumentSource(
                title=title,
                chunks=doc_chunks,
                url=url,
                publication_date=pub_date,
                age_description=age_desc,
                age_emoji=age_emoji,
                metadata={"document_id": doc_id}
            )
            document_sources.append(doc_source)
        
        # Handle orphan chunks if any exist
        if orphan_chunks:
            doc_source = DocumentSource(
                title="Documentos sin identificar",
                chunks=orphan_chunks,
                url=None,
                publication_date=None,
                age_description=None,
                age_emoji=None,
                metadata={"orphaned": True}
            )
            document_sources.append(doc_source)

        return document_sources


# Global RAG service singleton
rag_service = RAGService()


def get_rag_service() -> RAGService:
    """Get the RAG service singleton instance (mock implementation)."""
    if not rag_service._initialized:
        rag_service.initialize()
    return rag_service