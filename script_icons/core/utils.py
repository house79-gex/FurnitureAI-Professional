"""
Utility functions for icon generation
"""

import math
from typing import Tuple


def calculate_luminance(hex_color: str) -> float:
    """
    Calculate relative luminance of a color (WCAG formula)
    
    Args:
        hex_color: Color in hex format (#RRGGBB)
        
    Returns:
        Relative luminance (0-1)
    """
    # Remove # if present
    hex_color = hex_color.lstrip('#')
    
    # Convert to RGB
    r, g, b = tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))
    
    # Apply gamma correction
    def gamma_correct(channel):
        if channel <= 0.03928:
            return channel / 12.92
        else:
            return math.pow((channel + 0.055) / 1.055, 2.4)
    
    r_linear = gamma_correct(r)
    g_linear = gamma_correct(g)
    b_linear = gamma_correct(b)
    
    # Calculate luminance
    return 0.2126 * r_linear + 0.7152 * g_linear + 0.0722 * b_linear


def calculate_contrast_ratio(color1: str, color2: str) -> float:
    """
    Calculate contrast ratio between two colors (WCAG formula)
    
    Args:
        color1: First color in hex format
        color2: Second color in hex format
        
    Returns:
        Contrast ratio (1-21)
    """
    l1 = calculate_luminance(color1)
    l2 = calculate_luminance(color2)
    
    lighter = max(l1, l2)
    darker = min(l1, l2)
    
    return (lighter + 0.05) / (darker + 0.05)


def scale_value(value: float, from_size: int, to_size: int) -> float:
    """
    Scale a value proportionally from one size to another
    
    Args:
        value: Value to scale
        from_size: Original size
        to_size: Target size
        
    Returns:
        Scaled value
    """
    return value * (to_size / from_size)


def clamp(value: float, min_val: float, max_val: float) -> float:
    """
    Clamp a value between min and max
    
    Args:
        value: Value to clamp
        min_val: Minimum value
        max_val: Maximum value
        
    Returns:
        Clamped value
    """
    return max(min_val, min(value, max_val))


def point_in_rect(x: float, y: float, rect_x: float, rect_y: float, 
                  rect_width: float, rect_height: float) -> bool:
    """
    Check if a point is inside a rectangle
    
    Args:
        x, y: Point coordinates
        rect_x, rect_y: Rectangle top-left corner
        rect_width, rect_height: Rectangle dimensions
        
    Returns:
        True if point is inside rectangle
    """
    return (rect_x <= x <= rect_x + rect_width and 
            rect_y <= y <= rect_y + rect_height)


def interpolate_color(color1: str, color2: str, t: float) -> str:
    """
    Interpolate between two colors
    
    Args:
        color1: Start color in hex format
        color2: End color in hex format
        t: Interpolation factor (0-1)
        
    Returns:
        Interpolated color in hex format
    """
    # Remove # if present
    color1 = color1.lstrip('#')
    color2 = color2.lstrip('#')
    
    # Convert to RGB
    r1, g1, b1 = tuple(int(color1[i:i+2], 16) for i in (0, 2, 4))
    r2, g2, b2 = tuple(int(color2[i:i+2], 16) for i in (0, 2, 4))
    
    # Interpolate
    r = int(r1 + (r2 - r1) * t)
    g = int(g1 + (g2 - g1) * t)
    b = int(b1 + (b2 - b1) * t)
    
    # Convert back to hex
    return f'#{r:02x}{g:02x}{b:02x}'


def create_gradient_id(icon_name: str, size: int, gradient_type: str = 'linear') -> str:
    """
    Create a unique gradient ID for SVG
    
    Args:
        icon_name: Name of the icon
        size: Icon size
        gradient_type: Type of gradient (linear, radial)
        
    Returns:
        Unique gradient ID
    """
    return f'grad_{icon_name}_{size}_{gradient_type}'


def ensure_min_size(value: float, min_size: float) -> float:
    """
    Ensure a value is at least the minimum size
    
    Args:
        value: Value to check
        min_size: Minimum allowed size
        
    Returns:
        Value or minimum size, whichever is larger
    """
    return max(value, min_size)


def round_to_half(value: float) -> float:
    """
    Round a value to nearest 0.5
    Useful for crisp SVG rendering
    
    Args:
        value: Value to round
        
    Returns:
        Rounded value
    """
    return round(value * 2) / 2
