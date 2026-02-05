"""
SVG Builder with validation
FIXED: Added stroke_dasharray support to all methods
"""

import xml.etree.ElementTree as ET
from xml.dom import minidom

class SVGBuilder:
    """Builder class for creating SVG elements with validation"""
    
    def __init__(self, width, height, viewBox=None):
        """
        Initialize SVG builder
        
        Args:
            width: SVG width
            height: SVG height
            viewBox: Optional viewBox (default: "0 0 width height")
        """
        self.width = width
        self.height = height
        self.viewBox = viewBox or f"0 0 {width} {height}"
        
        # Create root SVG element
        self.root = ET.Element('svg', {
            'xmlns': 'http://www.w3.org/2000/svg',
            'width': str(width),
            'height': str(height),
            'viewBox': self.viewBox
        })
        
        # Create defs element for gradients, filters, etc.
        self.defs = ET.SubElement(self.root, 'defs')
    
    def _format_number(self, num):
        """Format number to reasonable precision"""
        if isinstance(num, (int, float)):
            return f"{num:.3f}".rstrip('0').rstrip('.')
        return str(num)
    
    def add_rect(self, x, y, width, height, fill=None, stroke=None, 
                 stroke_width=None, rx=None, opacity=None, id=None, stroke_dasharray=None):
        """
        Add rectangle element
        
        Args:
            x, y: Position
            width, height: Size
            fill: Fill color
            stroke: Stroke color
            stroke_width: Stroke width
            rx: Corner radius
            opacity: Opacity (0-1)
            id: Element ID
            stroke_dasharray: Dash pattern (e.g., "5,3")
        """
        attrs = {
            'x': self._format_number(x),
            'y': self._format_number(y),
            'width': self._format_number(width),
            'height': self._format_number(height)
        }
        
        if fill:
            attrs['fill'] = fill
        if stroke:
            attrs['stroke'] = stroke
        if stroke_width:
            attrs['stroke-width'] = self._format_number(stroke_width)
        if rx:
            attrs['rx'] = self._format_number(rx)
        if opacity:
            attrs['opacity'] = str(opacity)
        if id:
            attrs['id'] = id
        if stroke_dasharray:
            attrs['stroke-dasharray'] = stroke_dasharray
            
        element = ET.SubElement(self.root, 'rect', attrs)
        return element
    
    def add_circle(self, cx, cy, r, fill=None, stroke=None, 
                   stroke_width=None, opacity=None, id=None, stroke_dasharray=None):
        """
        Add circle element
        
        Args:
            cx, cy: Center position
            r: Radius
            fill: Fill color
            stroke: Stroke color
            stroke_width: Stroke width
            opacity: Opacity (0-1)
            id: Element ID
            stroke_dasharray: Dash pattern (e.g., "5,3")
        """
        attrs = {
            'cx': self._format_number(cx),
            'cy': self._format_number(cy),
            'r': self._format_number(r)
        }
        
        if fill:
            attrs['fill'] = fill
        if stroke:
            attrs['stroke'] = stroke
        if stroke_width:
            attrs['stroke-width'] = self._format_number(stroke_width)
        if opacity:
            attrs['opacity'] = str(opacity)
        if id:
            attrs['id'] = id
        if stroke_dasharray:
            attrs['stroke-dasharray'] = stroke_dasharray
            
        element = ET.SubElement(self.root, 'circle', attrs)
        return element
    
    def add_ellipse(self, cx, cy, rx, ry, fill=None, stroke=None, 
                    stroke_width=None, opacity=None, id=None, stroke_dasharray=None):
        """
        Add ellipse element
        
        Args:
            cx, cy: Center position
            rx, ry: Radii
            fill: Fill color
            stroke: Stroke color
            stroke_width: Stroke width
            opacity: Opacity (0-1)
            id: Element ID
            stroke_dasharray: Dash pattern (e.g., "5,3")
        """
        attrs = {
            'cx': self._format_number(cx),
            'cy': self._format_number(cy),
            'rx': self._format_number(rx),
            'ry': self._format_number(ry)
        }
        
        if fill:
            attrs['fill'] = fill
        if stroke:
            attrs['stroke'] = stroke
        if stroke_width:
            attrs['stroke-width'] = self._format_number(stroke_width)
        if opacity:
            attrs['opacity'] = str(opacity)
        if id:
            attrs['id'] = id
        if stroke_dasharray:
            attrs['stroke-dasharray'] = stroke_dasharray
            
        element = ET.SubElement(self.root, 'ellipse', attrs)
        return element
    
    def add_line(self, x1, y1, x2, y2, stroke=None, stroke_width=None, 
                 opacity=None, id=None, stroke_dasharray=None, stroke_linecap=None):
        """
        Add line element
        
        Args:
            x1, y1: Start position
            x2, y2: End position
            stroke: Stroke color
            stroke_width: Stroke width
            opacity: Opacity (0-1)
            id: Element ID
            stroke_dasharray: Dash pattern (e.g., "5,3")
            stroke_linecap: Line cap style ("round", "square", "butt")
        """
        attrs = {
            'x1': self._format_number(x1),
            'y1': self._format_number(y1),
            'x2': self._format_number(x2),
            'y2': self._format_number(y2)
        }
        
        if stroke:
            attrs['stroke'] = stroke
        if stroke_width:
            attrs['stroke-width'] = self._format_number(stroke_width)
        if opacity:
            attrs['opacity'] = str(opacity)
        if id:
            attrs['id'] = id
        if stroke_dasharray:
            attrs['stroke-dasharray'] = stroke_dasharray
        if stroke_linecap:
            attrs['stroke-linecap'] = stroke_linecap
            
        element = ET.SubElement(self.root, 'line', attrs)
        return element
    
    def add_path(self, d, fill=None, stroke=None, stroke_width=None, 
                 opacity=None, id=None, stroke_dasharray=None, stroke_linecap=None, 
                 stroke_linejoin=None):
        """
        Add path element
        
        Args:
            d: Path data
            fill: Fill color
            stroke: Stroke color
            stroke_width: Stroke width
            opacity: Opacity (0-1)
            id: Element ID
            stroke_dasharray: Dash pattern (e.g., "5,3")
            stroke_linecap: Line cap style
            stroke_linejoin: Line join style
        """
        attrs = {'d': d}
        
        if fill:
            attrs['fill'] = fill
        if stroke:
            attrs['stroke'] = stroke
        if stroke_width:
            attrs['stroke-width'] = self._format_number(stroke_width)
        if opacity:
            attrs['opacity'] = str(opacity)
        if id:
            attrs['id'] = id
        if stroke_dasharray:
            attrs['stroke-dasharray'] = stroke_dasharray
        if stroke_linecap:
            attrs['stroke-linecap'] = stroke_linecap
        if stroke_linejoin:
            attrs['stroke-linejoin'] = stroke_linejoin
            
        element = ET.SubElement(self.root, 'path', attrs)
        return element
    
    def add_polygon(self, points, fill=None, stroke=None, stroke_width=None, 
                    opacity=None, id=None, stroke_dasharray=None):
        """
        Add polygon element
        
        Args:
            points: List of (x, y) tuples
            fill: Fill color
            stroke: Stroke color
            stroke_width: Stroke width
            opacity: Opacity (0-1)
            id: Element ID
            stroke_dasharray: Dash pattern (e.g., "5,3")
        """
        points_str = ' '.join(f"{self._format_number(x)},{self._format_number(y)}" 
                             for x, y in points)
        
        attrs = {'points': points_str}
        
        if fill:
            attrs['fill'] = fill
        if stroke:
            attrs['stroke'] = stroke
        if stroke_width:
            attrs['stroke-width'] = self._format_number(stroke_width)
        if opacity:
            attrs['opacity'] = str(opacity)
        if id:
            attrs['id'] = id
        if stroke_dasharray:
            attrs['stroke-dasharray'] = stroke_dasharray
            
        element = ET.SubElement(self.root, 'polygon', attrs)
        return element
    
    def add_text(self, text, x, y, font_size=None, font_family=None, 
                 font_weight=None, fill=None, text_anchor=None, opacity=None, id=None):
        """
        Add text element
        
        Args:
            text: Text content
            x, y: Position
            font_size: Font size
            font_family: Font family
            font_weight: Font weight
            fill: Text color
            text_anchor: Text anchor ("start", "middle", "end")
            opacity: Opacity (0-1)
            id: Element ID
        """
        attrs = {
            'x': self._format_number(x),
            'y': self._format_number(y)
        }
        
        if font_size:
            attrs['font-size'] = str(font_size)
        if font_family:
            attrs['font-family'] = font_family
        if font_weight:
            attrs['font-weight'] = font_weight
        if fill:
            attrs['fill'] = fill
        if text_anchor:
            attrs['text-anchor'] = text_anchor
        if opacity:
            attrs['opacity'] = str(opacity)
        if id:
            attrs['id'] = id
            
        element = ET.SubElement(self.root, 'text', attrs)
        element.text = text
        return element
    
    def add_group(self, id=None, transform=None, opacity=None):
        """
        Add group element
        
        Args:
            id: Group ID
            transform: Transform attribute
            opacity: Opacity (0-1)
        """
        attrs = {}
        
        if id:
            attrs['id'] = id
        if transform:
            attrs['transform'] = transform
        if opacity:
            attrs['opacity'] = str(opacity)
            
        element = ET.SubElement(self.root, 'g', attrs)
        return element
    
    def add_linear_gradient(self, id, x1="0%", y1="0%", x2="100%", y2="0%"):
        """
        Add linear gradient definition
        
        Args:
            id: Gradient ID
            x1, y1: Start position
            x2, y2: End position
        """
        attrs = {
            'id': id,
            'x1': x1,
            'y1': y1,
            'x2': x2,
            'y2': y2
        }
        
        gradient = ET.SubElement(self.defs, 'linearGradient', attrs)
        return gradient
    
    def add_radial_gradient(self, id, cx="50%", cy="50%", r="50%"):
        """
        Add radial gradient definition
        
        Args:
            id: Gradient ID
            cx, cy: Center position
            r: Radius
        """
        attrs = {
            'id': id,
            'cx': cx,
            'cy': cy,
            'r': r
        }
        
        gradient = ET.SubElement(self.defs, 'radialGradient', attrs)
        return gradient
    
    def add_stop(self, gradient, offset, color, opacity=None):
        """
        Add gradient stop
        
        Args:
            gradient: Gradient element
            offset: Offset position (0-1 or "0%"-"100%")
            color: Stop color
            opacity: Stop opacity
        """
        attrs = {
            'offset': str(offset),
            'stop-color': color
        }
        
        if opacity is not None:
            attrs['stop-opacity'] = str(opacity)
            
        stop = ET.SubElement(gradient, 'stop', attrs)
        return stop
    
    def to_string(self, pretty=True):
        """
        Convert SVG to string
        
        Args:
            pretty: If True, return formatted XML
        """
        if pretty:
            rough_string = ET.tostring(self.root, encoding='unicode')
            reparsed = minidom.parseString(rough_string)
            return reparsed.toprettyxml(indent="  ")
        else:
            return ET.tostring(self.root, encoding='unicode')
    
    def save(self, filepath):
        """
        Save SVG to file
        
        Args:
            filepath: Output file path
        """
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.to_string())
