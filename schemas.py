"""Pydantic schemas for API endpoints."""

from pydantic import BaseModel, Field
from typing import List


class ChatQuery(BaseModel):
    """Schema for chat query requests."""
    
    text: str = Field(
        ..., 
        min_length=1, 
        max_length=1000,
        description="User question or query text"
    )


class ChatResponse(BaseModel):
    """Schema for chat response."""
    
    answer: str = Field(
        ...,
        description="Generated answer based on retrieved context"
    )
    sources: List[str] = Field(
        default_factory=list,
        description="List of source document headers or references"
    )
    
    
class HealthCheck(BaseModel):
    """Schema for health check response."""
    
    status: str = Field(default="ok")
    service: str = Field(default="dof-chat")
    version: str = Field(default="0.1.0")