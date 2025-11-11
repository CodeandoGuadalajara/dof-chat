"""Reusable card component using Air framework."""

import air
from typing import Optional, Union


class Card:
    """Reusable card component - CSS framework agnostic."""
    
    @staticmethod
    def create(
        *children: Union[str, air.BaseTag],
        title: Optional[str] = None,
        class_: Optional[str] = None,
        header_class: Optional[str] = None,
        body_class: Optional[str] = None,
        **kwargs
    ) -> air.Div:
        """Create a card container with optional title.
        
        Args:
            children: Child elements to include in card body
            title: Optional card title (creates header section)
            class_: CSS classes for card container (override default or add custom)
            header_class: CSS classes for header section  
            body_class: CSS classes for body section
            **kwargs: Additional HTML attributes
            
        Returns:
            Air Div component
            
        Examples:
            # Default styling (current CSS)
            Card.create("Content", title="Header")  # Uses: "card", "card-header", "card-body"
            
            # Tailwind override
            Card.create(
                "Content", 
                title="Header",
                class_="bg-white shadow rounded-lg overflow-hidden",
                header_class="bg-gray-50 px-4 py-3 border-b",
                body_class="p-4"
            )
            
            # Mixed approach
            Card.create("Content", class_="card shadow-lg")
        """
        # Default classes but allow override
        card_class = class_ if class_ else "card"
        
        card_content = []
        
        # Add title header if provided
        if title:
            title_class = header_class if header_class else "card-header"
            card_content.append(
                air.Div(
                    air.H3(title, class_="card-title"),
                    class_=title_class
                )
            )
        
        # Add body with children
        if children:
            content_class = body_class if body_class else "card-body"
            card_content.append(
                air.Div(*children, class_=content_class)
            )
        
        return air.Div(*card_content, class_=card_class, **kwargs)

    # Additional card variants (uncomment and customize as needed)
    # @staticmethod
    # def simple(*children, **kwargs) -> air.Div:
    #     """Simple card without header structure."""
    #     return air.Div(*children, class_="card", **kwargs)