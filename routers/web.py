"""Web routes for serving HTML pages."""

import air
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from routers.auth import require_login, get_db_session, authenticate_user
from pages.index import index_page
from pages.demo import demo_page
from pages.login import login_page

# Initialize Air router
router = air.AirRouter()

@router.page
def demo(request: air.Request, _auth = Depends(require_login)):
    """Serve the demo chatbot page."""
    return demo_page(request)

@router.page
def index():
    """Serve the home page redirecting to demo."""
    return index_page(demo.url())
    
@router.get("/login", tags=["auth"])
def login(request: air.Request):
    """Serve the login page."""
    return login_page(request)


@router.post("/login", tags=["auth"])
async def login_form(
    request: air.Request,
    session: AsyncSession = Depends(get_db_session)
):
    """Process HTML login form submission."""
    # Minimal orchestration: validate CSRF, delegate authentication to service
    form_data = await request.form()
    csrf_token = form_data.get("csrf_token")

    # Validate CSRF token
    if csrf_token != request.session.get("csrf_token"):
        request.session["error_message"] = "Token de seguridad inválido. Por favor, intenta nuevamente."
        return air.responses.RedirectResponse("/login", status_code=303)

    email = form_data.get("email")
    password = form_data.get("password")

    if not email or not password:
        request.session["error_message"] = "Por favor, proporciona email y contraseña."
        return air.responses.RedirectResponse("/login", status_code=303)

    # Delegate auth logic to service helper
    user, reason = await authenticate_user(session, email, password)
    if not user:
        request.session["error_message"] = "Email o contraseña incorrectos."
        return air.responses.RedirectResponse("/login", status_code=303)

    # Save user in session and redirect
    request.session["user"] = {"id": user.id, "email": user.email}
    request.session.pop("csrf_token", None)
    request.session.pop("error_message", None)  # Clear any error messages
    return air.responses.RedirectResponse("/demo", status_code=302)


@router.get("/logout", tags=["auth"])
async def logout(request: air.Request):
    """Logout user and clear session."""
    request.session.clear()
    return air.responses.RedirectResponse("/", status_code=303)