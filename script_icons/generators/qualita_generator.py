"""
Qualita Panel Icon Generators
3 icons: FAI_Verifica, FAI_Render, FAI_Viewer
"""

import sys
import os
import math

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.icon_base import IconBase, SimpleShapeIcon, IconGenerator
from core.svg_builder import SVGBuilder


class FAI_Verifica(SimpleShapeIcon):
    """Quality check - magnifying glass + checkmark"""
    
    def __init__(self):
        super().__init__(
            name="FAI_Verifica",
            category="Qualita",
            description="Verifica qualità"
        )
    
    def generate_16px(self, builder: SVGBuilder) -> SVGBuilder:
        """16px: Magnifying glass with check"""
        # Magnifying glass
        builder.add_circle(7, 7, 4, fill='none', stroke=self.colors['blue'], stroke_width=2)
        builder.add_line(10, 10, 14, 14, stroke=self.colors['blue'], stroke_width=2)
        
        # Checkmark
        builder.add_path("M 5 7 L 6 8 L 9 5", stroke=self.colors['green'], 
                        stroke_width=2, fill='none')
        
        return builder
    
    def generate_32px(self, builder: SVGBuilder) -> SVGBuilder:
        """32px: Detailed inspection tool"""
        # Magnifying glass lens
        builder.add_circle(14, 14, 8, fill=self.colors['very_light_gray'], 
                          stroke=self.colors['blue'], stroke_width=2)
        builder.add_circle(14, 14, 6, fill='none', stroke=self.colors['blue_light'], stroke_width=1)
        
        # Handle
        builder.add_line(20, 20, 28, 28, stroke=self.colors['dark_gray'], stroke_width=3)
        builder.add_circle(28, 28, 2, fill=self.colors['medium_gray'])
        
        # Checkmark inside lens
        builder.add_path("M 11 14 L 13 16 L 17 12", stroke=self.colors['green'], 
                        stroke_width=2.5, fill='none')
        
        return builder
    
    def generate_64px(self, builder: SVGBuilder) -> SVGBuilder:
        """64px: Quality inspection with details"""
        # Large magnifying glass
        builder.add_circle(28, 28, 16, fill=self.colors['very_light_gray'], 
                          stroke=self.colors['blue'], stroke_width=3)
        builder.add_circle(28, 28, 13, fill='none', stroke=self.colors['blue_light'], 
                          stroke_width=1.5, opacity=0.7)
        
        # Glass reflection
        builder.add_path("M 24 20 Q 28 18 32 20", stroke=self.colors['white'], 
                        stroke_width=2, fill='none', opacity=0.7)
        
        # Handle
        builder.add_line(40, 40, 56, 56, stroke=self.colors['dark_gray'], stroke_width=5)
        builder.add_circle(40, 40, 3, fill=self.colors['medium_gray'])
        builder.add_circle(56, 56, 3, fill=self.colors['medium_gray'])
        
        # Large checkmark
        builder.add_path("M 20 28 L 26 34 L 36 22", stroke=self.colors['green'], 
                        stroke_width=4, fill='none')
        
        return builder
    
    def generate_128px(self, builder: SVGBuilder) -> SVGBuilder:
        """128px: Complete quality control tool"""
        # Large magnifying glass lens
        builder.add_circle(56, 56, 32, fill=self.colors['very_light_gray'], 
                          stroke=self.colors['blue'], stroke_width=4)
        builder.add_circle(56, 56, 28, fill='none', stroke=self.colors['blue_light'], 
                          stroke_width=2, opacity=0.5)
        
        # Inner ring
        builder.add_circle(56, 56, 24, fill='none', stroke=self.colors['blue_light'], 
                          stroke_width=1, opacity=0.3)
        
        # Glass reflections
        builder.add_path("M 44 40 Q 56 36 68 40", stroke=self.colors['white'], 
                        stroke_width=3, fill='none', opacity=0.8)
        builder.add_path("M 48 48 Q 52 46 56 48", stroke=self.colors['white'], 
                        stroke_width=2, fill='none', opacity=0.5)
        
        # Handle with grip
        builder.add_line(80, 80, 112, 112, stroke=self.colors['dark_gray'], stroke_width=8)
        
        # Handle grip texture
        for i in range(5):
            pos = 80 + i * 6.4
            builder.add_circle(pos, pos, 2, fill=self.colors['medium_gray'])
        
        # End caps
        builder.add_circle(80, 80, 5, fill=self.colors['medium_gray'])
        builder.add_circle(112, 112, 5, fill=self.colors['medium_gray'])
        
        # Large checkmark in lens
        builder.add_path("M 40 56 L 52 68 L 72 44", stroke=self.colors['green'], 
                        stroke_width=6, fill='none')
        
        # Quality badge
        builder.add_circle(72, 40, 12, fill=self.colors['green'], opacity=0.9)
        builder.add_path("M 68 40 L 70 42 L 76 36", stroke=self.colors['white'], 
                        stroke_width=3, fill='none')
        
        return builder


class FAI_Render(SimpleShapeIcon):
    """Render - cabinet with realistic lighting"""
    
    def __init__(self):
        super().__init__(
            name="FAI_Render",
            category="Qualita",
            description="Rendering fotorealistico"
        )
    
    def generate_16px(self, builder: SVGBuilder) -> SVGBuilder:
        """16px: Simple cabinet with light"""
        # Cabinet
        builder.add_rect(4, 6, 8, 8, fill=self.colors['very_light_gray'], 
                        stroke=self.colors['blue'], stroke_width=1.5)
        
        # Light source
        builder.add_circle(2, 2, 2, fill=self.colors['yellow'])
        
        return builder
    
    def generate_32px(self, builder: SVGBuilder) -> SVGBuilder:
        """32px: Cabinet with lighting"""
        # Cabinet with gradient effect
        builder.add_rect(8, 12, 16, 16, fill=self.colors['very_light_gray'], 
                        stroke=self.colors['blue'], stroke_width=2)
        
        # Light side
        builder.add_rect(8, 12, 8, 16, fill=self.colors['white'], opacity=0.5)
        
        # Shadow side
        builder.add_rect(16, 12, 8, 16, fill=self.colors['dark_gray'], opacity=0.2)
        
        # Light source
        builder.add_circle(6, 6, 4, fill=self.colors['yellow'], opacity=0.8)
        
        # Light rays
        for angle in [30, 45, 60]:
            rad = math.radians(angle)
            builder.add_line(6, 6, 6 + 8*math.cos(rad), 6 + 8*math.sin(rad), 
                           stroke=self.colors['yellow'], stroke_width=1, opacity=0.5)
        
        return builder
    
    def generate_64px(self, builder: SVGBuilder) -> SVGBuilder:
        """64px: Detailed rendering preview"""
        # Cabinet with 3D effect
        builder.add_rect(16, 24, 32, 32, fill=self.colors['very_light_gray'], 
                        stroke=self.colors['blue'], stroke_width=2)
        
        # Lighting gradient (left to right)
        builder.add_rect(16, 24, 10, 32, fill=self.colors['white'], opacity=0.6)
        builder.add_rect(26, 24, 10, 32, fill=self.colors['white'], opacity=0.3)
        builder.add_rect(36, 24, 12, 32, fill=self.colors['dark_gray'], opacity=0.2)
        
        # Shadow below
        builder.add_ellipse(32, 58, 16, 4, fill=self.colors['black'], opacity=0.3)
        
        # Light source with glow
        builder.add_circle(12, 12, 8, fill=self.colors['yellow'], opacity=0.3)
        builder.add_circle(12, 12, 5, fill=self.colors['yellow'], opacity=0.6)
        builder.add_circle(12, 12, 3, fill=self.colors['yellow'])
        
        # Light rays
        for angle in range(20, 80, 10):
            rad = math.radians(angle)
            builder.add_line(12, 12, 12 + 16*math.cos(rad), 12 + 16*math.sin(rad), 
                           stroke=self.colors['yellow'], stroke_width=1.5, opacity=0.4)
        
        return builder
    
    def generate_128px(self, builder: SVGBuilder) -> SVGBuilder:
        """128px: Photorealistic rendering preview"""
        # Cabinet with detailed lighting
        builder.add_rect(32, 48, 64, 64, fill=self.colors['very_light_gray'], 
                        stroke=self.colors['blue'], stroke_width=3)
        
        # Multiple lighting zones for realism
        builder.add_rect(32, 48, 16, 64, fill=self.colors['white'], opacity=0.7)
        builder.add_rect(48, 48, 16, 64, fill=self.colors['white'], opacity=0.4)
        builder.add_rect(64, 48, 16, 64, fill=self.colors['white'], opacity=0.2)
        builder.add_rect(80, 48, 16, 64, fill=self.colors['dark_gray'], opacity=0.2)
        
        # Handle with reflection
        self.add_handle(builder, 88, 80, 128, 'bar')
        builder.add_rect(86, 78, 2, 8, fill=self.colors['white'], opacity=0.5)
        
        # Cast shadow
        builder.add_ellipse(64, 116, 32, 8, fill=self.colors['black'], opacity=0.4)
        
        # Light source with atmospheric glow
        light_x, light_y = 24, 24
        builder.add_circle(light_x, light_y, 16, fill=self.colors['yellow'], opacity=0.2)
        builder.add_circle(light_x, light_y, 12, fill=self.colors['yellow'], opacity=0.4)
        builder.add_circle(light_x, light_y, 8, fill=self.colors['yellow'], opacity=0.6)
        builder.add_circle(light_x, light_y, 4, fill=self.colors['yellow'])
        
        # Detailed light rays
        for angle in range(15, 90, 8):
            rad = math.radians(angle)
            length = 32 + (angle % 16) * 2
            builder.add_line(light_x, light_y, 
                           light_x + length*math.cos(rad), 
                           light_y + length*math.sin(rad), 
                           stroke=self.colors['yellow'], stroke_width=2, opacity=0.3)
        
        # Render progress indicator
        builder.add_rect(104, 16, 20, 4, fill=self.colors['light_gray'], 
                        stroke=self.colors['medium_gray'], stroke_width=1, rx=2)
        builder.add_rect(104, 16, 14, 4, fill=self.colors['green'], rx=2)
        
        return builder


class FAI_Viewer(SimpleShapeIcon):
    """360° viewer - cabinet with rotation arrows"""
    
    def __init__(self):
        super().__init__(
            name="FAI_Viewer",
            category="Qualita",
            description="Visualizzatore 360°"
        )
    
    def generate_16px(self, builder: SVGBuilder) -> SVGBuilder:
        """16px: Cabinet with rotation arrow"""
        # Cabinet
        builder.add_rect(4, 4, 8, 10, fill=self.colors['very_light_gray'], 
                        stroke=self.colors['blue'], stroke_width=1.5)
        
        # Rotation arrow
        builder.add_path("M 12 4 Q 14 2 14 4 Q 14 6 12 8", stroke=self.colors['green'], 
                        stroke_width=1.5, fill='none')
        builder.add_polygon([(12, 8), (11, 6), (13, 7)], fill=self.colors['green'])
        
        return builder
    
    def generate_32px(self, builder: SVGBuilder) -> SVGBuilder:
        """32px: 3D cabinet with rotation"""
        # 3D cabinet
        # Front face
        builder.add_rect(8, 12, 12, 16, fill=self.colors['very_light_gray'], 
                        stroke=self.colors['blue'], stroke_width=2)
        # Side face
        builder.add_polygon([(20, 12), (24, 10), (24, 26), (20, 28)], 
                           fill=self.colors['light_gray'], stroke=self.colors['blue'], stroke_width=1)
        # Top face
        builder.add_polygon([(8, 12), (20, 12), (24, 10), (12, 10)], 
                           fill=self.colors['blue_light'], stroke=self.colors['blue'], stroke_width=1)
        
        # Circular rotation arrow
        builder.add_path("M 24 18 Q 28 14 28 18 Q 28 22 24 26", stroke=self.colors['green'], 
                        stroke_width=2, fill='none')
        builder.add_polygon([(24, 26), (23, 23), (26, 24)], fill=self.colors['green'])
        
        return builder
    
    def generate_64px(self, builder: SVGBuilder) -> SVGBuilder:
        """64px: Detailed 360° viewer"""
        # 3D cabinet
        # Front
        builder.add_rect(16, 24, 24, 32, fill=self.colors['very_light_gray'], 
                        stroke=self.colors['blue'], stroke_width=2)
        # Side
        builder.add_polygon([(40, 24), (48, 20), (48, 52), (40, 56)], 
                           fill=self.colors['light_gray'], stroke=self.colors['blue'], stroke_width=1.5)
        # Top
        builder.add_polygon([(16, 24), (40, 24), (48, 20), (24, 20)], 
                           fill=self.colors['blue_light'], stroke=self.colors['blue'], stroke_width=1.5)
        
        # Handle
        self.add_handle(builder, 36, 40, 64, 'circle')
        
        # 360° rotation arrows
        builder.add_path("M 48 36 Q 56 28 56 36 Q 56 44 48 52", stroke=self.colors['green'], 
                        stroke_width=3, fill='none')
        builder.add_polygon([(48, 52), (46, 48), (51, 50)], fill=self.colors['green'])
        
        # Angle indicator
        builder.add_circle(32, 8, 8, fill='none', stroke=self.colors['green'], 
                          stroke_width=2, stroke_dasharray="2,2")
        
        return builder
    
    def generate_128px(self, builder: SVGBuilder) -> SVGBuilder:
        """128px: Complete 360° viewer interface"""
        # Large 3D cabinet
        # Front face
        builder.add_rect(32, 48, 48, 64, fill=self.colors['very_light_gray'], 
                        stroke=self.colors['blue'], stroke_width=3)
        builder.add_rect(36, 52, 40, 56, fill='none', stroke=self.colors['blue_light'], stroke_width=1.5)
        
        # Side face
        builder.add_polygon([(80, 48), (96, 40), (96, 104), (80, 112)], 
                           fill=self.colors['light_gray'], stroke=self.colors['blue'], stroke_width=2)
        
        # Top face
        builder.add_polygon([(32, 48), (80, 48), (96, 40), (48, 40)], 
                           fill=self.colors['blue_light'], stroke=self.colors['blue'], stroke_width=2)
        
        # Handle with reflection
        self.add_handle(builder, 72, 80, 128, 'bar')
        
        # 360° rotation circle
        center_x, center_y = 104, 80
        builder.add_circle(center_x, center_y, 24, fill='none', 
                          stroke=self.colors['green'], stroke_width=3, opacity=0.7)
        
        # Rotation arrows at cardinal points
        arrow_positions = [
            (center_x, center_y - 24, 0),      # Top
            (center_x + 24, center_y, 90),     # Right
            (center_x, center_y + 24, 180),    # Bottom
            (center_x - 24, center_y, 270)     # Left
        ]
        
        for x, y, angle in arrow_positions:
            # Arrow head
            rad = math.radians(angle)
            p1_x = x + 4 * math.cos(math.radians(angle - 135))
            p1_y = y + 4 * math.sin(math.radians(angle - 135))
            p2_x = x + 4 * math.cos(math.radians(angle + 135))
            p2_y = y + 4 * math.sin(math.radians(angle + 135))
            
            builder.add_polygon([(x, y), (p1_x, p1_y), (p2_x, p2_y)], fill=self.colors['green'])
        
        # Angle measurement
        builder.add_path("M 104 56 Q 112 64 120 64", stroke=self.colors['orange'], 
                        stroke_width=2, fill='none')
        
        # Degree indicators
        for angle in range(0, 360, 45):
            rad = math.radians(angle)
            x = center_x + 30 * math.cos(rad)
            y = center_y + 30 * math.sin(rad)
            builder.add_circle(x, y, 2, fill=self.colors['green'], opacity=0.5)
        
        # Control panel
        builder.add_rect(16, 16, 48, 16, fill=self.colors['light_gray'], 
                        stroke=self.colors['medium_gray'], stroke_width=2, rx=4)
        
        # Play/rotate button
        builder.add_circle(28, 24, 6, fill=self.colors['green'], opacity=0.8)
        builder.add_polygon([(26, 22), (26, 26), (30, 24)], fill=self.colors['white'])
        
        return builder


class QualitaGenerator(IconGenerator):
    """Generator for Qualità Panel icons"""
    
    def __init__(self):
        super().__init__()
    
    def get_icons(self):
        """Return dict of icon names to methods"""
        return {
            'FAI_Verifica': self._generate_verifica,
            'FAI_Render': self._generate_render,
            'FAI_Viewer': self._generate_viewer,
        }
    
    def _generate_verifica(self, size):
        icon = FAI_Verifica()
        builder = self._create_svg(size)
        if size == 16:
            return icon.generate_16px(builder).get_svg()
        elif size == 32:
            return icon.generate_32px(builder).get_svg()
        elif size == 64:
            return icon.generate_64px(builder).get_svg()
        else:
            return icon.generate_128px(builder).get_svg()
    
    def _generate_render(self, size):
        icon = FAI_Render()
        builder = self._create_svg(size)
        if size == 16:
            return icon.generate_16px(builder).get_svg()
        elif size == 32:
            return icon.generate_32px(builder).get_svg()
        elif size == 64:
            return icon.generate_64px(builder).get_svg()
        else:
            return icon.generate_128px(builder).get_svg()
    
    def _generate_viewer(self, size):
        icon = FAI_Viewer()
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
    'FAI_Verifica',
    'FAI_Render',
    'FAI_Viewer',
    'QualitaGenerator'
]
