import air
from routers.auth import generate_csrf_token


def login_page(request: air.Request):
    
    csrf_token = generate_csrf_token()
    request.session["csrf_token"] = csrf_token
    
    # Retrieve error message from session (flash message pattern)
    error_message = request.session.pop("error_message", None)
    
    # Build error alert if there's a message
    error_alert = None
    if error_message:
        error_alert = air.Div(
            air.P(
                error_message,
                style="margin: 0; font-weight: 500;"
            ),
            style="max-width: 400px; margin: 0 auto 1.5rem auto; padding: 1rem; "
                  "background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; "
                  "border-radius: 6px; text-align: center;"
        )
    
    return air.layouts.mvpcss(
        air.Title("Login - DOF Chat"),
        air.H1("Iniciar Sesión", style="text-align: center; margin-bottom: 2rem;"),
        
        # Show error alert if exists
        error_alert if error_alert else air.Div(),
        
        # Classic login form
        air.Div(
            air.H2("Login con Email y Contraseña", 
                   style="font-size: 1.2rem; margin-bottom: 1rem; color: #495057;"),
            air.Form(
                air.Input(
                    type="email",
                    name="email",
                    placeholder="Email",
                    required=True,
                    style="width: 100%; padding: 0.75rem; margin-bottom: 1rem; "
                          "border: 2px solid #e9ecef; border-radius: 6px; font-size: 1rem;"
                ),
                air.Input(
                    type="password",
                    name="password",
                    placeholder="Password",
                    required=True,
                    style="width: 100%; padding: 0.75rem; margin-bottom: 1rem; "
                          "border: 2px solid #e9ecef; border-radius: 6px; font-size: 1rem;"
                ),
                air.Input(
                    type="hidden",
                    name="csrf_token",
                    value=csrf_token
                ),
                air.Button(
                    "Entrar con Email",
                    type="submit",
                    style="width: 100%; padding: 0.75rem; background: #667eea; "
                          "color: white; border: none; border-radius: 6px; "
                          "font-size: 1rem; cursor: pointer; margin-bottom: 1rem;"
                ),
                method="post",
                action="/login"
            ),
            style="max-width: 400px; margin: 0 auto 2rem auto; padding: 2rem; "
                  "background: white; border-radius: 8px; "
                  "box-shadow: 0 2px 8px rgba(0,0,0,0.1);"
        ),
        
        air.P(
            air.A("← Volver al inicio", href="/"),
            style="text-align: center; margin-top: 2rem;"
        )
    )