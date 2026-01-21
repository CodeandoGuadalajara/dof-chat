"""Conversation card and History Panel components for DOF Chat - ChatGPT Style."""

import air
import airdragon as ad
from typing import Optional
from utils.mock_history_data import MOCK_CONVERSATIONS


# Helper to reference SVG sprite icons
def _icon(name: str, size: int = 20) -> str:
    """Generate SVG element referencing the sprite."""
    return f'<svg width="{size}" height="{size}" class="shrink-0"><use href="/static/svg/icons.svg#icon-{name}"></use></svg>'


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
        """Create a conversation card component using AirDragon utilities.
        
        Args:
            title: Conversation title (truncated if too long)
            conversation_id: Unique identifier for the conversation
            is_active: Whether this card is currently selected
            **kwargs: Additional attributes
            
        Returns:
            Air Div component representing a conversation card
        """
        # Base classes
        base_classes = (
            "group flex items-center gap-2 px-4 py-2.5 rounded-lg cursor-pointer "
            "transition-colors hover:bg-gray-100 mb-0.5 "
            "data-[active=true]:bg-gray-100 data-[active=true]:border-l-4 "
            "data-[active=true]:border-purple-500"
        )
        
        return air.Div(
            # Content area
            air.Div(
                air.Span(
                    title,
                    class_="text-sm font-medium text-gray-800 truncate block",
                    **{"data-conversation-title": "true"}
                ),
                class_="flex-1 min-w-0"
            ),
            
            # Actions container (visible on hover)
            air.Div(
                # Menu trigger button (3 dots)
                ad.Button(
                    air.Raw(_icon("more", 18)),
                    modifier=ad.ButtonMods.ghost,
                    class_="w-7 h-7 rounded-full opacity-0 group-hover:opacity-100 transition-opacity",
                    type="button",
                    **{"aria-label": "Opciones de conversación", "data-menu-trigger": "true"}
                ),
                # Dropdown menu (hidden by default)
                air.Div(
                    ad.Button(
                        air.Span(air.Raw(_icon("share", 16)), class_="w-4 h-4 opacity-70"),
                        air.Span("Compartir"),
                        modifier=ad.ButtonMods.ghost,
                        class_="flex items-center gap-2 w-full justify-start px-3 py-2 text-sm hover:bg-gray-100",
                        **{"data-action": "share"}
                    ),
                    ad.Button(
                        air.Span(air.Raw(_icon("edit", 16)), class_="w-4 h-4 opacity-70"),
                        air.Span("Renombrar"),
                        modifier=ad.ButtonMods.ghost,
                        class_="flex items-center gap-2 w-full justify-start px-3 py-2 text-sm hover:bg-gray-100",
                        **{"data-action": "rename"}
                    ),
                    ad.Button(
                        air.Span(air.Raw(_icon("trash", 16)), class_="w-4 h-4 opacity-70"),
                        air.Span("Eliminar"),
                        modifier=ad.ButtonMods.ghost,
                        class_="flex items-center gap-2 w-full justify-start px-3 py-2 text-sm text-red-600 hover:bg-red-50",
                        **{"data-action": "delete"}
                    ),
                    class_="hidden absolute right-0 top-8 bg-white border border-gray-200 rounded-lg shadow-lg p-1 z-50 min-w-[140px] flex-col gap-0.5",
                    **{"data-dropdown": "true"}
                ),
                class_="relative",
                **{"data-dropdown-container": "true"}
            ),
            
            class_=base_classes,
            **{"data-conversation-id": conversation_id, "data-active": "true" if is_active else "false"},
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
            air.Div(
                group_title,
                class_="px-4 py-2 text-xs font-semibold text-gray-500 uppercase tracking-wide"
            ),
            air.Div(
                *cards,
                class_="flex flex-col ml-2"
            ),
            class_="mb-2",
            **{"data-conversation-group": "true"}
        )
    
    @staticmethod
    def create_panel(
        conversations: Optional[dict] = None,
        active_id: Optional[str] = "conv-003",
        expanded: bool = True
    ) -> air.Aside:
        """Create the complete history sidebar panel using AirDragon utilities.
        
        Args:
            conversations: Dict of date groups with conversation lists
            active_id: ID of the currently active conversation
            expanded: Whether the sidebar starts expanded
            
        Returns:
            Air Aside component for the sidebar
        """
        if conversations is None:
            conversations = MOCK_CONVERSATIONS
        
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
        
        # Sidebar classes with Tailwind - maintaining current design
        sidebar_base = "flex flex-col h-full bg-gray-50 border-r border-gray-200 transition-all duration-300 ease-in-out overflow-hidden z-50"

        
        return air.Aside(
            # Inner column container
            air.Div(
                # Header with toggle button
                air.Div(
                    ad.Button(
                        air.Raw(_icon("menu", 20)),
                        modifier=ad.ButtonMods.ghost,
                        class_="w-8 h-8 rounded-full flex items-center justify-center",
                        id="sidebar-toggle",
                        type="button",
                        **{"aria-label": "Alternar barra lateral"}
                    ),
                    class_="flex items-center justify-center w-[52px] py-3 h-12 shrink-0"
                ),
                
                # Actions section (New conversation button)
                air.Div(
                    ad.Button(
                        air.Raw(_icon("plus", 20)),
                        air.Span(
                            "Nueva conversación",
                            class_="ml-3 text-sm font-medium whitespace-nowrap opacity-100 group-data-[state=collapsed]/sidebar:opacity-0 group-data-[state=collapsed]/sidebar:w-0 group-data-[state=collapsed]/sidebar:hidden transition-all duration-200",
                            **{"data-label": "true"}
                        ),
                        modifier=ad.ButtonMods.secondary,
                        class_=(
                            "flex items-center transition-all duration-200 rounded-lg "
                            "w-full h-11 justify-start px-2 border border-gray-300 "
                            "group-data-[state=collapsed]/sidebar:w-9 group-data-[state=collapsed]/sidebar:h-9 "
                            "group-data-[state=collapsed]/sidebar:justify-center group-data-[state=collapsed]/sidebar:px-0 "
                            "group-data-[state=collapsed]/sidebar:border-transparent"
                        ),
                        id="new-chat-btn",
                        type="button",
                        **{"aria-label": "Nueva conversación"}
                    ),
                    class_="flex justify-center px-4 py-3 shrink-0"
                ),
                
                # Main content area (only visible when expanded)
                air.Div(
                    # Search input
                    air.Div(
                        air.Input(
                            type="search",
                            placeholder="Buscar...",
                            class_="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg bg-white focus:outline-none focus:border-indigo-500",
                            id="history-search",
                            **{"aria-label": "Buscar conversaciones"}
                        ),
                        class_="px-4 mb-2"
                    ),
                    
                    # Section title
                    air.Div(
                        "Recientes",
                        class_="px-4 py-2 text-sm font-semibold text-gray-700"
                    ),
                    
                    # Scrollable history list
                    air.Div(
                        *conversation_groups,
                        class_="flex-1 overflow-y-auto pr-1",
                        id="history-list"
                    ),
                    
                    id="sidebar-main-content",
                    class_="flex-1 flex flex-col overflow-hidden transition-opacity duration-200 group-data-[state=collapsed]/sidebar:hidden"
                ),
                
                # Footer with settings
                air.Div(
                    ad.Button(
                        air.Raw(_icon("settings", 20)),
                        air.Span(
                            "Configuración",
                            class_="ml-3 text-sm whitespace-nowrap opacity-100 group-data-[state=collapsed]/sidebar:opacity-0 group-data-[state=collapsed]/sidebar:w-0 group-data-[state=collapsed]/sidebar:hidden transition-all duration-200",
                            **{"data-label": "true"}
                        ),
                        modifier=ad.ButtonMods.ghost,
                        class_=(
                            "flex items-center transition-colors "
                            "w-full justify-start px-2 "
                            "group-data-[state=collapsed]/sidebar:w-9 group-data-[state=collapsed]/sidebar:h-9 "
                            "group-data-[state=collapsed]/sidebar:justify-center group-data-[state=collapsed]/sidebar:px-0 "
                            "group-data-[state=collapsed]/sidebar:border group-data-[state=collapsed]/sidebar:border-transparent"
                        ),
                        id="settings-btn",
                        type="button",
                        **{"aria-label": "Configuración"}
                    ),
                    class_="flex justify-center px-2 py-3 group-data-[state=collapsed]/sidebar:pt-[0.1rem] group-data-[state=collapsed]/sidebar:pb-1.5 border-t border-gray-200 mt-auto shrink-0"
                ),
                
                class_="flex flex-col h-full w-full"
            ),
            
            class_=f"{sidebar_base} w-[380px] min-w-[380px] data-[state=collapsed]:w-[52px] data-[state=collapsed]:min-w-[52px] group/sidebar",
            id="history-sidebar",
            **{"data-state": "expanded" if expanded else "collapsed"}
        )
    
    @staticmethod
    def create_mobile_toggle() -> ad.Button:
        """Create the mobile toggle button (visible only on small screens).
        
        Returns:
            AirDragon Button component for mobile sidebar toggle
        """
        return ad.Button(
            air.Raw(_icon("menu", 20)),
            modifier=ad.ButtonMods.ghost,
            class_="fixed top-[88px] left-3 w-10 h-10 md:hidden shadow-lg z-40",
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
            class_="fixed inset-0 bg-black bg-opacity-30 z-40 hidden",
            id="sidebar-overlay"
        )