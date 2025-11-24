"""Web routes for serving HTML pages."""

import air
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import ValidationError
from routers.auth import require_login, get_db_session, authenticate_user
from pages.index import index_page
from pages.demo import demo_page
from pages.login import login_page
from schemas import LoginRequest

# Initialize Air router
router = air.AirRouter()

def redirect_with_error(request: air.Request, message: str):
    """Helper to redirect to login with error message."""
    request.session["error_message"] = message
    return air.responses.RedirectResponse("/login", status_code=303)


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
    """Process HTML login form submission with Pydantic validation."""
    # Get form data
    form_data = await request.form()
    csrf_token = form_data.get("csrf_token")

    # Validate CSRF token
    if csrf_token != request.session.get("csrf_token"):
        return redirect_with_error(request, "Token de seguridad inválido. Por favor, intenta nuevamente.")

    # Validate input with Pydantic
    try:
        login_data = LoginRequest(
            email=form_data.get("email", ""),
            password=form_data.get("password", "")
        )
    except ValidationError as e:
        # Extract user-friendly error message
        errors = e.errors()
        if any(err["type"] == "value_error.email" for err in errors):
            error_msg = "El formato del email es inválido."
        elif any(err["loc"] == ("password",) and "at least" in str(err.get("msg", "")) for err in errors):
            error_msg = "La contraseña debe tener al menos 8 caracteres."
        
        return redirect_with_error(request, error_msg)

    # Delegate auth logic to service helper
    user, reason = await authenticate_user(session, login_data.email, login_data.password)
    if not user:
        return redirect_with_error(request, "Email o contraseña incorrectos.")

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