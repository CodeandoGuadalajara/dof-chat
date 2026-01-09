from typing import List, Optional
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship, Column
from pgvector.sqlalchemy import Vector
from config import settings

class Document(SQLModel, table=True):
    __tablename__ = "documents"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    url: Optional[str] = Field(sa_column_kwargs={"unique": True})
    file_path: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    chunks: List["Chunk"] = Relationship(back_populates="document")

class Chunk(SQLModel, table=True):
    __tablename__ = "chunks"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    document_id: int = Field(foreign_key="documents.id")
    text: str
    header: Optional[str] = None
    chunk_number: int
    
    # Type annotation is List[float] for Pydantic compatibility,
    # but actual SQL column uses pgvector's Vector type
    embedding: List[float] = Field(sa_column=Column(Vector(settings.embedding_dimension)))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    document: Optional[Document] = Relationship(back_populates="chunks")
