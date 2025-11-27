"""Reusable form component using Air framework."""

import air
from typing import Optional, Union


class Form:
    """Reusable form component - CSS framework agnostic."""
    
    @staticmethod
    def create(
        *children: Union[str, air.BaseTag],
        action: Optional[str] = None,
        method: str = "POST",
        id: Optional[str] = None,
        class_: Optional[str] = None,
        **kwargs
    ) -> air.Form:
        """Create a basic form container.
        
        Args:
            children: Form elements (inputs, buttons, etc.)
            action: Form action URL
            method: HTTP method (GET, POST)
            id: HTML id attribute
            class_: CSS classes (use existing 'form' or Tailwind classes)
            **kwargs: Additional HTML attributes
            
        Returns:
            Air Form component
            
        Examples:
            # Current CSS approach
            Form.create(inputs, class_="form")
            
            # Tailwind approach  
            Form.create(inputs, class_="space-y-4 p-4")
            
            # Custom approach
            Form.create(inputs, class_="my-custom-form")
        """
        return air.Form(
            *children,
            action=action,
            method=method,
            id=id,
            class_=class_ or "",
            **kwargs
        )

    # Additional form layouts (uncomment and customize as needed)
    # @staticmethod
    # def inline(*children, **kwargs) -> air.Form:
    #     """Inline form layout - add CSS classes for inline styling"""
    #     return Form.create(*children, class_="form-inline", **kwargs)
    
    # @staticmethod  
    # def field_group(label: str, input_component, **kwargs) -> air.Div:
    #     """Form field group with label and input"""
    #     return air.Div(
    #         air.Label(label),
    #         input_component,
    #         class_="form-group",
    #         **kwargs
    #     )