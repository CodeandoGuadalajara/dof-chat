"""Web routes for serving HTML pages."""

import air

# Initialize Air router
router = air.AirRouter()

@router.page
def demo():
    """Serve the demo chatbot page."""
    return air.Html(
        air.Head(
            air.Title("DOF Chat Demo"),
            air.Meta(charset="UTF-8"),
            air.Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
            air.Link(rel="stylesheet", href="/static/css/chat.css"),
            air.Link(rel="stylesheet", href="/static/css/context.css")
        ),
        air.Body(
            air.Div(
                air.H1("DOF Chat Demo"),
                air.P("Sistema de consultas sobre documentos del Diario Oficial de la Federación"),
                class_="header"
            ),
            air.Div(
                air.Div(
                    air.Div(
                        "¡Hola! Soy tu asistente para consultas sobre documentos del DOF. "
                        "Puedes preguntarme sobre cualquier tema y te ayudaré a encontrar información relevante.",
                        class_="welcome-message"
                    ),
                    id="chat-window",
                    class_="chat-window"
                ),
                air.Div(
                    air.Form(
                        air.Input(
                            type="text",
                            id="chat-input",
                            class_="chat-input",
                            placeholder="Escribe tu pregunta sobre documentos del DOF...",
                            required=True
                        ),
                        air.Button(
                            "Enviar",
                            type="submit",
                            id="send-button",
                            class_="send-button"
                        ),
                        id="chat-form",
                        style="display: flex; width: 100%; gap: 0.5rem;"
                    ),
                    class_="input-container"
                ),
                class_="chat-container"
            ),
            # Use external JavaScript file
            air.Script(src="/static/js/chat.js")
        )
    )

@router.page
def index():
    """Serve the home page redirecting to demo."""
    return air.Html(
        air.Head(
            air.Title("DOF Chat"),
            air.Meta(charset="UTF-8"),
            air.Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
            air.Style("""
                body {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    max-width: 600px;
                    margin: 2rem auto;
                    padding: 2rem;
                    background-color: #f5f5f5;
                }
                .container {
                    background: white;
                    padding: 2rem;
                    border-radius: 8px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                    text-align: center;
                }
                h1 {
                    color: #667eea;
                    margin-bottom: 1rem;
                }
                p {
                    margin-bottom: 1rem;
                    color: #666;
                    line-height: 1.6;
                }
                a {
                    background: #667eea;
                    color: white;
                    padding: 0.75rem 1.5rem;
                    text-decoration: none;
                    border-radius: 6px;
                    font-weight: bold;
                    transition: background-color 0.2s;
                }
                a:hover {
                    background: #5a6fd8;
                }
            """)
        ),
        air.Body(
            air.Div(
                air.H1("DOF Chat"),
                air.P("Bienvenido al sistema de consultas sobre documentos del Diario Oficial de la Federación"),
                air.P(
                    air.A("Ir al Demo", href=demo.url())
                ),
                class_="container"
            )
        )
    )