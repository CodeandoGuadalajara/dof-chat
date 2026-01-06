"""Conversation card and History Panel components for DOF Chat - ChatGPT Style."""

import air
from typing import Optional
from utils.mock_data import MOCK_CONVERSATIONS


# SVG Icons as constants (only for UI controls, NOT for conversation items)
ICON_MORE = """<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="1"/><circle cx="19" cy="12" r="1"/><circle cx="5" cy="12" r="1"/></svg>"""

ICON_EDIT = """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z"/></svg>"""

ICON_TRASH = """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>"""

ICON_SHARE = """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg>"""

ICON_MENU = """<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/></svg>"""

ICON_PLUS = """<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>"""

ICON_SETTINGS = """<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M12 1v4M12 19v4M4.22 4.22l2.83 2.83M16.95 16.95l2.83 2.83M1 12h4M19 12h4M4.22 19.78l2.83-2.83M16.95 7.05l2.83-2.83"/></svg>"""


class ConversationCard:
    """Component for rendering conversation cards in ChatGPT style.
    
    Renders individual conversation items for the history sidebar panel
    with title, preview text, icons, and hover actions.
    """
    
    @staticmethod
    def create(
        title: str, 
        conversation_id: str = "",
        is_active: bool = False,
        **kwargs
    ) -> air.Div:
        """Create a conversation card component in ChatGPT style.
        
        Args:
            title: Conversation title (truncated if too long)
            conversation_id: Unique identifier for the conversation
            is_active: Whether this card is currently selected
            **kwargs: Additional attributes
            
        Returns:
            Air Div component representing a conversation card
        """
        active_class = " active" if is_active else ""
        
        return air.Div(
            # Content area (solo título) - como en la imagen de referencia
            air.Div(
                air.Span(title, class_="history-item-title"),
                class_="history-item-content"
            ),
            
            # Actions container (visible on hover)
            air.Div(
                # Menu trigger button (3 dots)
                air.Button(
                    air.Raw(ICON_MORE),
                    class_="history-menu-trigger",
                    type="button",
                    **{"aria-label": "Opciones de conversación", "data-conversation-id": conversation_id}
                ),
                # Dropdown menu (hidden by default)
                air.Div(
                    air.Button(
                        air.Span(air.Raw(ICON_SHARE), class_="menu-item-icon"),
                        air.Span("Compartir"),
                        class_="history-menu-item"
                    ),
                    air.Button(
                        air.Span(air.Raw(ICON_EDIT), class_="menu-item-icon"),
                        air.Span("Renombrar"),
                        class_="history-menu-item"
                    ),
                    air.Button(
                        air.Span(air.Raw(ICON_TRASH), class_="menu-item-icon"),
                        air.Span("Eliminar"),
                        class_="history-menu-item delete"
                    ),
                    class_="history-dropdown-menu hidden"
                ),
                class_="history-item-actions-container"
            ),
            
            class_=f"history-item{active_class}",
            **{"data-conversation-id": conversation_id},
            **kwargs
        )
    
    @staticmethod
    def create_group(group_title: str, cards: list) -> air.Div:
        """Create a group of conversation cards with a date header.
        
        Args:
            group_title: Title for the group (e.g., "HOY", "AYER")
            cards: List of ConversationCard components
            
        Returns:
            Air Div component containing the grouped cards
        """
        return air.Div(
            air.Div(group_title, class_="history-group-title"),
            *cards,
            class_="history-group"
        )
    
    @staticmethod
    def create_panel(
        conversations: Optional[dict] = None,
        active_id: Optional[str] = "conv-003",
        expanded: bool = True
    ) -> air.Aside:
        """Create the complete history sidebar panel.
        
        Args:
            conversations: Dict of date groups with conversation lists
            active_id: ID of the currently active conversation
            expanded: Whether the sidebar starts expanded
            
        Returns:
            Air Aside component for the sidebar
        """
        if conversations is None:
            conversations = MOCK_CONVERSATIONS
            
        expanded_class = " expanded" if expanded else ""
        
        # Build conversation groups
        conversation_groups = []
        for group_title, convs in conversations.items():
            cards = []
            for conv in convs:
                is_active = conv.get("id") == active_id
                cards.append(
                    ConversationCard.create(
                        title=conv["title"],
                        conversation_id=conv["id"],
                        is_active=is_active
                    )
                )
            if cards:
                conversation_groups.append(
                    ConversationCard.create_group(group_title, cards)
                )
        
        return air.Aside(
            # Inner column container
            air.Div(
                # Header with toggle button
                air.Div(
                    air.Button(
                        air.Raw(ICON_MENU),
                        class_="sidebar-icon-btn",
                        id="sidebar-toggle",
                        type="button",
                        **{"aria-label": "Alternar barra lateral"}
                    ),
                    class_="sidebar-header"
                ),
                
                # Actions section (New conversation button)
                air.Div(
                    air.Button(
                        air.Raw(ICON_PLUS),
                        air.Span("Nueva conversación", class_="sidebar-label"),
                        class_="new-chat-btn",
                        id="new-chat-btn",
                        type="button",
                        **{"aria-label": "Nueva conversación"}
                    ),
                    class_="sidebar-actions"
                ),
                
                # Main content area (only visible when expanded)
                air.Div(
                    # Search input
                    air.Div(
                        air.Input(
                            type="search",
                            placeholder="Buscar...",
                            class_="history-search-input",
                            id="history-search",
                            **{"aria-label": "Buscar conversaciones"}
                        ),
                        class_="history-search-container"
                    ),
                    
                    # Section title
                    air.Div("Recientes", class_="history-section-title"),
                    
                    # Scrollable history list
                    air.Div(
                        *conversation_groups,
                        class_="history-scroll-area",
                        id="history-list"
                    ),
                    
                    class_="sidebar-main-content"
                ),
                
                # Footer with settings
                air.Div(
                    air.Button(
                        air.Raw(ICON_SETTINGS),
                        air.Span("Configuración", class_="sidebar-label"),
                        class_="sidebar-footer-btn",
                        id="settings-btn",
                        type="button",
                        **{"aria-label": "Configuración"}
                    ),
                    class_="sidebar-footer"
                ),
                
                class_="sidebar-inner-col"
            ),
            
            class_=f"sidebar{expanded_class}",
            id="history-sidebar"
        )
    
    @staticmethod
    def create_mobile_toggle() -> air.Button:
        """Create the mobile toggle button (visible only on small screens).
        
        Returns:
            Air Button component for mobile sidebar toggle
        """
        return air.Button(
            air.Raw(ICON_MENU),
            class_="mobile-toggle",
            id="mobile-sidebar-toggle",
            type="button",
            **{"aria-label": "Abrir menú lateral"}
        )
    
    @staticmethod
    def create_overlay() -> air.Div:
        """Create the mobile overlay for sidebar.
        
        Returns:
            Air Div component for the overlay
        """
        return air.Div(
            class_="sidebar-overlay",
            id="sidebar-overlay"
        )