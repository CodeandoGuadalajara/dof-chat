"""Conversation card component for DOF Chat."""

import air


class ConversationCard:
    """Component for rendering conversation cards and summaries.
    
    TODO: Future implementation for conversation history/list feature.
    Currently not needed as the app focuses on single demo conversations.
    The context_renderer.py already handles accordion-based context display.
    """
    
    @staticmethod
    def create(title: str, preview: str, **kwargs) -> air.Div:
        """TODO: Create a conversation card component.
        
        This is a placeholder for future conversation history functionality.
        Currently the app only supports single demo conversations.
        
        Args:
            title: Conversation title
            preview: Preview text
            **kwargs: Additional attributes
            
        Returns:
            Air Div placeholder component
        """
        return air.Div(
            f"TODO: ConversationCard - {title}: {preview}",
            class_="conversation-card-placeholder"
        )