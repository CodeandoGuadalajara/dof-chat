"""Web routes for serving HTML pages."""

import air
from pages.conversation_new import ConversationNewPage
# from pages.login import LoginPage
from pages.index import IndexPage

# Initialize Air router
router = air.AirRouter()

@router.page
def demo():
    """Serve the demo chatbot page."""
    return ConversationNewPage.render()

# @router.page 
# def login():
#     """Serve the login page."""
#     return LoginPage.render()

@router.page
def index():
    """Serve the home page redirecting to demo."""
    return IndexPage.render(demo_url=demo.url())