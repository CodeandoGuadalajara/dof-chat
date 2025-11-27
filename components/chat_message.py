"""Chat message component for DOF Chat."""

import air
from typing import Optional


class ChatMessage:
    """Component for rendering individual chat messages."""
    
    @staticmethod
    def welcome_message(
        content: str,
        *,
        class_: Optional[str] = None
    ) -> air.Div:
        """Create a welcome message component with proper styling.
        
        Args:
            content: Welcome message text
            class_: Additional CSS classes
            
        Returns:
            Air Div component for welcome message
        """
        css_classes = "welcome-message"
        if class_:
            css_classes += f" {class_}"
        
        return air.Div(content, class_=css_classes)
    
    @staticmethod
    def loading_message(text: str = "Procesando tu consulta...", **kwargs) -> air.Div:
        """TODO: Create a loading message component.
        
        Currently not used - loading is handled by JavaScript in chat.js
        
        Args:
            text: Loading text to display
            **kwargs: Additional attributes
            
        Returns:
            Air Div placeholder component
        """
        return air.Div(f"TODO: LoadingMessage - {text}", class_="loading-message-placeholder")