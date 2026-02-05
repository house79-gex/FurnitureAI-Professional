"""
Base icon class with adaptive scaling logic
"""

import sys
import os
from abc import ABC, abstractmethod
from typing import Dict, List, Optional

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import COLORS, RESOLUTIONS, DETAIL_LEVELS, VALIDATION_RULES
from core.svg_builder import SVGBuilder
from core.utils import scale_value, ensure_min_size


class IconBase(ABC):
    """
    Base class for all icons with adaptive scaling
    """
    
    def __init__(self, name: str, category: str, description: str):
        """
        Initialize icon
        
        Args:
            name: Icon name (e.g., "FAI_LayoutIA")
            category: Category/panel name
            description: Icon description
        """
        self.name = name
        self.category = category
        self.description = description
        self.colors = COLORS
        
    @abstractmethod
    def generate_16px(self, builder: SVGBuilder) -> SVGBuilder:
        """
        Generate 16x16 minimalist version
        
        Args:
            builder: SVG builder instance
            
        Returns:
            Modified builder
        """
        pass
    
    @abstractmethod
    def generate_32px(self, builder: SVGBuilder) -> SVGBuilder:
        """
        Generate 32x32 balanced version
        
        Args:
            builder: SVG builder instance
            
        Returns:
            Modified builder
        """
        pass
    
    @abstractmethod
    def generate_64px(self, builder: SVGBuilder) -> SVGBuilder:
        """
        Generate 64x64 balanced version
        
        Args:
            builder: SVG builder instance
            
        Returns:
            Modified builder
        """
        pass
    
    @abstractmethod
    def generate_128px(self, builder: SVGBuilder) -> SVGBuilder:
        """
        Generate 128x128 detailed version
        
        Args:
            builder: SVG builder instance
            
        Returns:
            Modified builder
        """
        pass
    
    def generate(self, size: int) -> SVGBuilder:
        """
        Generate icon at specified size
        
        Args:
            size: Icon size (16, 32, 64, or 128)
            
        Returns:
            SVG builder with icon
        """
        if size not in RESOLUTIONS:
            raise ValueError(f"Invalid size {size}. Must be one of {RESOLUTIONS}")
        
        builder = SVGBuilder(size, size, self.name)
        
        if size == 16:
            return self.generate_16px(builder)
        elif size == 32:
            return self.generate_32px(builder)
        elif size == 64:
            return self.generate_64px(builder)
        elif size == 128:
            return self.generate_128px(builder)
    
    def generate_all_sizes(self) -> Dict[int, SVGBuilder]:
        """
        Generate icon at all resolutions
        
        Returns:
            Dictionary mapping size to SVG builder
        """
        return {size: self.generate(size) for size in RESOLUTIONS}
    
    def save_svg(self, size: int, output_dir: str) -> str:
        """
        Generate and save SVG file
        
        Args:
            size: Icon size
            output_dir: Output directory
            
        Returns:
            Path to saved file
        """
        builder = self.generate(size)
        filename = os.path.join(output_dir, f"{self.name}_{size}.svg")
        builder.save(filename)
        return filename
    
    def save_all_svgs(self, output_dir: str) -> List[str]:
        """
        Generate and save all SVG sizes
        
        Args:
            output_dir: Output directory
            
        Returns:
            List of saved file paths
        """
        os.makedirs(output_dir, exist_ok=True)
        return [self.save_svg(size, output_dir) for size in RESOLUTIONS]
    
    def get_metadata(self) -> Dict:
        """
        Get icon metadata
        
        Returns:
            Metadata dictionary
        """
        return {
            'name': self.name,
            'category': self.category,
            'description': self.description,
            'resolutions': RESOLUTIONS,
            'detail_levels': {
                size: DETAIL_LEVELS[size] for size in RESOLUTIONS
            }
        }
    
    def get_min_stroke_width(self, size: int) -> float:
        """
        Get minimum stroke width for size
        
        Args:
            size: Icon size
            
        Returns:
            Minimum stroke width
        """
        return VALIDATION_RULES['min_stroke_width'].get(size, 1)
    
    def scale_stroke_width(self, base_width: float, from_size: int, to_size: int) -> float:
        """
        Scale stroke width proportionally while respecting minimums
        
        Args:
            base_width: Base stroke width
            from_size: Source size
            to_size: Target size
            
        Returns:
            Scaled stroke width
        """
        scaled = scale_value(base_width, from_size, to_size)
        min_width = self.get_min_stroke_width(to_size)
        return ensure_min_size(scaled, min_width)
    
    def get_padding(self, size: int, relative: float = 0.1) -> float:
        """
        Get padding for icon at size
        
        Args:
            size: Icon size
            relative: Relative padding (fraction of size)
            
        Returns:
            Padding in pixels
        """
        return max(2, size * relative)


class SimpleShapeIcon(IconBase):
    """
    Helper class for icons based on simple geometric shapes
    Provides common shape-building methods
    """
    
    def add_cabinet_shape(self, builder: SVGBuilder, x: float, y: float, 
                         width: float, height: float, size: int) -> SVGBuilder:
        """
        Add a basic cabinet shape
        
        Args:
            builder: SVG builder
            x, y: Position
            width, height: Dimensions
            size: Icon size for stroke scaling
            
        Returns:
            Modified builder
        """
        stroke_width = self.get_min_stroke_width(size)
        
        # Main cabinet body
        builder.add_rect(
            x, y, width, height,
            fill=self.colors['very_light_gray'],
            stroke=self.colors['blue'],
            stroke_width=stroke_width
        )
        
        return builder
    
    def add_handle(self, builder: SVGBuilder, x: float, y: float, 
                   size: int, handle_type: str = 'circle') -> SVGBuilder:
        """
        Add a handle to a cabinet/drawer
        
        Args:
            builder: SVG builder
            x, y: Handle position
            size: Icon size
            handle_type: 'circle' or 'bar'
            
        Returns:
            Modified builder
        """
        if handle_type == 'circle':
            r = max(2, size * 0.05)
            builder.add_circle(x, y, r, fill=self.colors['medium_gray'])
        elif handle_type == 'bar':
            bar_width = max(4, size * 0.2)
            bar_height = max(2, size * 0.03)
            builder.add_rect(
                x - bar_width/2, y - bar_height/2,
                bar_width, bar_height,
                fill=self.colors['medium_gray'],
                rx=bar_height/2
            )
        
        return builder
    
    def add_ai_brain(self, builder: SVGBuilder, cx: float, cy: float, 
                     radius: float, size: int) -> SVGBuilder:
        """
        Add AI brain symbol
        
        Args:
            builder: SVG builder
            cx, cy: Center position
            radius: Brain radius
            size: Icon size
            
        Returns:
            Modified builder
        """
        # Brain circle
        builder.add_circle(
            cx, cy, radius,
            fill=self.colors['purple'],
            opacity=0.9
        )
        
        # Add nodes if size permits
        if size >= 32:
            node_r = max(1, radius * 0.2)
            # Add small neural network nodes
            for angle in [0, 120, 240]:
                import math
                node_x = cx + radius * 0.5 * math.cos(math.radians(angle))
                node_y = cy + radius * 0.5 * math.sin(math.radians(angle))
                builder.add_circle(node_x, node_y, node_r, fill=self.colors['white'])
        
        return builder
