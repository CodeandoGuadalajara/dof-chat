"""Script to initialize the authentication database."""

import asyncio
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from models import User
from config import Settings

# Load settings
settings = Settings()

# Create async engine
engine = create_async_engine(
    settings.database_url,
    echo=settings.auth_echo,
)


async def create_db_and_tables():
    """Create all database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def main():
    print("Initializing authentication database...")
    await create_db_and_tables()
    print("Database initialized successfully!")
    print(f"Database location: {settings.database_url}")


if __name__ == "__main__":
    asyncio.run(main())
