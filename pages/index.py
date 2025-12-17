"""Index/home page for DOF Chat."""

import air


class IndexPage:
    """Page component for home/landing page."""
    
    @staticmethod
    def render(demo_url: str = "/demo") -> air.Html:
        """Render the home page.
        
        Args:
            demo_url: URL to the demo page
            
        Returns:
            Air Html component for the home page
        """
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
                        air.A("Ir al Demo", href=demo_url)
                    ),
                    class_="container"
                )
            )
        )