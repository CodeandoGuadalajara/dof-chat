"""Create a test user for authentication testing."""

import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from models import User
from routers.auth import get_password_hash
from config import settings

# Create async engine for this script
engine = create_async_engine(
    settings.database_url,
)

async def create_test_user():
    """Create a test user in the database."""
    async with AsyncSession(engine) as session:
        # Check if user already exists
        statement = select(User).where(User.email == "test@example.com")
        result = await session.exec(statement)
        existing_user = result.first()
        
        if existing_user:
            print("Test user already exists!")
            print(f"Email: {existing_user.email}")
            return
        
        # Create new test user
        test_user = User(
            email="test@example.com",
            username="testuser",
            full_name="Test User",
            password_hash=get_password_hash("password123"),
            is_active=True,
            is_superuser=False
        )
        
        session.add(test_user)
        await session.commit()
        await session.refresh(test_user)
        
        print("Test user created successfully!")
        print(f"Email: {test_user.email}")
        print(f"Username: {test_user.username}")
        print("Password: password123")
        print(f"User ID: {test_user.id}")


if __name__ == "__main__":
    asyncio.run(create_test_user())
