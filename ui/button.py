"""Reusable button component using Air framework."""

import air
from typing import Optional


class Button:
    """Reusable button component"""
    
    @staticmethod
    def primary(
        text: str,
        *,
        type: str = "button",
        id: Optional[str] = None,
        class_: Optional[str] = None,
        disabled: bool = False,
        **kwargs
    ) -> air.Button:
        """Create a primary button.
        
        Args:
            text: Button text content
            type: Button type (button, submit, reset)
            id: HTML id attribute
            class_: CSS classes (override default or add custom)
            disabled: Whether button is disabled
            **kwargs: Additional HTML attributes
            
        Returns:
            Air Button component
            
        Examples:
            # Default styling (current CSS)
            Button.primary("Save")  # Uses: "btn btn-primary"
        """
        # Default to current CSS classes, but allow full override
        default_classes = "btn btn-primary"
        final_classes = class_ if class_ else default_classes
        
        return air.Button(
            text,
            type=type,
            id=id,
            class_=final_classes,
            disabled=disabled,
            **kwargs
        )

    # Additional button variants (uncomment and customize as needed)
    # @staticmethod  
    # def secondary(text: str, **kwargs) -> air.Button:
    #     """Secondary button - add CSS classes for .btn-secondary"""
    #     return air.Button(text, class_="btn btn-secondary", **kwargs)

    # @staticmethod
    # def danger(text: str, **kwargs) -> air.Button:
    #     """Danger button - add CSS classes for .btn-danger"""
    #     return air.Button(text, class_="btn btn-danger", **kwargs)
    
    # @staticmethod
    # def large(text: str, **kwargs) -> air.Button:
    #     """Large button - ready to use.
    #     
    #     REQUIRES CSS: .btn-lg (not implemented yet)
    #     """
    #     return air.Button(text, class_="btn btn-primary btn-lg", **kwargs)
    
    # @staticmethod
    # def small(text: str, **kwargs) -> air.Button:
    #     """Small button - ready to use.
    #     
    #     REQUIRES CSS: .btn-secondary and .btn-sm (not implemented yet)
    #     """
    #     return air.Button(text, class_="btn btn-secondary btn-sm", **kwargs)