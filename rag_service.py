"""RAG service for document querying - Mock implementation for integration testing.

Mock RAG pipeline for DOF Chat: demonstrates component integration without real models.
Tests: query embedding → vector search → LLM generation → Air component rendering.

Current mode: Full simulation for testing component connectivity.
"""

import time
import threading
from typing import List
from config import settings
from database import db_manager
from schemas import EnrichedChatResponse, ChunkData, DocumentSource
from utils.logger import logger
from utils.context_renderer import render_embedded_sources
from service.embedding_service import get_embedding_service


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
    
    def initialize(self):
        """Initialize service with mock implementations."""
        if self._initialized:
            return
        
        logger.info("Initializing RAG service (mock mode)")
        
        # Initialize embedding model (Qwen/Qwen3-Embedding-0.6B)
        try:
            self.embedding_service = get_embedding_service()
            logger.info("Embedding service initialized successfully")
        except Exception as e:
            logger.warning(f"Embedding service initialization failed: {e}, will use mock")
            self.embedding_service = None
        
        # TODO: Initialize Gemini API client
        # TODO: Validate API keys and model availability
        
        # Test database connection (only connectivity, no model loading)
        try:
            db_result = db_manager.test_connection()
            if db_result["status"] == "success":
                logger.info("Database connected")
            else:
                logger.warning("Database connection failed, continuing with mocks")
        except Exception as e:
            logger.warning(f"Database test failed: {e}, continuing with mocks")
        
        self._initialized = True
        logger.info("RAG service ready (mock mode)")
    
    def search_chunks(self, embedding: List[float], top_k: int = None) -> List[ChunkData]:
        """Search for similar chunks (mock implementation).
        
        Args:
            embedding: Query embedding vector (unused in mock)
            top_k: Number of results to return
            
        Returns:
            List[ChunkData]: Mock document chunks with realistic data
        """
        if top_k is None:
            top_k = settings.max_chunks
        
        # TODO: Replace with real DuckDB vector search
        # TODO: Execute vector similarity search against embeddings table
        # TODO: Return real chunks from database with metadata
        
        # Generate mock chunks for integration testing
        logger.debug(f"Searching for {top_k} similar chunks")
        logger.info("MOCK: Returning predefined document chunks")
        
        mock_chunks_data = [
            {
                "text": "LEY DEL IMPUESTO SOBRE LA RENTA - Artículo 1.- Las personas físicas y las morales están obligadas al pago del impuesto sobre la renta en los siguientes casos: I.- Las residentes en México, respecto de todos sus ingresos, cualquiera que sea la ubicación de la fuente de riqueza de donde procedan.",
                "header": "Artículo 1 - Obligaciones fiscales generales",
                "doc_type": "LEY"
            },
            {
                "text": "REGLAMENTO DE SEGURIDAD Y SALUD EN EL TRABAJO - Artículo 5.- Los patrones deberán implementar un sistema de gestión de seguridad y salud en el trabajo que incluya la identificación de peligros y evaluación de riesgos.",
                "header": "Artículo 5 - Sistemas de gestión laboral",
                "doc_type": "REGLAMENTO"
            },
            {
                "text": "NORMA Oficial Mexicana NOM-001-SEMARNAT-2021 - Que establece los límites máximos permisibles de contaminantes en las descargas de aguas residuales en aguas y bienes nacionales.",
                "header": "NOM-001-SEMARNAT-2021 - Límites de contaminantes",
                "doc_type": "NORMA"
            }
        ]
        
        # Convert to ChunkData objects
        chunk_objects = []
        for chunk_data in mock_chunks_data[:top_k]:
            chunk_obj = ChunkData(
                text=chunk_data["text"],
                header=chunk_data["header"],
                doc_type=chunk_data["doc_type"]
            )
            chunk_objects.append(chunk_obj)
        
        logger.debug(f"Returning {len(chunk_objects)} mock ChunkData objects")
        return chunk_objects
    
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
            chunk_summaries.append(f"• {chunk.doc_type}: {chunk.header}")
        
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
    
    def query(self, text: str) -> EnrichedChatResponse:
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
            
            # Ensure embedding service is available before using it
            if self.embedding_service is None:
                logger.error("Embedding service is not available after initialization")
                raise RuntimeError("Embedding service is not available")
            
            # Step 1: Embed query
            embedding = self.embedding_service.embed_query(text)
            
            # Step 2: Search for relevant chunks
            chunks = self.search_chunks(embedding)
            
            # Step 3: Generate answer
            answer = self.generate_answer(text, chunks)
            
            # Step 4: Create document sources for context rendering
            document_sources = self._create_document_sources(chunks)
            
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
    
    def _create_document_sources(self, chunks: List[ChunkData]) -> List[DocumentSource]:
        """Create DocumentSource objects from ChunkData for Air rendering.
        
        Groups chunks by document type and creates structured DocumentSource objects
        with metadata for accordion display.
        
        Args:
            chunks: List of chunk data objects
            
        Returns:
            List[DocumentSource]: Document sources grouped by type
        """
        # Group chunks by document type for realistic simulation
        doc_groups = {}
        for chunk in chunks:
            doc_key = chunk.doc_type
            if doc_key not in doc_groups:
                doc_groups[doc_key] = []
            doc_groups[doc_key].append(chunk)
        
        # Create DocumentSource objects
        document_sources = []
        for doc_type, doc_chunks in doc_groups.items():
            # Create realistic document metadata
            if doc_type == "LEY":
                title = "Ley del Impuesto Sobre la Renta"
                pub_date = "15 de enero de 2024"
                age_desc = "Reciente"
                age_emoji = "🟢"
                url = "https://dof.gob.mx/nota_detalle.php?codigo=5678901"
            elif doc_type == "REGLAMENTO":
                title = "Reglamento de Seguridad y Salud en el Trabajo"
                pub_date = "20 de febrero de 2024"
                age_desc = "Reciente"
                age_emoji = "🟢"
                url = "https://dof.gob.mx/nota_detalle.php?codigo=5678902"
            else:  # NORMA
                title = "NOM-001-SEMARNAT-2021"
                pub_date = "10 de marzo de 2024"
                age_desc = "Reciente"
                age_emoji = "🟢"
                url = "https://dof.gob.mx/nota_detalle.php?codigo=5678903"
            
            doc_source = DocumentSource(
                title=title,
                chunks=doc_chunks,
                url=url,
                publication_date=pub_date,
                age_description=age_desc,
                age_emoji=age_emoji,
                metadata={"doc_type": doc_type}
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