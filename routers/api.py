"""API routes for chat functionality."""

import air
from fastapi import Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from schemas import ChatQuery, ChatResponse, HealthCheck
from rag_service import RAGService, get_rag_service
from routers.auth import get_db_session
from models import User
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


# Authentication API router
auth_router = air.AirRouter(prefix="/api/v1/auth", tags=["auth"])


@auth_router.get("/me")
async def me_json(
    request: air.Request,
    session: AsyncSession = Depends(get_db_session)
):
    """JSON endpoint to get current authenticated user.
    
    Returns user data from session or 401 if not authenticated.
    """
    user_data = request.session.get("user")
    if not user_data:
        return JSONResponse(
            status_code=401,
            content={"detail": "No autenticado"}
        )
    
    # Load full user data from database
    result = await session.exec(
        select(User).where(User.id == user_data["id"])
    )
    user = result.first()
    
    if not user:
        return JSONResponse(
            status_code=401,
            content={"detail": "Usuario no encontrado"}
        )
    
    return JSONResponse(
        content={
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "full_name": user.full_name
        }
    )