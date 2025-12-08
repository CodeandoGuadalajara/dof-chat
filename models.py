"""Database models for authentication using SQLModel."""

from datetime import datetime, timezone
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime
from typing import Optional


class User(SQLModel, table=True):
    """Local user with classic authentication."""
    
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    username: Optional[str] = Field(default=None, index=True)
    full_name: Optional[str] = None
    password_hash: Optional[str] = None
    is_active: bool = True
    is_superuser: bool = False
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True))
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True))
    )


# class OAuthAccount(SQLModel, table=True):
#     """Vinculación de cuentas OAuth (GitHub, etc.)."""
    
#     id: Optional[int] = Field(default=None, primary_key=True)
#     user_id: int = Field(foreign_key="user.id")
#     provider: str  # ej. "github"
#     provider_account_id: str
#     access_token: Optional[str] = None
#     refresh_token: Optional[str] = None
#     expires_at: Optional[datetime] = Field(
#         default=None,
#         sa_column=Column(DateTime(timezone=True), nullable=True)
#     )
#     created_at: datetime = Field(
#         default_factory=lambda: datetime.now(timezone.utc),
#         sa_column=Column(DateTime(timezone=True))
#     )
#     updated_at: datetime = Field(
#         default_factory=lambda: datetime.now(timezone.utc),
#         sa_column=Column(DateTime(timezone=True))
#     )
