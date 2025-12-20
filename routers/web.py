"""Web routes for serving HTML pages."""

import air
import airclerk
from pages.conversation_new import ConversationNewPage
from pages.login import LoginPage
from pages.index import IndexPage

# Initialize Air router
router = air.AirRouter()


@router.get("/login")
async def login(request: air.Request, next: str = "/"):
    """Serve the login page with Clerk authentication."""
    return await LoginPage.render_async(request, next)


@router.page
def demo(request: air.Request, user=airclerk.require_auth):
    """Serve the demo chatbot page (requires authentication)."""
    return ConversationNewPage.render(user=user)


@router.page
def index():
    """Serve the home page redirecting to demo."""
    return IndexPage.render(demo_url=demo.url())
