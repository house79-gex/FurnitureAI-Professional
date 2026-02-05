"""
Geometry validators for icon generation
Ensures all generated SVG elements meet quality standards
"""

from typing import Dict, List, Tuple, Optional
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import VALIDATION_RULES
from core.utils import calculate_contrast_ratio


class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass


class GeometryValidator:
    """Validates SVG geometry elements"""
    
    def __init__(self, size: int):
        """
        Initialize validator for specific icon size
        
        Args:
            size: Icon size (16, 32, 64, or 128)
        """
        self.size = size
        self.rules = VALIDATION_RULES
        self.errors = []
        
    def validate_element(self, element: Dict) -> bool:
        """
        Validate a single SVG element
        
        Args:
            element: Element dictionary with type and attributes
            
        Returns:
            True if valid, False otherwise
        """
        self.errors.clear()
        
        element_type = element.get('type', '')
        
        if element_type == 'rect':
            return self._validate_rect(element)
        elif element_type == 'circle':
            return self._validate_circle(element)
        elif element_type == 'line':
            return self._validate_line(element)
        elif element_type == 'path':
            return self._validate_path(element)
        elif element_type == 'polygon':
            return self._validate_polygon(element)
        elif element_type == 'ellipse':
            return self._validate_ellipse(element)
        else:
            self.errors.append(f"Unknown element type: {element_type}")
            return False
    
    def _validate_rect(self, element: Dict) -> bool:
        """Validate rectangle element"""
        width = element.get('width', 0)
        height = element.get('height', 0)
        
        min_size = self.rules['min_element_size']
        
        if width < min_size:
            self.errors.append(f"Rectangle width {width} < minimum {min_size}")
            return False
            
        if height < min_size:
            self.errors.append(f"Rectangle height {height} < minimum {min_size}")
            return False
        
        # Validate stroke width if present
        if 'stroke_width' in element:
            if not self._validate_stroke_width(element['stroke_width']):
                return False
        
        return True
    
    def _validate_circle(self, element: Dict) -> bool:
        """Validate circle element"""
        r = element.get('r', 0)
        
        min_radius = self.rules['min_circle_radius']
        
        if r < min_radius:
            self.errors.append(f"Circle radius {r} < minimum {min_radius}")
            return False
        
        # Validate stroke width if present
        if 'stroke_width' in element:
            if not self._validate_stroke_width(element['stroke_width']):
                return False
        
        return True
    
    def _validate_ellipse(self, element: Dict) -> bool:
        """Validate ellipse element"""
        rx = element.get('rx', 0)
        ry = element.get('ry', 0)
        
        min_size = self.rules['min_element_size']
        
        if rx < min_size:
            self.errors.append(f"Ellipse rx {rx} < minimum {min_size}")
            return False
            
        if ry < min_size:
            self.errors.append(f"Ellipse ry {ry} < minimum {min_size}")
            return False
        
        return True
    
    def _validate_line(self, element: Dict) -> bool:
        """Validate line element"""
        x1 = element.get('x1', 0)
        y1 = element.get('y1', 0)
        x2 = element.get('x2', 0)
        y2 = element.get('y2', 0)
        
        # Calculate line length
        length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        
        min_size = self.rules['min_element_size']
        
        if length < min_size:
            self.errors.append(f"Line length {length:.2f} < minimum {min_size}")
            return False
        
        # Validate stroke width if present
        if 'stroke_width' in element:
            if not self._validate_stroke_width(element['stroke_width']):
                return False
        
        return True
    
    def _validate_path(self, element: Dict) -> bool:
        """Validate path element"""
        d = element.get('d', '')
        
        if not d:
            self.errors.append("Path has empty 'd' attribute")
            return False
        
        # Basic validation: check for valid commands
        valid_commands = set('MmLlHhVvCcSsQqTtAaZz')
        commands = [c for c in d if c.isalpha()]
        
        for cmd in commands:
            if cmd not in valid_commands:
                self.errors.append(f"Invalid path command: {cmd}")
                return False
        
        # Check path is closed (ends with Z or z) for filled paths
        if element.get('fill') and element['fill'] != 'none':
            if not d.strip().endswith(('Z', 'z')):
                self.errors.append("Filled path should be closed (end with Z)")
                # This is a warning, not an error
        
        return True
    
    def _validate_polygon(self, element: Dict) -> bool:
        """Validate polygon element"""
        points = element.get('points', '')
        
        if not points:
            self.errors.append("Polygon has empty 'points' attribute")
            return False
        
        # Parse points
        try:
            point_list = []
            coords = points.replace(',', ' ').split()
            
            for i in range(0, len(coords), 2):
                x = float(coords[i])
                y = float(coords[i + 1])
                point_list.append((x, y))
            
            # Must have at least 3 points
            if len(point_list) < 3:
                self.errors.append(f"Polygon must have at least 3 points, got {len(point_list)}")
                return False
        
        except (ValueError, IndexError) as e:
            self.errors.append(f"Invalid polygon points format: {e}")
            return False
        
        return True
    
    def _validate_stroke_width(self, stroke_width: float) -> bool:
        """Validate stroke width for current size"""
        min_stroke = self.rules['min_stroke_width'].get(self.size, 1)
        
        if stroke_width < min_stroke:
            self.errors.append(
                f"Stroke width {stroke_width} < minimum {min_stroke} for size {self.size}"
            )
            return False
        
        return True
    
    def validate_contrast(self, fg_color: str, bg_color: str) -> bool:
        """
        Validate color contrast meets WCAG standards
        
        Args:
            fg_color: Foreground color (hex)
            bg_color: Background color (hex)
            
        Returns:
            True if contrast is sufficient
        """
        try:
            contrast = calculate_contrast_ratio(fg_color, bg_color)
            min_contrast = self.rules['min_contrast_ratio']
            
            if contrast < min_contrast:
                self.errors.append(
                    f"Contrast ratio {contrast:.2f} < minimum {min_contrast}"
                )
                return False
            
            return True
        
        except Exception as e:
            self.errors.append(f"Error calculating contrast: {e}")
            return False
    
    def get_errors(self) -> List[str]:
        """Get list of validation errors"""
        return self.errors.copy()
    
    def clear_errors(self):
        """Clear error list"""
        self.errors.clear()


def validate_icon_elements(elements: List[Dict], size: int) -> Tuple[bool, List[str]]:
    """
    Validate all elements in an icon
    
    Args:
        elements: List of element dictionaries
        size: Icon size
        
    Returns:
        Tuple of (is_valid, error_list)
    """
    validator = GeometryValidator(size)
    all_errors = []
    
    for i, element in enumerate(elements):
        if not validator.validate_element(element):
            errors = validator.get_errors()
            all_errors.extend([f"Element {i} ({element.get('type', 'unknown')}): {err}" 
                             for err in errors])
    
    return len(all_errors) == 0, all_errors
