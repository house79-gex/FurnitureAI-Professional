"""
Design Panel Icon Generators
4 icons: FAI_LayoutIA, FAI_GeneraIA, FAI_Wizard, FAI_Template
"""

import sys
import os
import math

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.icon_base import IconBase, SimpleShapeIcon, IconGenerator
from core.svg_builder import SVGBuilder


class FAI_LayoutIA(SimpleShapeIcon):
    """Floor plan with AI brain for automatic layout"""
    
    def __init__(self):
        super().__init__(
            name="FAI_LayoutIA",
            category="Design",
            description="Floor plan con AI brain per layout automatico"
        )
    
    def generate_16px(self, builder: SVGBuilder) -> SVGBuilder:
        """16px: Simple grid + AI circle"""
        # Floor plan grid (simplified)
        builder.add_rect(
            2, 2, 12, 12,
            fill='none',
            stroke=self.colors['blue'],
            stroke_width=2
        )
        
        # AI brain indicator
        builder.add_circle(
            11, 5, 3,
            fill=self.colors['purple'],
            opacity=0.9
        )
        
        return builder
    
    def generate_32px(self, builder: SVGBuilder) -> SVGBuilder:
        """32px: Grid with divisions + AI brain"""
        # Main floor plan
        builder.add_rect(
            4, 4, 24, 24,
            fill='none',
            stroke=self.colors['blue'],
            stroke_width=2
        )
        
        # Division lines
        builder.add_line(16, 4, 16, 28, stroke=self.colors['blue_light'], stroke_width=1, stroke_dasharray="3,2")
        builder.add_line(4, 16, 28, 16, stroke=self.colors['blue_light'], stroke_width=1, stroke_dasharray="3,2")
        
        # AI brain with nodes
        self.add_ai_brain(builder, 24, 8, 5, 32)
        
        return builder
    
    def generate_64px(self, builder: SVGBuilder) -> SVGBuilder:
        """64px: Detailed grid + AI brain with connections"""
        # Main floor plan
        builder.add_rect(
            8, 8, 48, 48,
            fill=self.colors['very_light_gray'],
            stroke=self.colors['blue'],
            stroke_width=2
        )
        
        # Grid divisions
        for i in range(1, 3):
            x = 8 + i * 16
            y = 8 + i * 16
            builder.add_line(x, 8, x, 56, stroke=self.colors['blue_light'], stroke_width=1, stroke_dasharray="4,2")
            builder.add_line(8, y, 56, y, stroke=self.colors['blue_light'], stroke_width=1, stroke_dasharray="4,2")
        
        # AI brain
        brain_x, brain_y = 48, 16
        builder.add_circle(brain_x, brain_y, 8, fill=self.colors['purple'], opacity=0.9)
        
        # Neural network nodes
        for angle in [0, 120, 240]:
            node_x = brain_x + 4 * math.cos(math.radians(angle))
            node_y = brain_y + 4 * math.sin(math.radians(angle))
            builder.add_circle(node_x, node_y, 2, fill=self.colors['white'])
        
        return builder
    
    def generate_128px(self, builder: SVGBuilder) -> SVGBuilder:
        """128px: Detailed floor plan with complete neural network"""
        # Main floor plan with gradient
        builder.add_rect(
            16, 16, 96, 96,
            fill=self.colors['very_light_gray'],
            stroke=self.colors['blue'],
            stroke_width=3
        )
        
        # Detailed grid
        for i in range(1, 4):
            x = 16 + i * 24
            y = 16 + i * 24
            builder.add_line(x, 16, x, 112, stroke=self.colors['blue_light'], stroke_width=1.5, stroke_dasharray="6,3")
            builder.add_line(16, y, 112, y, stroke=self.colors['blue_light'], stroke_width=1.5, stroke_dasharray="6,3")
        
        # Room indicators (small rectangles in grid)
        rooms = [(24, 24, 20, 20), (52, 24, 20, 20), (24, 52, 20, 20)]
        for rx, ry, rw, rh in rooms:
            builder.add_rect(rx, ry, rw, rh, fill=self.colors['white'], stroke=self.colors['blue_dark'], stroke_width=1)
        
        # AI brain - larger and more detailed
        brain_x, brain_y = 96, 32
        builder.add_circle(brain_x, brain_y, 16, fill=self.colors['purple'], opacity=0.9)
        
        # Complex neural network
        for angle in [0, 60, 120, 180, 240, 300]:
            outer_x = brain_x + 10 * math.cos(math.radians(angle))
            outer_y = brain_y + 10 * math.sin(math.radians(angle))
            builder.add_circle(outer_x, outer_y, 3, fill=self.colors['white'])
            
            # Connections
            builder.add_line(brain_x, brain_y, outer_x, outer_y, 
                           stroke=self.colors['white'], stroke_width=1, opacity=0.5)
        
        # Center node
        builder.add_circle(brain_x, brain_y, 4, fill=self.colors['white'])
        
        return builder


class FAI_GeneraIA(SimpleShapeIcon):
    """Magic wand for generative AI"""
    
    def __init__(self):
        super().__init__(
            name="FAI_GeneraIA",
            category="Design",
            description="Magic wand generativa con AI"
        )
    
    def generate_16px(self, builder: SVGBuilder) -> SVGBuilder:
        """16px: Simple wand + star"""
        # Wand stick
        builder.add_line(3, 13, 9, 7, stroke=self.colors['medium_gray'], stroke_width=2)
        
        # Star at tip
        star_points = [
            (10, 3), (11, 6), (14, 6), (12, 8), (13, 11), (10, 9), (7, 11), (8, 8), (6, 6), (9, 6)
        ]
        builder.add_polygon(star_points, fill=self.colors['yellow'], stroke=self.colors['orange'], stroke_width=1)
        
        return builder
    
    def generate_32px(self, builder: SVGBuilder) -> SVGBuilder:
        """32px: Wand + star + sparkles"""
        # Wand stick with grip
        builder.add_line(6, 26, 18, 14, stroke=self.colors['dark_gray'], stroke_width=3)
        builder.add_circle(6, 26, 3, fill=self.colors['medium_gray'])
        
        # Main star
        star_points = [
            (20, 6), (22, 12), (28, 12), (24, 16), (26, 22), (20, 18), (14, 22), (16, 16), (12, 12), (18, 12)
        ]
        builder.add_polygon(star_points, fill=self.colors['yellow'], stroke=self.colors['orange'], stroke_width=1.5)
        
        # Sparkles
        for sx, sy in [(8, 10), (26, 8), (24, 24)]:
            builder.add_line(sx-2, sy, sx+2, sy, stroke=self.colors['yellow'], stroke_width=1.5)
            builder.add_line(sx, sy-2, sx, sy+2, stroke=self.colors['yellow'], stroke_width=1.5)
        
        return builder
    
    def generate_64px(self, builder: SVGBuilder) -> SVGBuilder:
        """64px: Detailed wand with multiple sparkles"""
        # Wand stick with gradient effect
        builder.add_line(12, 52, 36, 28, stroke=self.colors['dark_gray'], stroke_width=4)
        
        # Grip
        for i in range(3):
            builder.add_circle(12 + i*2, 52 - i*2, 4, fill=self.colors['medium_gray'])
        
        # Large star
        star_points = [
            (40, 12), (44, 24), (56, 24), (48, 32), (52, 44), (40, 36), (28, 44), (32, 32), (24, 24), (36, 24)
        ]
        builder.add_polygon(star_points, fill=self.colors['yellow'], stroke=self.colors['orange'], stroke_width=2)
        
        # Inner star glow
        inner_star = [(x * 0.6 + 40 * 0.4, y * 0.6 + 28 * 0.4) for x, y in star_points]
        builder.add_polygon(inner_star, fill=self.colors['white'], opacity=0.7)
        
        # Multiple sparkles
        sparkle_positions = [(16, 20), (52, 16), (48, 48), (20, 40)]
        for sx, sy in sparkle_positions:
            builder.add_line(sx-3, sy, sx+3, sy, stroke=self.colors['yellow'], stroke_width=2)
            builder.add_line(sx, sy-3, sx, sy+3, stroke=self.colors['yellow'], stroke_width=2)
        
        return builder
    
    def generate_128px(self, builder: SVGBuilder) -> SVGBuilder:
        """128px: Complete wand with emerging furniture"""
        # Detailed wand
        builder.add_line(24, 104, 72, 56, stroke=self.colors['dark_gray'], stroke_width=6)
        
        # Detailed grip with texture
        for i in range(6):
            builder.add_circle(24 + i*3, 104 - i*3, 5, 
                             fill=self.colors['medium_gray'] if i % 2 == 0 else self.colors['light_gray'])
        
        # Large glowing star
        star_points = [
            (80, 24), (88, 48), (112, 48), (96, 64), (104, 88), (80, 72), (56, 88), (64, 64), (48, 48), (72, 48)
        ]
        builder.add_polygon(star_points, fill=self.colors['yellow'], stroke=self.colors['orange'], stroke_width=3)
        
        # Multiple glow layers
        for scale in [0.7, 0.5, 0.3]:
            inner_star = [(x * scale + 80 * (1-scale), y * scale + 56 * (1-scale)) for x, y in star_points]
            builder.add_polygon(inner_star, fill=self.colors['white'], opacity=0.4)
        
        # Magic particles
        for angle in range(0, 360, 30):
            dist = 40 + (angle % 60) * 0.5
            px = 80 + dist * math.cos(math.radians(angle))
            py = 56 + dist * math.sin(math.radians(angle))
            builder.add_circle(px, py, 2, fill=self.colors['yellow'], opacity=0.7)
        
        # Emerging cabinet silhouette
        builder.add_rect(20, 60, 24, 32, fill=self.colors['blue_light'], opacity=0.3)
        builder.add_circle(32, 76, 2, fill=self.colors['blue'], opacity=0.5)
        
        return builder


class FAI_Wizard(SimpleShapeIcon):
    """Step-by-step wizard icon"""
    
    def __init__(self):
        super().__init__(
            name="FAI_Wizard",
            category="Design",
            description="Wizard passo-passo per creazione mobili"
        )
    
    def generate_16px(self, builder: SVGBuilder) -> SVGBuilder:
        """16px: Three numbered circles"""
        for i in range(3):
            x = 4 + i * 4
            builder.add_circle(x, 8, 2, fill=self.colors['blue'], opacity=0.8)
        
        return builder
    
    def generate_32px(self, builder: SVGBuilder) -> SVGBuilder:
        """32px: Steps with simple furniture"""
        # Cabinet shape
        builder.add_rect(4, 16, 10, 12, fill=self.colors['very_light_gray'], 
                        stroke=self.colors['blue'], stroke_width=1.5)
        
        # Step circles
        for i in range(3):
            x = 20 + i * 6
            builder.add_circle(x, 8, 3, fill=self.colors['blue'], 
                             stroke=self.colors['white'], stroke_width=1)
            
            # Connection line
            if i < 2:
                builder.add_line(x+3, 8, x+3, 8, stroke=self.colors['blue_light'], stroke_width=1.5)
        
        # Arrow
        builder.add_line(14, 22, 20, 22, stroke=self.colors['green'], stroke_width=2)
        
        return builder
    
    def generate_64px(self, builder: SVGBuilder) -> SVGBuilder:
        """64px: Cabinet + detailed steps"""
        # Cabinet
        builder.add_rect(8, 32, 20, 24, fill=self.colors['very_light_gray'],
                        stroke=self.colors['blue'], stroke_width=2)
        builder.add_line(8, 44, 28, 44, stroke=self.colors['blue'], stroke_width=1)
        self.add_handle(builder, 18, 50, 64, 'circle')
        
        # Step circles with numbers
        for i in range(3):
            x = 36 + i * 12
            y = 16
            
            # Circle
            builder.add_circle(x, y, 5, fill=self.colors['blue'],
                             stroke=self.colors['white'], stroke_width=2)
            
            # Connection line
            if i < 2:
                builder.add_line(x+5, y, x+7, y, stroke=self.colors['blue_light'], stroke_width=2)
        
        # Timeline arrow
        builder.add_line(32, 28, 56, 28, stroke=self.colors['green'], stroke_width=2)
        builder.add_polygon([(56, 28), (52, 26), (52, 30)], fill=self.colors['green'])
        
        return builder
    
    def generate_128px(self, builder: SVGBuilder) -> SVGBuilder:
        """128px: Detailed cabinet + timeline with icons"""
        # Detailed cabinet
        builder.add_rect(16, 64, 40, 48, fill=self.colors['very_light_gray'],
                        stroke=self.colors['blue'], stroke_width=3)
        
        # Cabinet details
        builder.add_line(16, 88, 56, 88, stroke=self.colors['blue'], stroke_width=2)
        builder.add_rect(20, 68, 32, 16, fill='none', stroke=self.colors['blue_light'], stroke_width=1.5)
        self.add_handle(builder, 36, 100, 128, 'bar')
        
        # Step circles with detailed icons
        steps = [
            (72, 32, "layout"),   # Layout step
            (96, 32, "edit"),     # Edit step
            (120, 32, "check")    # Verify step
        ]
        
        for i, (x, y, step_type) in enumerate(steps):
            # Circle background
            builder.add_circle(x, y, 10, fill=self.colors['blue'],
                             stroke=self.colors['white'], stroke_width=3)
            
            # Step icon (simplified)
            if step_type == "layout":
                builder.add_rect(x-4, y-4, 8, 8, fill='none', 
                               stroke=self.colors['white'], stroke_width=2)
            elif step_type == "edit":
                builder.add_line(x-4, y, x+4, y, stroke=self.colors['white'], stroke_width=2)
                builder.add_line(x, y-4, x, y+4, stroke=self.colors['white'], stroke_width=2)
            elif step_type == "check":
                builder.add_path(f"M {x-4} {y} L {x-1} {y+4} L {x+4} {y-4}",
                               stroke=self.colors['white'], stroke_width=2, fill='none')
            
            # Connection line
            if i < len(steps) - 1:
                builder.add_line(x+10, y, x+14, y, stroke=self.colors['blue_light'], stroke_width=3)
        
        # Timeline arrow below
        builder.add_line(64, 56, 112, 56, stroke=self.colors['green'], stroke_width=3)
        builder.add_polygon([(112, 56), (106, 53), (106, 59)], fill=self.colors['green'])
        
        return builder


class FAI_Template(SimpleShapeIcon):
    """Template folder icon"""
    
    def __init__(self):
        super().__init__(
            name="FAI_Template",
            category="Design",
            description="Cartella con template predefiniti"
        )
    
    def generate_16px(self, builder: SVGBuilder) -> SVGBuilder:
        """16px: Simple folder"""
        # Folder tab
        builder.add_rect(2, 2, 6, 3, fill=self.colors['orange'], stroke=self.colors['orange_light'], stroke_width=1)
        
        # Folder body
        builder.add_rect(2, 5, 12, 9, fill=self.colors['orange'], stroke=self.colors['orange_light'], stroke_width=1)
        
        return builder
    
    def generate_32px(self, builder: SVGBuilder) -> SVGBuilder:
        """32px: Folder with visible documents"""
        # Folder tab
        builder.add_rect(4, 4, 12, 6, fill=self.colors['orange'], rx=1)
        
        # Folder body
        builder.add_rect(4, 10, 24, 18, fill=self.colors['orange'], stroke=self.colors['orange_light'], stroke_width=2, rx=2)
        
        # Documents inside (simplified)
        builder.add_rect(8, 14, 16, 10, fill=self.colors['white'], opacity=0.8)
        builder.add_line(10, 17, 20, 17, stroke=self.colors['blue'], stroke_width=1)
        builder.add_line(10, 20, 18, 20, stroke=self.colors['blue'], stroke_width=1)
        
        return builder
    
    def generate_64px(self, builder: SVGBuilder) -> SVGBuilder:
        """64px: Open folder with multiple documents"""
        # Folder tab
        builder.add_rect(8, 8, 24, 12, fill=self.colors['orange'], rx=2)
        
        # Folder body (open)
        builder.add_rect(8, 20, 48, 36, fill=self.colors['orange'],
                        stroke=self.colors['orange_light'], stroke_width=2, rx=3)
        
        # Multiple documents
        docs = [(14, 26, 18, 24), (24, 26, 18, 24), (34, 26, 18, 24)]
        for dx, dy, dw, dh in docs:
            builder.add_rect(dx, dy, dw, dh, fill=self.colors['white'], 
                           stroke=self.colors['light_gray'], stroke_width=1)
            
            # Blueprint lines
            for i in range(3):
                builder.add_line(dx+2, dy+4+i*6, dx+dw-2, dy+4+i*6,
                               stroke=self.colors['blue_light'], stroke_width=1)
        
        return builder
    
    def generate_128px(self, builder: SVGBuilder) -> SVGBuilder:
        """128px: Detailed folder with blueprint documents"""
        # Folder tab with shadow
        builder.add_rect(18, 18, 46, 24, fill=self.colors['orange'], rx=4)
        
        # Folder body
        builder.add_rect(16, 42, 96, 70, fill=self.colors['orange'],
                        stroke=self.colors['orange_light'], stroke_width=3, rx=5)
        
        # Shadow inside
        builder.add_rect(18, 44, 92, 4, fill=self.colors['dark_gray'], opacity=0.2)
        
        # Detailed documents with blueprints
        docs = [
            (24, 52, 26, 52),
            (54, 52, 26, 52),
            (84, 52, 26, 52)
        ]
        
        for dx, dy, dw, dh in docs:
            # Document background
            builder.add_rect(dx, dy, dw, dh, fill=self.colors['white'],
                           stroke=self.colors['light_gray'], stroke_width=1.5)
            
            # Blueprint grid
            for i in range(1, 4):
                y_pos = dy + i * dh / 4
                builder.add_line(dx+2, y_pos, dx+dw-2, y_pos,
                               stroke=self.colors['blue_light'], stroke_width=0.5,
                               stroke_dasharray="2,2")
            
            # Cabinet sketch
            builder.add_rect(dx+4, dy+8, dw-8, dh-16, fill='none',
                           stroke=self.colors['blue'], stroke_width=1.5)
            builder.add_line(dx+dw//2, dy+8, dx+dw//2, dy+dh-8,
                           stroke=self.colors['blue'], stroke_width=1)
            
            # Title bar
            builder.add_rect(dx, dy, dw, 6, fill=self.colors['blue_light'], opacity=0.3)
        
        return builder


class DesignGenerator(IconGenerator):
    """Generator for Design Panel icons"""
    
    def __init__(self):
        super().__init__()
    
    def get_icons(self):
        """Return dict of icon names to methods"""
        return {
            'FAI_LayoutIA': self._generate_layout_ia,
            'FAI_GeneraIA': self._generate_genera_ia,
            'FAI_Wizard': self._generate_wizard,
            'FAI_Template': self._generate_template,
        }
    
    def _generate_layout_ia(self, generator, size):
        """Generate FAI_LayoutIA icon"""
        icon = FAI_LayoutIA()
        builder = self._create_svg(size)
        
        if size == 16:
            return icon.generate_16px(builder).to_string()
        elif size == 32:
            return icon.generate_32px(builder).to_string()
        elif size == 64:
            return icon.generate_64px(builder).to_string()
        else:  # 128
            return icon.generate_128px(builder).to_string()
    
    def _generate_genera_ia(self, generator, size):
        """Generate FAI_GeneraIA icon"""
        icon = FAI_GeneraIA()
        builder = self._create_svg(size)
        
        if size == 16:
            return icon.generate_16px(builder).to_string()
        elif size == 32:
            return icon.generate_32px(builder).to_string()
        elif size == 64:
            return icon.generate_64px(builder).to_string()
        else:  # 128
            return icon.generate_128px(builder).to_string()
    
    def _generate_wizard(self, generator, size):
        """Generate FAI_Wizard icon"""
        icon = FAI_Wizard()
        builder = self._create_svg(size)
        
        if size == 16:
            return icon.generate_16px(builder).to_string()
        elif size == 32:
            return icon.generate_32px(builder).to_string()
        elif size == 64:
            return icon.generate_64px(builder).to_string()
        else:  # 128
            return icon.generate_128px(builder).to_string()
    
    def _generate_template(self, generator, size):
        """Generate FAI_Template icon"""
        icon = FAI_Template()
        builder = self._create_svg(size)
        
        if size == 16:
            return icon.generate_16px(builder).to_string()
        elif size == 32:
            return icon.generate_32px(builder).to_string()
        elif size == 64:
            return icon.generate_64px(builder).to_string()
        else:  # 128
            return icon.generate_128px(builder).to_string()


# Export all classes
__all__ = [
    'FAI_LayoutIA',
    'FAI_GeneraIA',
    'FAI_Wizard',
    'FAI_Template',
    'DesignGenerator'
]
