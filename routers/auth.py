"""Authentication routes using GitHub OAuth via Air.

This module configures the GitHub OAuth flow using Air's built-in
`GitHubOAuthClientFactory` and exposes the router to be included by the app.

Environment variables (loaded through `config.Settings`):
- `GITHUB_CLIENT_ID`
- `GITHUB_CLIENT_SECRET`

The OAuth flow will expose routes like:
- `GET /account/github/login` (initiate login)
- `GET /account/github/callback` (OAuth callback)

On successful authentication, the user's GitHub access token is stored
in the session under `github_access_token`.
"""

from datetime import datetime, timezone
import secrets
from typing import Optional, Callable, Tuple
import air
import airsqlmodel as sql
import bcrypt
from config import settings
from fastapi import HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from models import User, OAuthAccount


async def get_db_session():
    """Dependency to get async database session with correct URL."""
    async for session in sql.get_async_session(url=settings.database_url):
        yield session


def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its bcrypt hash."""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )


def generate_csrf_token() -> str:
    """Generate a unique CSRF token."""
    return secrets.token_urlsafe(32)


async def authenticate_user(
    session: AsyncSession,
    identifier: str,
    password: str,
    by_username: bool = False,
) -> Tuple[Optional[User], Optional[str]]:
    """Authenticate a user by email or username.

    Returns a tuple (user, reason) where `user` is the authenticated User
    or `None` on failure, and `reason` is one of:
      - None: success
      - 'not_found'
      - 'invalid_password'
      - 'inactive'
    """
    if by_username:
        stmt = select(User).where(User.username == identifier)
    else:
        stmt = select(User).where(User.email == identifier)

    result = await session.exec(stmt)
    user = result.first()

    if not user:
        return None, "not_found"

    if not verify_password(password, user.password_hash or ""):
        return None, "invalid_password"

    if not user.is_active:
        return None, "inactive"

    return user, None


# async def github_process_callable(request: air.Request, token: dict, client: str = "") -> None:
#     """Process GitHub user token after OAuth login.

#     Creates or updates a User and OAuthAccount in the database,
#     and stores user info in the session for later use.
#     """
#     access_token = token.get("access_token", "")
#     if not access_token:
#         return

#     # For demo purposes, use a placeholder GitHub user ID
#     # In production, we will call the GitHub API to get the real user information
#     github_user_id = token.get("user_id", f"github_user_{access_token[:8]}")
    
#     async for session in sql.get_async_session(url=settings.database_url):
#         # Search for existing OAuth account
#         result = await session.exec(
#             select(OAuthAccount).where(
#                 OAuthAccount.provider == "github",
#                 OAuthAccount.provider_account_id == str(github_user_id)
#             )
#         )
#         oauth_account = result.first()
        
#         if not oauth_account:
#             # Create new user and oauth account
#             user = User(
#                 email=f"github_{github_user_id}@github.com",
#                 username=f"github_user_{github_user_id}",
#                 is_active=True
#             )
#             session.add(user)
#             await session.commit()
#             await session.refresh(user)
            
#             # Create OAuth account linked to the new user
#             oauth_account = OAuthAccount(
#                 user_id=user.id,
#                 provider="github",
#                 provider_account_id=str(github_user_id),
#                 access_token=access_token
#             )
#             session.add(oauth_account)
#             await session.commit()
#         else:
#             # Update existing OAuth account's access token
#             oauth_account.access_token = access_token
#             oauth_account.updated_at = datetime.now(timezone.utc)
#             session.add(oauth_account)
#             await session.commit()
            
#         # Get the user associated with this OAuth account
#         user = await session.get(User, oauth_account.user_id)
        
#         if user:
#             # Save user in session
#             request.session["user"] = {"id": user.id, "email": user.email}
    
#     # Also persist GitHub token for backward compatibility
#     request.session["github_access_token"] = access_token


# # Configure GitHub OAuth client using settings from .env
# github_oauth_client = air.ext.auth.GitHubOAuthClientFactory(
#     github_client_id=settings.github_client_id,
#     github_client_secret=settings.github_client_secret,
#     github_process_callable=github_process_callable,
#     login_redirect_to=settings.oauth_login_redirect,
# )


# Expose the router for inclusion in the main app
# Note: GitHub OAuth is commented out for now
# router = github_oauth_client.router


def require_login(request: air.Request):
    """Validate that user is authenticated.
    
    Checks if user is logged in by verifying session data.
    
    Returns:
        dict: User data from session
        
    Raises:
        HTTPException: 307 redirect to /login if not authenticated
    """
    # Check for user authentication in session
    user = request.session.get("user") if hasattr(request, "session") else None
    
    if not user:
        # Redirect if not logged in
        raise HTTPException(
            status_code=307,
            headers={"Location": "/login"}
        )
    
    return user


# Legacy GitHub OAuth authentication (commented out for future use)
# def require_login(request: air.Request):
#     """Validate that user is authenticated (local or GitHub).
#     
#     This unified function checks for both local authentication (user in session)
#     and GitHub OAuth (github_access_token in session).
#     
#     Returns:
#         dict: User data from session or GitHub indicator
#         
#     Raises:
#         HTTPException: 307 redirect to /login if not authenticated
#     """
#     # Check for local user authentication
#     user = request.session.get("user")
#     
#     if not user:
#         # If no local user, check for GitHub authentication
#         github_token = request.session.get("github_access_token")
#         if not github_token:
#             # Not authenticated by any method, redirect to login
#             raise HTTPException(
#                 status_code=307,
#                 headers={"Location": "/login"}
#             )
#         # Return GitHub authentication indicator
#         return {"source": "github", "token": github_token}
#     
#     # Return local user data
#     return user