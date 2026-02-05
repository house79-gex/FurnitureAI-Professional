"""
Lavorazioni Panel Icon Generators
3 icons: FAI_Forature, FAI_Giunzioni, FAI_Scanalature
"""

import sys
import os
import math

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.icon_base import IconBase, SimpleShapeIcon, IconGenerator
from core.svg_builder import SVGBuilder


class FAI_Forature(SimpleShapeIcon):
    """Drilling - panel with 32mm system holes"""
    
    def __init__(self):
        super().__init__(
            name="FAI_Forature",
            category="Lavorazioni",
            description="Forature sistema 32mm"
        )
    
    def generate_16px(self, builder: SVGBuilder) -> SVGBuilder:
        """16px: Panel with holes"""
        # Panel
        builder.add_rect(2, 2, 12, 12, fill=self.colors['very_light_gray'], 
                        stroke=self.colors['blue'], stroke_width=1.5)
        
        # Holes
        for y in [5, 9, 13]:
            builder.add_circle(8, y, 1.5, fill=self.colors['medium_gray'])
        
        return builder
    
    def generate_32px(self, builder: SVGBuilder) -> SVGBuilder:
        """32px: Panel with 32mm system"""
        # Panel
        builder.add_rect(4, 4, 24, 24, fill=self.colors['very_light_gray'], 
                        stroke=self.colors['blue'], stroke_width=2)
        
        # 32mm system holes (side)
        for i in range(4):
            y = 8 + i * 6
            builder.add_circle(8, y, 2, fill=self.colors['medium_gray'])
            builder.add_circle(8, y, 1, fill=self.colors['dark_gray'])
        
        # Drill bit indicator
        builder.add_line(20, 4, 20, 12, stroke=self.colors['orange'], stroke_width=2)
        builder.add_polygon([(20, 12), (18, 10), (22, 10)], fill=self.colors['orange'])
        
        return builder
    
    def generate_64px(self, builder: SVGBuilder) -> SVGBuilder:
        """64px: Detailed drilling pattern"""
        # Panel
        builder.add_rect(8, 8, 48, 48, fill=self.colors['very_light_gray'], 
                        stroke=self.colors['blue'], stroke_width=2)
        
        # 32mm system - vertical pattern
        for i in range(7):
            y = 12 + i * 7
            # Hole with depth
            builder.add_circle(16, y, 3, fill=self.colors['medium_gray'])
            builder.add_circle(16, y, 2, fill=self.colors['dark_gray'])
            builder.add_circle(16, y, 1, fill=self.colors['black'])
        
        # Measurement lines
        builder.add_line(20, 12, 24, 12, stroke=self.colors['orange'], stroke_width=1)
        builder.add_line(20, 19, 24, 19, stroke=self.colors['orange'], stroke_width=1)
        builder.add_line(22, 12, 22, 19, stroke=self.colors['orange'], stroke_width=1)
        
        # Drill bit
        builder.add_rect(40, 8, 4, 16, fill=self.colors['orange'])
        builder.add_polygon([(42, 24), (38, 28), (46, 28)], fill=self.colors['dark_gray'])
        
        return builder
    
    def generate_128px(self, builder: SVGBuilder) -> SVGBuilder:
        """128px: Complete drilling system with dimensions"""
        # Panel with edge detail
        builder.add_rect(16, 16, 96, 96, fill=self.colors['very_light_gray'], 
                        stroke=self.colors['blue'], stroke_width=3)
        
        # Edge banding
        builder.add_rect(16, 16, 96, 4, fill=self.colors['light_gray'])
        builder.add_rect(16, 16, 4, 96, fill=self.colors['light_gray'])
        
        # 32mm system holes - two vertical rows
        for col in [32, 96]:
            for i in range(11):
                y = 24 + i * 8
                # 3D hole effect
                builder.add_circle(col, y, 4, fill=self.colors['medium_gray'])
                builder.add_circle(col, y, 3, fill=self.colors['dark_gray'])
                builder.add_circle(col, y, 2, fill=self.colors['black'])
                
                # Highlight
                builder.add_circle(col-1, y-1, 1, fill=self.colors['light_gray'], opacity=0.5)
        
        # Dimension lines for 32mm spacing
        builder.add_line(108, 24, 112, 24, stroke=self.colors['orange'], stroke_width=2)
        builder.add_line(108, 32, 112, 32, stroke=self.colors['orange'], stroke_width=2)
        builder.add_line(110, 24, 110, 32, stroke=self.colors['orange'], stroke_width=2)
        
        # Drill bit with motor
        builder.add_rect(60, 16, 8, 32, fill=self.colors['orange'], rx=1)
        builder.add_circle(64, 16, 6, fill=self.colors['medium_gray'])
        builder.add_polygon([(64, 48), (60, 54), (68, 54)], fill=self.colors['dark_gray'])
        
        # Drill flutes
        for i in range(6):
            builder.add_line(62, 20+i*4, 62, 22+i*4, stroke=self.colors['orange_light'], stroke_width=1)
        
        # Depth indicator
        builder.add_circle(64, 64, 20, fill='none', stroke=self.colors['green'], 
                          stroke_width=2, stroke_dasharray="4,4")
        
        return builder


class FAI_Giunzioni(SimpleShapeIcon):
    """Wood joints - dowel joint connection"""
    
    def __init__(self):
        super().__init__(
            name="FAI_Giunzioni",
            category="Lavorazioni",
            description="Giunzioni e assemblaggio"
        )
    
    def generate_16px(self, builder: SVGBuilder) -> SVGBuilder:
        """16px: Simple joint"""
        # Two pieces
        builder.add_rect(2, 4, 6, 8, fill=self.colors['very_light_gray'], 
                        stroke=self.colors['blue'], stroke_width=1)
        builder.add_rect(8, 4, 6, 8, fill=self.colors['light_gray'], 
                        stroke=self.colors['blue'], stroke_width=1)
        
        # Dowel
        builder.add_circle(8, 8, 2, fill=self.colors['medium_gray'])
        
        return builder
    
    def generate_32px(self, builder: SVGBuilder) -> SVGBuilder:
        """32px: Dowel joint"""
        # Left panel
        builder.add_rect(4, 8, 10, 16, fill=self.colors['very_light_gray'], 
                        stroke=self.colors['blue'], stroke_width=2)
        
        # Right panel
        builder.add_rect(18, 8, 10, 16, fill=self.colors['light_gray'], 
                        stroke=self.colors['blue'], stroke_width=2)
        
        # Dowels
        for y in [12, 20]:
            builder.add_circle(14, y, 2.5, fill=self.colors['medium_gray'])
            builder.add_circle(18, y, 2.5, fill=self.colors['medium_gray'])
        
        return builder
    
    def generate_64px(self, builder: SVGBuilder) -> SVGBuilder:
        """64px: Detailed joint with dowels"""
        # Left panel (side view)
        builder.add_rect(8, 16, 20, 32, fill=self.colors['very_light_gray'], 
                        stroke=self.colors['blue'], stroke_width=2)
        
        # Right panel
        builder.add_rect(36, 16, 20, 32, fill=self.colors['light_gray'], 
                        stroke=self.colors['blue'], stroke_width=2)
        
        # Dowels with detail
        for y in [24, 32, 40]:
            # Left side dowel
            builder.add_ellipse(28, y, 8, 3, fill=self.colors['medium_gray'])
            builder.add_ellipse(28, y, 6, 2, fill=self.colors['light_gray'])
            
            # Right side hole
            builder.add_circle(36, y, 3, fill=self.colors['dark_gray'])
        
        # Glue indication
        for y in [20, 44]:
            builder.add_circle(28, y, 1.5, fill=self.colors['yellow'], opacity=0.7)
        
        return builder
    
    def generate_128px(self, builder: SVGBuilder) -> SVGBuilder:
        """128px: Complete joint assembly"""
        # Left panel with wood grain
        builder.add_rect(16, 32, 40, 64, fill=self.colors['very_light_gray'], 
                        stroke=self.colors['blue'], stroke_width=3)
        
        # Wood grain
        for i in range(8):
            builder.add_path(f"M 20 {36+i*8} Q 36 {37+i*8} 52 {36+i*8}", 
                           stroke=self.colors['light_gray'], stroke_width=0.5, fill='none')
        
        # Right panel
        builder.add_rect(72, 32, 40, 64, fill=self.colors['light_gray'], 
                        stroke=self.colors['blue'], stroke_width=3)
        
        # Multiple dowels
        for y in [48, 64, 80]:
            # Dowel protruding from left
            builder.add_ellipse(56, y, 16, 6, fill=self.colors['medium_gray'])
            builder.add_ellipse(56, y, 12, 4, fill=self.colors['light_gray'])
            
            # Grooves on dowel
            for i in range(3):
                builder.add_line(52-i*4, y-2, 52-i*4, y+2, 
                               stroke=self.colors['dark_gray'], stroke_width=1)
            
            # Receiving hole in right panel
            builder.add_circle(72, y, 6, fill=self.colors['dark_gray'])
            builder.add_circle(72, y, 4, fill=self.colors['black'])
        
        # Glue application
        for y in [44, 68, 88]:
            for x in range(3):
                builder.add_circle(58 + x*4, y, 2, fill=self.colors['yellow'], opacity=0.6)
        
        # Assembly arrow
        builder.add_line(56, 16, 72, 16, stroke=self.colors['green'], stroke_width=4)
        builder.add_polygon([(72, 16), (66, 12), (66, 20)], fill=self.colors['green'])
        
        # Measurement lines
        builder.add_line(16, 48, 72, 48, stroke=self.colors['orange'], stroke_width=1, 
                        stroke_dasharray="4,4", opacity=0.5)
        
        return builder


class FAI_Scanalature(SimpleShapeIcon):
    """Grooves - panel with groove cuts"""
    
    def __init__(self):
        super().__init__(
            name="FAI_Scanalature",
            category="Lavorazioni",
            description="Scanalature e fresature"
        )
    
    def generate_16px(self, builder: SVGBuilder) -> SVGBuilder:
        """16px: Panel with groove"""
        # Panel
        builder.add_rect(2, 2, 12, 12, fill=self.colors['very_light_gray'], 
                        stroke=self.colors['blue'], stroke_width=1.5)
        
        # Groove
        builder.add_rect(6, 2, 4, 12, fill=self.colors['medium_gray'])
        
        return builder
    
    def generate_32px(self, builder: SVGBuilder) -> SVGBuilder:
        """32px: Panel with groove detail"""
        # Panel
        builder.add_rect(4, 4, 24, 24, fill=self.colors['very_light_gray'], 
                        stroke=self.colors['blue'], stroke_width=2)
        
        # Groove with depth
        builder.add_rect(12, 4, 8, 24, fill=self.colors['medium_gray'])
        builder.add_rect(14, 4, 4, 24, fill=self.colors['dark_gray'])
        
        # Router bit indicator
        builder.add_circle(16, 8, 3, fill=self.colors['orange'], opacity=0.7)
        
        return builder
    
    def generate_64px(self, builder: SVGBuilder) -> SVGBuilder:
        """64px: Detailed groove cutting"""
        # Panel (3D view)
        builder.add_rect(8, 16, 48, 40, fill=self.colors['very_light_gray'], 
                        stroke=self.colors['blue'], stroke_width=2)
        
        # Vertical groove
        builder.add_rect(24, 16, 10, 40, fill=self.colors['medium_gray'])
        builder.add_rect(26, 16, 6, 40, fill=self.colors['dark_gray'])
        
        # Groove profile (side view)
        builder.add_polygon([(26, 14), (24, 16), (34, 16), (32, 14)], 
                           fill=self.colors['light_gray'])
        
        # Router bit
        builder.add_circle(29, 8, 6, fill=self.colors['orange'], opacity=0.8)
        builder.add_rect(27, 2, 4, 6, fill=self.colors['orange'])
        
        # Depth indicator
        builder.add_line(38, 16, 38, 26, stroke=self.colors['green'], stroke_width=2)
        builder.add_line(36, 16, 40, 16, stroke=self.colors['green'], stroke_width=1)
        builder.add_line(36, 26, 40, 26, stroke=self.colors['green'], stroke_width=1)
        
        return builder
    
    def generate_128px(self, builder: SVGBuilder) -> SVGBuilder:
        """128px: Complete grooving operation"""
        # Panel with 3D perspective
        builder.add_rect(16, 32, 96, 80, fill=self.colors['very_light_gray'], 
                        stroke=self.colors['blue'], stroke_width=3)
        
        # Multiple grooves
        groove_positions = [40, 64, 88]
        for x in groove_positions:
            # Groove with 3D depth
            builder.add_rect(x, 32, 12, 80, fill=self.colors['medium_gray'])
            builder.add_rect(x+2, 32, 8, 80, fill=self.colors['dark_gray'])
            builder.add_rect(x+4, 32, 4, 80, fill=self.colors['black'])
            
            # Top bevel
            builder.add_polygon([(x, 32), (x+2, 30), (x+10, 30), (x+12, 32)], 
                               fill=self.colors['light_gray'])
        
        # Router bit with motor
        builder.add_rect(60, 8, 12, 16, fill=self.colors['orange'], rx=2)
        builder.add_circle(66, 8, 8, fill=self.colors['medium_gray'], 
                          stroke=self.colors['dark_gray'], stroke_width=2)
        
        # Cutting bit
        builder.add_polygon([(66, 24), (62, 32), (70, 32)], fill=self.colors['dark_gray'])
        
        # Rotation indicator
        for angle in [0, 60, 120, 180, 240, 300]:
            rad = math.radians(angle)
            x1 = 66 + 12 * math.cos(rad)
            y1 = 16 + 12 * math.sin(rad)
            x2 = 66 + 14 * math.cos(rad)
            y2 = 16 + 14 * math.sin(rad)
            builder.add_line(x1, y1, x2, y2, stroke=self.colors['orange_light'], stroke_width=1)
        
        # Depth measurements
        for x in groove_positions:
            builder.add_line(x+12, 40, x+20, 40, stroke=self.colors['green'], stroke_width=1.5)
            builder.add_line(x+20, 32, x+20, 48, stroke=self.colors['green'], stroke_width=1.5)
            builder.add_line(x+18, 32, x+22, 32, stroke=self.colors['green'], stroke_width=1)
            builder.add_line(x+18, 48, x+22, 48, stroke=self.colors['green'], stroke_width=1)
        
        # Wood chips
        for i in range(5):
            builder.add_circle(64 + i*8, 116, 2, fill=self.colors['orange'], opacity=0.5)
        
        return builder


class LavorazioniGenerator(IconGenerator):
    """Generator for Lavorazioni Panel icons"""
    
    def __init__(self):
        super().__init__()
    
    def get_icons(self):
        """Return dict of icon names to methods"""
        return {
            'FAI_Forature': self._generate_forature,
            'FAI_Giunzioni': self._generate_giunzioni,
            'FAI_Scanalature': self._generate_scanalature,
        }
    
    def _generate_forature(self, size):
        icon = FAI_Forature()
        builder = self._create_svg(size)
        if size == 16:
            return icon.generate_16px(builder).get_svg()
        elif size == 32:
            return icon.generate_32px(builder).get_svg()
        elif size == 64:
            return icon.generate_64px(builder).get_svg()
        else:
            return icon.generate_128px(builder).get_svg()
    
    def _generate_giunzioni(self, size):
        icon = FAI_Giunzioni()
        builder = self._create_svg(size)
        if size == 16:
            return icon.generate_16px(builder).get_svg()
        elif size == 32:
            return icon.generate_32px(builder).get_svg()
        elif size == 64:
            return icon.generate_64px(builder).get_svg()
        else:
            return icon.generate_128px(builder).get_svg()
    
    def _generate_scanalature(self, size):
        icon = FAI_Scanalature()
        builder = self._create_svg(size)
        if size == 16:
            return icon.generate_16px(builder).get_svg()
        elif size == 32:
            return icon.generate_32px(builder).get_svg()
        elif size == 64:
            return icon.generate_64px(builder).get_svg()
        else:
            return icon.generate_128px(builder).get_svg()


# Export all classes
__all__ = [
    'FAI_Forature',
    'FAI_Giunzioni',
    'FAI_Scanalature',
    'LavorazioniGenerator'
]
