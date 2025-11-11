"""Reusable input components using Air framework."""

import air


class Input:
    """Reusable input component - CSS framework agnostic."""
    
    @staticmethod
    def chat(**kwargs) -> air.Input:
        """Chat input with predefined styling.
        
        Args:
            **kwargs: HTML attributes (id, placeholder, required, etc.)
            
        Returns:
            Air Input component with chat styling
        """
        return air.Input(type="text", class_="form-input chat-input", **kwargs)