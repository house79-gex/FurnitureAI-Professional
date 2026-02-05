"""
SVG Builder with validation and optimization
"""

import sys
import os
from typing import Dict, List, Optional, Tuple

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.validators import GeometryValidator
from core.utils import round_to_half


class SVGBuilder:
    """Builds SVG documents with validation"""
    
    def __init__(self, width: int, height: int, icon_name: str = "icon"):
        """
        Initialize SVG builder
        
        Args:
            width: SVG width
            height: SVG height
            icon_name: Name for the icon (used in IDs)
        """
        self.width = width
        self.height = height
        self.icon_name = icon_name
        self.elements = []
        self.defs = []
        self.validator = GeometryValidator(width)
        
    def add_rect(self, x: float, y: float, width: float, height: float, 
                 fill: Optional[str] = None, stroke: Optional[str] = None,
                 stroke_width: Optional[float] = None, opacity: float = 1.0,
                 rx: float = 0, ry: float = 0, element_id: Optional[str] = None) -> 'SVGBuilder':
        """Add a rectangle element"""
        element = {
            'type': 'rect',
            'x': round_to_half(x),
            'y': round_to_half(y),
            'width': round_to_half(width),
            'height': round_to_half(height),
            'rx': rx,
            'ry': ry,
        }
        
        if fill:
            element['fill'] = fill
        if stroke:
            element['stroke'] = stroke
        if stroke_width is not None:
            element['stroke_width'] = stroke_width
        if opacity != 1.0:
            element['opacity'] = opacity
        if element_id:
            element['id'] = element_id
        
        self.elements.append(element)
        return self
    
    def add_circle(self, cx: float, cy: float, r: float,
                   fill: Optional[str] = None, stroke: Optional[str] = None,
                   stroke_width: Optional[float] = None, opacity: float = 1.0,
                   element_id: Optional[str] = None) -> 'SVGBuilder':
        """Add a circle element"""
        element = {
            'type': 'circle',
            'cx': round_to_half(cx),
            'cy': round_to_half(cy),
            'r': round_to_half(r),
        }
        
        if fill:
            element['fill'] = fill
        if stroke:
            element['stroke'] = stroke
        if stroke_width is not None:
            element['stroke_width'] = stroke_width
        if opacity != 1.0:
            element['opacity'] = opacity
        if element_id:
            element['id'] = element_id
        
        self.elements.append(element)
        return self
    
    def add_ellipse(self, cx: float, cy: float, rx: float, ry: float,
                    fill: Optional[str] = None, stroke: Optional[str] = None,
                    stroke_width: Optional[float] = None, opacity: float = 1.0,
                    element_id: Optional[str] = None) -> 'SVGBuilder':
        """Add an ellipse element"""
        element = {
            'type': 'ellipse',
            'cx': round_to_half(cx),
            'cy': round_to_half(cy),
            'rx': round_to_half(rx),
            'ry': round_to_half(ry),
        }
        
        if fill:
            element['fill'] = fill
        if stroke:
            element['stroke'] = stroke
        if stroke_width is not None:
            element['stroke_width'] = stroke_width
        if opacity != 1.0:
            element['opacity'] = opacity
        if element_id:
            element['id'] = element_id
        
        self.elements.append(element)
        return self
    
    def add_line(self, x1: float, y1: float, x2: float, y2: float,
                 stroke: str = '#000000', stroke_width: float = 1,
                 opacity: float = 1.0, stroke_dasharray: Optional[str] = None,
                 element_id: Optional[str] = None) -> 'SVGBuilder':
        """Add a line element"""
        element = {
            'type': 'line',
            'x1': round_to_half(x1),
            'y1': round_to_half(y1),
            'x2': round_to_half(x2),
            'y2': round_to_half(y2),
            'stroke': stroke,
            'stroke_width': stroke_width,
        }
        
        if opacity != 1.0:
            element['opacity'] = opacity
        if stroke_dasharray:
            element['stroke_dasharray'] = stroke_dasharray
        if element_id:
            element['id'] = element_id
        
        self.elements.append(element)
        return self
    
    def add_path(self, d: str, fill: Optional[str] = None, 
                 stroke: Optional[str] = None, stroke_width: Optional[float] = None,
                 opacity: float = 1.0, element_id: Optional[str] = None) -> 'SVGBuilder':
        """Add a path element"""
        element = {
            'type': 'path',
            'd': d,
        }
        
        if fill:
            element['fill'] = fill
        if stroke:
            element['stroke'] = stroke
        if stroke_width is not None:
            element['stroke_width'] = stroke_width
        if opacity != 1.0:
            element['opacity'] = opacity
        if element_id:
            element['id'] = element_id
        
        self.elements.append(element)
        return self
    
    def add_polygon(self, points: List[Tuple[float, float]], 
                    fill: Optional[str] = None, stroke: Optional[str] = None,
                    stroke_width: Optional[float] = None, opacity: float = 1.0,
                    element_id: Optional[str] = None) -> 'SVGBuilder':
        """Add a polygon element"""
        points_str = ' '.join([f"{round_to_half(x)},{round_to_half(y)}" 
                               for x, y in points])
        
        element = {
            'type': 'polygon',
            'points': points_str,
        }
        
        if fill:
            element['fill'] = fill
        if stroke:
            element['stroke'] = stroke
        if stroke_width is not None:
            element['stroke_width'] = stroke_width
        if opacity != 1.0:
            element['opacity'] = opacity
        if element_id:
            element['id'] = element_id
        
        self.elements.append(element)
        return self
    
    def add_text(self, x: float, y: float, text: str, 
                 font_size: int = 12, font_family: str = "Arial",
                 fill: str = "#000000", text_anchor: str = "start",
                 font_weight: str = "normal", element_id: Optional[str] = None) -> 'SVGBuilder':
        """Add a text element"""
        element = {
            'type': 'text',
            'x': round_to_half(x),
            'y': round_to_half(y),
            'text': text,
            'font_size': font_size,
            'font_family': font_family,
            'fill': fill,
            'text_anchor': text_anchor,
            'font_weight': font_weight,
        }
        
        if element_id:
            element['id'] = element_id
        
        self.elements.append(element)
        return self
    
    def add_linear_gradient(self, gradient_id: str, x1: str = "0%", y1: str = "0%",
                           x2: str = "100%", y2: str = "0%",
                           stops: List[Tuple[str, str, float]] = None) -> 'SVGBuilder':
        """
        Add a linear gradient definition
        
        Args:
            gradient_id: Unique ID for the gradient
            x1, y1, x2, y2: Gradient direction
            stops: List of (offset, color, opacity) tuples
        """
        gradient = {
            'type': 'linearGradient',
            'id': gradient_id,
            'x1': x1,
            'y1': y1,
            'x2': x2,
            'y2': y2,
            'stops': stops or []
        }
        
        self.defs.append(gradient)
        return self
    
    def validate(self) -> Tuple[bool, List[str]]:
        """
        Validate all elements
        
        Returns:
            Tuple of (is_valid, error_list)
        """
        errors = []
        
        for i, element in enumerate(self.elements):
            if not self.validator.validate_element(element):
                element_errors = self.validator.get_errors()
                errors.extend([f"Element {i}: {err}" for err in element_errors])
        
        return len(errors) == 0, errors
    
    def to_svg_string(self) -> str:
        """
        Generate SVG string
        
        Returns:
            Complete SVG document as string
        """
        svg_parts = [
            f'<?xml version="1.0" encoding="UTF-8"?>',
            f'<svg width="{self.width}" height="{self.height}" '
            f'viewBox="0 0 {self.width} {self.height}" '
            f'xmlns="http://www.w3.org/2000/svg">'
        ]
        
        # Add defs if any
        if self.defs:
            svg_parts.append('  <defs>')
            for def_element in self.defs:
                if def_element['type'] == 'linearGradient':
                    svg_parts.append(
                        f'    <linearGradient id="{def_element["id"]}" '
                        f'x1="{def_element["x1"]}" y1="{def_element["y1"]}" '
                        f'x2="{def_element["x2"]}" y2="{def_element["y2"]}">'
                    )
                    for offset, color, opacity in def_element['stops']:
                        svg_parts.append(
                            f'      <stop offset="{offset}" stop-color="{color}" '
                            f'stop-opacity="{opacity}"/>'
                        )
                    svg_parts.append('    </linearGradient>')
            svg_parts.append('  </defs>')
        
        # Add elements
        for element in self.elements:
            svg_parts.append('  ' + self._element_to_svg(element))
        
        svg_parts.append('</svg>')
        
        return '\n'.join(svg_parts)
    
    def _element_to_svg(self, element: Dict) -> str:
        """Convert element dictionary to SVG string"""
        elem_type = element['type']
        
        if elem_type == 'rect':
            attrs = [
                f'x="{element["x"]}"',
                f'y="{element["y"]}"',
                f'width="{element["width"]}"',
                f'height="{element["height"]}"',
            ]
            if element.get('rx', 0) > 0:
                attrs.append(f'rx="{element["rx"]}"')
            if element.get('ry', 0) > 0:
                attrs.append(f'ry="{element["ry"]}"')
                
        elif elem_type == 'circle':
            attrs = [
                f'cx="{element["cx"]}"',
                f'cy="{element["cy"]}"',
                f'r="{element["r"]}"',
            ]
            
        elif elem_type == 'ellipse':
            attrs = [
                f'cx="{element["cx"]}"',
                f'cy="{element["cy"]}"',
                f'rx="{element["rx"]}"',
                f'ry="{element["ry"]}"',
            ]
            
        elif elem_type == 'line':
            attrs = [
                f'x1="{element["x1"]}"',
                f'y1="{element["y1"]}"',
                f'x2="{element["x2"]}"',
                f'y2="{element["y2"]}"',
            ]
            
        elif elem_type == 'path':
            attrs = [f'd="{element["d"]}"']
            
        elif elem_type == 'polygon':
            attrs = [f'points="{element["points"]}"']
            
        elif elem_type == 'text':
            return (f'<text x="{element["x"]}" y="{element["y"]}" '
                   f'font-size="{element["font_size"]}" '
                   f'font-family="{element["font_family"]}" '
                   f'fill="{element["fill"]}" '
                   f'text-anchor="{element["text_anchor"]}" '
                   f'font-weight="{element["font_weight"]}"'
                   f'{" id=\"" + element["id"] + "\"" if "id" in element else ""}>'
                   f'{element["text"]}</text>')
        else:
            return f'<!-- Unknown element type: {elem_type} -->'
        
        # Add common attributes
        if 'fill' in element:
            attrs.append(f'fill="{element["fill"]}"')
        if 'stroke' in element:
            attrs.append(f'stroke="{element["stroke"]}"')
        if 'stroke_width' in element:
            attrs.append(f'stroke-width="{element["stroke_width"]}"')
        if 'opacity' in element and element['opacity'] != 1.0:
            attrs.append(f'opacity="{element["opacity"]}"')
        if 'stroke_dasharray' in element:
            attrs.append(f'stroke-dasharray="{element["stroke_dasharray"]}"')
        if 'id' in element:
            attrs.append(f'id="{element["id"]}"')
        
        return f'<{elem_type} {" ".join(attrs)} />'
    
    def save(self, filename: str) -> bool:
        """
        Save SVG to file
        
        Args:
            filename: Output filename
            
        Returns:
            True if successful
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(self.to_svg_string())
            return True
        except Exception as e:
            print(f"Error saving SVG: {e}")
            return False
