import air
from airclerk import settings
from airclerk.main import sanitize_next, _to_httpx_request
from clerk_backend_api import Clerk
from clerk_backend_api.security.types import AuthenticateRequestOptions


async def login_page(request: air.Request, next: str = "/"):
    httpx_request = await _to_httpx_request(request)
    origin = f"{request.url.scheme}://{request.url.netloc}"
    next = sanitize_next(next)

    with Clerk(bearer_auth=settings.CLERK_SECRET_KEY) as clerk:
        state = clerk.authenticate_request(
            httpx_request,
            AuthenticateRequestOptions(authorized_parties=[origin]),
        )

        if state.is_signed_in:
            return air.RedirectResponse(
                next if next != "/" else settings.CLERK_LOGIN_REDIRECT_ROUTE
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
                src=settings.CLERK_JS_SRC,
                crossorigin="anonymous",
                **{"data-clerk-publishable-key": settings.CLERK_PUBLISHABLE_KEY},
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
                                window.location.assign('{next}');
                                return;
                            }}
                            
                            window.Clerk.mountSignIn(
                                document.getElementById('sign-in'),
                                {{ redirectUrl: '{next}' }}
                            );
                        }});
                    }}
                    initClerk();
                """),
            ),
        )