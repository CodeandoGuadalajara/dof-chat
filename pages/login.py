"""Login page for DOF Chat with Clerk authentication."""

import air


class LoginPage:
    """Page component for user authentication using Clerk."""
    
    @staticmethod
    async def render_async(request: air.Request, next: str = "/"):
        """Render the login page with full Clerk authentication.
        
        This method handles the complete Clerk authentication flow,
        checking if user is already signed in and rendering the sign-in form.
        
        Args:
            request: The Air/Starlette request object
            next: URL to redirect after successful login
            
        Returns:
            Air Html component or RedirectResponse if already authenticated
        """
        # Lazy imports to ensure dotenv is loaded first via main.py
        from airclerk import settings as clerk_settings
        from airclerk.main import sanitize_next, _to_httpx_request
        from clerk_backend_api import Clerk
        from clerk_backend_api.security.types import AuthenticateRequestOptions
        
        httpx_request = await _to_httpx_request(request)
        origin = f"{request.url.scheme}://{request.url.netloc}"
        next_url = sanitize_next(next)

        with Clerk(bearer_auth=clerk_settings.CLERK_SECRET_KEY) as clerk:
            state = clerk.authenticate_request(
                httpx_request,
                AuthenticateRequestOptions(authorized_parties=[origin]),
            )

            if state.is_signed_in:
                return air.RedirectResponse(
                    next_url if next_url != "/" else clerk_settings.CLERK_LOGIN_REDIRECT_ROUTE
                )

            return air.layouts.mvpcss(
                air.Title("Iniciar Sesión"),
                air.Style("""
                    body {
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        min-height: 100vh;
                    }
                    main {
                        max-width: 450px;
                        width: 100%;
                    }
                    #sign-in {
                        width: 100%;
                    }
                """),
                air.Script(
                    src=clerk_settings.CLERK_JS_SRC,
                    crossorigin="anonymous",
                    **{"data-clerk-publishable-key": clerk_settings.CLERK_PUBLISHABLE_KEY},
                ),
                air.Article(
                    air.Div(id="sign-in"),
                    air.Script(f"""                    
                        function initClerk() {{
                            if (!window.Clerk) {{
                                setTimeout(initClerk, 100);
                                return;
                            }}
                            
                            window.Clerk.load().then(() => {{
                                if (window.Clerk.user) {{
                                    window.location.assign('{next_url}');
                                    return;
                                }}
                                
                                window.Clerk.mountSignIn(
                                    document.getElementById('sign-in'),
                                    {{ redirectUrl: '{next_url}' }}
                                );
                            }});
                        }}
                        initClerk();
                    """),
                ),
            )