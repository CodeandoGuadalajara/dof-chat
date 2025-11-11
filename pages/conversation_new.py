"""Conversation new page (Chat demo) for DOF Chat."""

import air
from ui.input import Input
from ui.button import Button
from ui.card import Card
from ui.form import Form
from components.chat_message import ChatMessage


class ConversationNewPage:
    """Page component for new conversation (chat demo)."""
    
    @staticmethod
    def render() -> air.Html:
        """Render the complete demo chat page using existing CSS classes.
        
        Uses existing chat.css and context.css for styling.
        Minimal responsive design without hardcoded styles.
        
        Returns:
            Air Html component for the demo page
        """
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
                    # Chat window
                    Card.create(
                        ChatMessage.welcome_message(
                            "¡Hola! Soy tu asistente para consultas sobre documentos del DOF. "
                            "Puedes preguntarme sobre cualquier tema y te ayudaré a encontrar información relevante."
                        ),
                        id="chat-window",
                        class_="chat-window"
                    ),
                    
                    air.Div(
                        Form.create(
                            air.Label(
                                "Escribe tu consulta:",
                                for_="chat-input",
                                class_="sr-only"
                            ),
                            Input.chat(
                                id="chat-input",
                                placeholder="Escribe tu pregunta sobre documentos del DOF...",
                                required=True,
                                **{
                                    "aria-label": "Campo de texto para consultas sobre documentos del DOF",
                                    "autocomplete": "off"
                                }
                            ),
                            # Send button
                            Button.primary(
                                "Enviar",
                                type="submit",
                                id="send-button"
                            ),
                            id="chat-form"
                        ),
                        class_="input-container"
                    ),
                    
                    class_="chat-container"
                ),
                
                # JavaScript for chat functionality
                air.Script(src="/static/js/chat.js")
            )
        )