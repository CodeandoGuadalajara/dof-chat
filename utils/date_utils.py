"""Date utilities for document processing.

Utilities for extracting and formatting dates from document titles,
calculating document age, and providing age indicators for the DOF Chat system.
"""

from datetime import datetime
from typing import Tuple


def extract_date_from_title(title: str) -> Tuple[str, str, str]:
    """Extract date from document title using first 8 characters in format DDMMAAAA and calculate age.
    
    Args:
        title: Document title starting with date in DDMMAAAA format (e.g., "19082025_MAT")
        
    Returns:
        Tuple[str, str, str]: (formatted_date, age_description, age_emoji)
        
    Example:
        >>> extract_date_from_title("19082025_LEY_IMPUESTO")
        ("19 de agosto de 2025", "Muy reciente", "🟢")
    """
    try:
        # Extract first 8 characters for date (DDMMAAAA format)
        date_str = title[:8]
        
        # Validate that we have 8 digits
        if len(date_str) == 8 and date_str.isdigit():
            day = date_str[:2]
            month = date_str[2:4]
            year = date_str[4:8]
            
            # Parse the date
            doc_date = datetime(int(year), int(month), int(day))
            
            # Calculate age
            today = datetime.now()
            days_diff = (today - doc_date).days
            
            # Format date for display
            formatted_date = f"{day} de {get_month_name(int(month))} de {year}"
            
            # Calculate age description and emoji
            if days_diff < 30:
                age_desc = "Muy reciente"
                age_emoji = "🟢"
            elif days_diff < 90:
                age_desc = "Reciente"
                age_emoji = "🟡"
            elif days_diff < 365:
                age_desc = "Este año"
                age_emoji = "🟠"
            else:
                years = days_diff // 365
                age_desc = f"Hace {years} año{'s' if years > 1 else ''}"
                age_emoji = "🔴"
            
            return formatted_date, age_desc, age_emoji
            
    except (ValueError, IndexError):
        # Invalid date or format, use fallback
        pass
    
    # Fallback if no date found or invalid date
    return "Fecha no disponible", "Antigüedad desconocida", "⚫"


def get_month_name(month: int) -> str:
    """Get Spanish month name from month number.
    
    Args:
        month: Month number (1-12)
        
    Returns:
        str: Spanish month name
        
    Example:
        >>> get_month_name(8)
        "agosto"
    """
    months = {
        1: "enero", 2: "febrero", 3: "marzo", 4: "abril",
        5: "mayo", 6: "junio", 7: "julio", 8: "agosto", 
        9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"
    }
    return months.get(month, "mes desconocido")


def calculate_document_age(doc_date: datetime) -> Tuple[str, str]:
    """Calculate document age description and emoji from a datetime object.
    
    Args:
        doc_date: Document publication date
        
    Returns:
        Tuple[str, str]: (age_description, age_emoji)
        
    Example:
        >>> from datetime import datetime, timedelta
        >>> old_date = datetime.now() - timedelta(days=400)
        >>> calculate_document_age(old_date)
        ("Hace 1 año", "🔴")
    """
    today = datetime.now()
    days_diff = (today - doc_date).days
    
    if days_diff < 30:
        return "Muy reciente", "🟢"
    elif days_diff < 90:
        return "Reciente", "🟡"
    elif days_diff < 365:
        return "Este año", "🟠"
    else:
        years = days_diff // 365
        age_desc = f"Hace {years} año{'s' if years > 1 else ''}"
        return age_desc, "🔴"


def format_spanish_date(date_obj: datetime) -> str:
    """Format a datetime object to Spanish date format.
    
    Args:
        date_obj: Date to format
        
    Returns:
        str: Formatted date in Spanish (DD de MONTH de YYYY)
        
    Example:
        >>> from datetime import datetime
        >>> format_spanish_date(datetime(2025, 8, 19))
        "19 de agosto de 2025"
    """
    day = date_obj.day
    month = date_obj.month
    year = date_obj.year
    
    return f"{day:02d} de {get_month_name(month)} de {year}"