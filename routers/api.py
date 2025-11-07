"""API routes for chat functionality.

FastAPI router for DOF Chat REST endpoints with RAG pipeline integration.
Uses FastAPI (not Air) for proper JSON serialization of accordion HTML responses.

Endpoints:
- POST /v1/chat: Main chat endpoint with RAG pipeline
- GET /v1/health: Service health check
"""

from fastapi import APIRouter, Depends, HTTPException
from schemas import ChatQuery, EnrichedChatResponse, HealthCheck
from rag_service import RAGService, get_rag_service
from utils.logger import logger

# Initialize FastAPI router with API prefix for better JSON compatibility
router = APIRouter(prefix="/v1", tags=["chat"])


@router.post("/chat", response_model=EnrichedChatResponse)
async def handle_chat(
    query: ChatQuery,
    rag_service: RAGService = Depends(get_rag_service)
) -> EnrichedChatResponse:
    """Handle chat queries using RAG service with enriched context.
    
    Processes user questions through RAG pipeline and returns responses
    with accordion HTML context for frontend rendering.
    
    Args:
        query: ChatQuery object with validated user text
        rag_service: Injected singleton RAG service instance
        
    Returns:
        EnrichedChatResponse: Complete response with answer and accordion HTML
        
    Raises:
        HTTPException: 500 if RAG pipeline fails
    """
    try:
        logger.info(f"Processing chat query: {query.text[:50]}...")
        
        # Process query through RAG pipeline
        response = rag_service.query(query.text)
        
        logger.info(f"Generated enriched response with {len(response.sources)} sources")
        return response
        
    except Exception as e:
        logger.error(f"Chat handling failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/health", response_model=HealthCheck)
async def health_check() -> HealthCheck:
    """Health check endpoint.
    
    Returns:
        HealthCheck: Service health status information
    """
    return HealthCheck()