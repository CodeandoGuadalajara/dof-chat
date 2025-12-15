"""API routes for chat functionality."""

import air
from fastapi import Depends, HTTPException
from fastapi.responses import JSONResponse
from schemas import ChatQuery, ChatResponse, HealthCheck
from rag_service import RAGService, get_rag_service
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Initialize Air router with API prefix
router = air.AirRouter(prefix="/api/v1", tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
async def handle_chat(
    query: ChatQuery,
    rag_service: RAGService = Depends(get_rag_service)
) -> ChatResponse:
    """Handle chat queries using RAG service.
    
    Args:
        query: User query containing text
        rag_service: RAG service dependency
        
    Returns:
        Chat response with answer and sources
        
    Raises:
        HTTPException: If query processing fails
    """
    try:
        logger.info(f"Processing chat query: {query.text[:50]}...")
        
        # Process query through RAG pipeline
        response = rag_service.query(query.text)
        
        logger.info(f"Generated response with {len(response.sources)} sources")
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
        Health status information
    """
    return HealthCheck()