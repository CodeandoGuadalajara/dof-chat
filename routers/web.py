import air
import airclerk
from pages.index import index_page
from pages.conversation_new import ConversationNewPage
from pages.login import login_page

# Initialize Air router
router = air.AirRouter()


@router.get("/login")
async def login(request: air.Request, next: str = "/"):
    """Serve the custom login page."""
    return await login_page(request, next)


@router.page
def demo(request: air.Request, user=airclerk.require_auth):
    """Serve the demo chatbot page."""
    # Pass user to demo_page to support showing user info/logout button
    return demo_page(request, user)

@router.page
def index():
    """Serve the home page redirecting to demo."""
    return IndexPage.render(demo_url=demo.url())
