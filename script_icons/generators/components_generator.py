"""
Components Panel Icon Generators
8 icons: FAI_Designer, FAI_Anta, FAI_Cassetto, FAI_Ripiano, 
         FAI_Schienale, FAI_Cornice, FAI_Cappello, FAI_Zoccolo
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.icon_base import IconBase, SimpleShapeIcon, IconGenerator
from core.svg_builder import SVGBuilder


class FAI_Designer(SimpleShapeIcon):
    """Design tool icon"""
    
    def __init__(self):
        super().__init__(
            name="FAI_Designer",
            category="Componenti",
            description="Strumento di design componenti"
        )
    
    def generate_16px(self, builder: SVGBuilder) -> SVGBuilder:
        # Pencil/ruler combo
        builder.add_line(3, 13, 13, 3, stroke=self.colors['blue'], stroke_width=2)
        builder.add_circle(3, 13, 2, fill=self.colors['orange'])
        return builder
    
    def generate_32px(self, builder: SVGBuilder) -> SVGBuilder:
        # Pencil
        builder.add_line(6, 26, 20, 12, stroke=self.colors['blue'], stroke_width=3)
        builder.add_polygon([(20, 12), (24, 8), (26, 10), (22, 14)], fill=self.colors['dark_gray'])
        builder.add_circle(6, 26, 3, fill=self.colors['orange'])
        
        # Ruler marks
        for i in range(4):
            x = 10 + i * 3
            y = 22 - i * 3
            builder.add_line(x, y, x+1, y+1, stroke=self.colors['white'], stroke_width=1)
        return builder
    
    def generate_64px(self, builder: SVGBuilder) -> SVGBuilder:
        # Detailed pencil
        builder.add_rect(12, 40, 40, 6, fill=self.colors['blue'], rx=1)
        builder.add_polygon([(52, 40), (58, 43), (52, 46)], fill=self.colors['dark_gray'])
        builder.add_circle(12, 43, 4, fill=self.colors['orange'])
        
        # Ruler below
        builder.add_rect(12, 52, 40, 6, fill=self.colors['yellow'], stroke=self.colors['orange'], stroke_width=1)
        for i in range(8):
            x = 14 + i * 5
            h = 3 if i % 2 == 0 else 2
            builder.add_line(x, 52, x, 52+h, stroke=self.colors['dark_gray'], stroke_width=1)
        return builder
    
    def generate_128px(self, builder: SVGBuilder) -> SVGBuilder:
        # Large pencil with details
        builder.add_rect(24, 80, 80, 12, fill=self.colors['blue'], rx=2)
        builder.add_rect(28, 82, 72, 8, fill=self.colors['blue_light'], rx=1)
        builder.add_polygon([(104, 80), (116, 86), (104, 92)], fill=self.colors['dark_gray'])
        builder.add_polygon([(116, 86), (120, 86), (118, 88)], fill=self.colors['black'])
        builder.add_circle(24, 86, 6, fill=self.colors['orange'], stroke=self.colors['red'], stroke_width=2)
        
        # Detailed ruler
        builder.add_rect(24, 104, 80, 12, fill=self.colors['yellow'], 
                        stroke=self.colors['orange'], stroke_width=2, rx=2)
        for i in range(16):
            x = 26 + i * 5
            h = 6 if i % 4 == 0 else (4 if i % 2 == 0 else 2)
            builder.add_line(x, 104, x, 104+h, stroke=self.colors['dark_gray'], stroke_width=1)
        return builder


class FAI_Anta(SimpleShapeIcon):
    """Cabinet door icon"""
    
    def __init__(self):
        super().__init__(
            name="FAI_Anta",
            category="Componenti",
            description="Anta mobile"
        )
    
    def generate_16px(self, builder: SVGBuilder) -> SVGBuilder:
        builder.add_rect(3, 2, 10, 12, fill=self.colors['very_light_gray'],
                        stroke=self.colors['blue'], stroke_width=2)
        builder.add_circle(11, 8, 2, fill=self.colors['medium_gray'])
        return builder
    
    def generate_32px(self, builder: SVGBuilder) -> SVGBuilder:
        builder.add_rect(6, 4, 20, 24, fill=self.colors['very_light_gray'],
                        stroke=self.colors['blue'], stroke_width=2)
        builder.add_rect(9, 7, 14, 18, fill='none', stroke=self.colors['blue_light'], stroke_width=1)
        self.add_handle(builder, 22, 16, 32, 'circle')
        return builder
    
    def generate_64px(self, builder: SVGBuilder) -> SVGBuilder:
        builder.add_rect(12, 8, 40, 48, fill=self.colors['very_light_gray'],
                        stroke=self.colors['blue'], stroke_width=2)
        builder.add_rect(16, 12, 32, 40, fill='none', stroke=self.colors['blue_light'], stroke_width=1.5)
        builder.add_rect(20, 16, 24, 32, fill='none', stroke=self.colors['blue_light'], stroke_width=1)
        self.add_handle(builder, 44, 32, 64, 'bar')
        return builder
    
    def generate_128px(self, builder: SVGBuilder) -> SVGBuilder:
        # Door with wood grain texture
        builder.add_rect(24, 16, 80, 96, fill=self.colors['very_light_gray'],
                        stroke=self.colors['blue'], stroke_width=3)
        
        # Frame details
        builder.add_rect(28, 20, 72, 88, fill='none', stroke=self.colors['blue_light'], stroke_width=2)
        builder.add_rect(32, 24, 64, 80, fill='none', stroke=self.colors['blue_light'], stroke_width=1.5)
        
        # Wood grain lines
        for i in range(8):
            y = 28 + i * 10
            builder.add_path(
                f"M 36 {y} Q 68 {y+2} 96 {y}",
                stroke=self.colors['light_gray'], stroke_width=0.5, fill='none'
            )
        
        # Handle
        self.add_handle(builder, 88, 64, 128, 'bar')
        
        # Hinges
        for hy in [32, 64, 96]:
            builder.add_rect(24, hy-4, 4, 8, fill=self.colors['medium_gray'])
        
        return builder


class FAI_Cassetto(SimpleShapeIcon):
    """Drawer icon"""
    
    def __init__(self):
        super().__init__(
            name="FAI_Cassetto",
            category="Componenti",
            description="Cassetto"
        )
    
    def generate_16px(self, builder: SVGBuilder) -> SVGBuilder:
        builder.add_rect(2, 4, 12, 8, fill=self.colors['very_light_gray'],
                        stroke=self.colors['green'], stroke_width=2)
        builder.add_rect(5, 6, 6, 2, fill=self.colors['medium_gray'], rx=1)
        return builder
    
    def generate_32px(self, builder: SVGBuilder) -> SVGBuilder:
        # Drawer front
        builder.add_rect(4, 8, 24, 16, fill=self.colors['very_light_gray'],
                        stroke=self.colors['green'], stroke_width=2)
        
        # Handle
        builder.add_rect(12, 14, 8, 4, fill=self.colors['medium_gray'], rx=2)
        
        # Depth lines
        builder.add_line(4, 8, 2, 6, stroke=self.colors['green_dark'], stroke_width=1)
        builder.add_line(28, 8, 30, 6, stroke=self.colors['green_dark'], stroke_width=1)
        
        return builder
    
    def generate_64px(self, builder: SVGBuilder) -> SVGBuilder:
        # Drawer with 3D effect
        builder.add_rect(8, 16, 48, 32, fill=self.colors['very_light_gray'],
                        stroke=self.colors['green'], stroke_width=2)
        
        # 3D sides
        builder.add_polygon([(8, 16), (4, 12), (4, 44), (8, 48)], fill=self.colors['light_gray'])
        builder.add_polygon([(56, 16), (60, 12), (60, 44), (56, 48)], fill=self.colors['light_gray'])
        
        # Handle
        builder.add_rect(24, 28, 16, 6, fill=self.colors['medium_gray'], rx=3)
        
        return builder
    
    def generate_128px(self, builder: SVGBuilder) -> SVGBuilder:
        # Detailed drawer with dovetail joints
        builder.add_rect(16, 32, 96, 64, fill=self.colors['very_light_gray'],
                        stroke=self.colors['green'], stroke_width=3)
        
        # 3D perspective
        builder.add_polygon([(16, 32), (8, 24), (8, 88), (16, 96)], fill=self.colors['light_gray'])
        builder.add_polygon([(112, 32), (120, 24), (120, 88), (112, 96)], fill=self.colors['light_gray'])
        
        # Dovetail joints on sides
        for y in [36, 52, 68, 84]:
            builder.add_polygon([(16, y), (14, y+4), (16, y+8)], fill=self.colors['medium_gray'])
            builder.add_polygon([(112, y), (114, y+4), (112, y+8)], fill=self.colors['medium_gray'])
        
        # Large handle
        builder.add_rect(48, 56, 32, 12, fill=self.colors['medium_gray'], rx=6)
        builder.add_rect(50, 58, 28, 8, fill=self.colors['light_gray'], rx=4)
        
        return builder


class FAI_Ripiano(SimpleShapeIcon):
    """Shelf icon"""
    
    def __init__(self):
        super().__init__(
            name="FAI_Ripiano",
            category="Componenti",
            description="Ripiano"
        )
    
    def generate_16px(self, builder: SVGBuilder) -> SVGBuilder:
        # Simple shelf
        builder.add_rect(2, 7, 12, 2, fill=self.colors['very_light_gray'],
                        stroke=self.colors['orange'], stroke_width=1)
        # Support lines
        builder.add_line(3, 9, 3, 13, stroke=self.colors['orange'], stroke_width=1)
        builder.add_line(13, 9, 13, 13, stroke=self.colors['orange'], stroke_width=1)
        return builder
    
    def generate_32px(self, builder: SVGBuilder) -> SVGBuilder:
        # Shelf with supports
        builder.add_rect(4, 14, 24, 4, fill=self.colors['very_light_gray'],
                        stroke=self.colors['orange'], stroke_width=2)
        
        # Support pins
        for x in [6, 26]:
            builder.add_line(x, 18, x, 26, stroke=self.colors['orange'], stroke_width=2)
            builder.add_circle(x, 26, 2, fill=self.colors['orange_light'])
        
        return builder
    
    def generate_64px(self, builder: SVGBuilder) -> SVGBuilder:
        # Shelf with multiple supports
        builder.add_rect(8, 28, 48, 8, fill=self.colors['very_light_gray'],
                        stroke=self.colors['orange'], stroke_width=2)
        
        # 3D edge
        builder.add_polygon([(8, 28), (4, 24), (52, 24), (56, 28)], fill=self.colors['light_gray'])
        
        # Support pins (32mm system)
        for x in [12, 28, 44, 52]:
            builder.add_line(x, 36, x, 52, stroke=self.colors['orange'], stroke_width=2)
            builder.add_circle(x, 52, 3, fill=self.colors['orange_light'])
        
        return builder
    
    def generate_128px(self, builder: SVGBuilder) -> SVGBuilder:
        # Detailed shelf with grain
        builder.add_rect(16, 56, 96, 16, fill=self.colors['very_light_gray'],
                        stroke=self.colors['orange'], stroke_width=3)
        
        # 3D edge
        builder.add_polygon([(16, 56), (8, 48), (104, 48), (112, 56)], fill=self.colors['light_gray'])
        
        # Wood grain
        for i in range(10):
            y = 58 + i
            builder.add_path(
                f"M 20 {y} Q 64 {y+1} 108 {y}",
                stroke=self.colors['light_gray'], stroke_width=0.5, fill='none'
            )
        
        # Support pins
        for x in [24, 48, 72, 96, 104]:
            builder.add_rect(x-2, 72, 4, 32, fill=self.colors['orange'], rx=2)
            builder.add_circle(x, 104, 4, fill=self.colors['orange_light'],
                             stroke=self.colors['orange'], stroke_width=1)
        
        return builder


class FAI_Schienale(SimpleShapeIcon):
    """Back panel icon"""
    
    def __init__(self):
        super().__init__(
            name="FAI_Schienale",
            category="Componenti",
            description="Schienale mobile"
        )
    
    def generate_16px(self, builder: SVGBuilder) -> SVGBuilder:
        builder.add_rect(4, 2, 8, 12, fill=self.colors['light_gray'],
                        stroke=self.colors['medium_gray'], stroke_width=1, opacity=0.7)
        return builder
    
    def generate_32px(self, builder: SVGBuilder) -> SVGBuilder:
        # Back panel with groove indication
        builder.add_rect(8, 4, 16, 24, fill=self.colors['light_gray'],
                        stroke=self.colors['medium_gray'], stroke_width=2, opacity=0.8)
        
        # Groove lines
        builder.add_line(8, 6, 8, 26, stroke=self.colors['dark_gray'], stroke_width=1)
        builder.add_line(24, 6, 24, 26, stroke=self.colors['dark_gray'], stroke_width=1)
        
        return builder
    
    def generate_64px(self, builder: SVGBuilder) -> SVGBuilder:
        # Back panel with pattern
        builder.add_rect(16, 8, 32, 48, fill=self.colors['light_gray'],
                        stroke=self.colors['medium_gray'], stroke_width=2)
        
        # MDF pattern (small holes)
        for y in range(4):
            for x in range(3):
                builder.add_circle(20 + x*10, 16 + y*10, 1, fill=self.colors['dark_gray'], opacity=0.3)
        
        # Grooves
        builder.add_rect(16, 8, 2, 48, fill=self.colors['dark_gray'], opacity=0.5)
        builder.add_rect(46, 8, 2, 48, fill=self.colors['dark_gray'], opacity=0.5)
        
        return builder
    
    def generate_128px(self, builder: SVGBuilder) -> SVGBuilder:
        # Detailed back panel
        builder.add_rect(32, 16, 64, 96, fill=self.colors['light_gray'],
                        stroke=self.colors['medium_gray'], stroke_width=3)
        
        # MDF texture pattern
        for y in range(12):
            for x in range(8):
                builder.add_circle(36 + x*8, 20 + y*8, 1.5, 
                                 fill=self.colors['dark_gray'], opacity=0.2)
        
        # Groove details
        builder.add_rect(32, 16, 4, 96, fill=self.colors['dark_gray'], opacity=0.4)
        builder.add_rect(92, 16, 4, 96, fill=self.colors['dark_gray'], opacity=0.4)
        
        # Edge banding
        builder.add_rect(32, 16, 64, 3, fill=self.colors['medium_gray'])
        builder.add_rect(32, 109, 64, 3, fill=self.colors['medium_gray'])
        
        return builder


class FAI_Cornice(SimpleShapeIcon):
    """Crown molding icon"""
    
    def __init__(self):
        super().__init__(
            name="FAI_Cornice",
            category="Componenti",
            description="Cornice decorativa"
        )
    
    def generate_16px(self, builder: SVGBuilder) -> SVGBuilder:
        builder.add_path("M 2 10 L 8 4 L 14 10", stroke=self.colors['blue'], 
                        stroke_width=2, fill='none')
        return builder
    
    def generate_32px(self, builder: SVGBuilder) -> SVGBuilder:
        builder.add_path("M 4 20 L 8 16 L 16 8 L 24 16 L 28 20", 
                        stroke=self.colors['blue'], stroke_width=2, fill=self.colors['very_light_gray'])
        return builder
    
    def generate_64px(self, builder: SVGBuilder) -> SVGBuilder:
        # Decorative molding profile
        builder.add_path(
            "M 8 40 L 12 36 L 20 28 L 32 16 L 44 28 L 52 36 L 56 40",
            stroke=self.colors['blue'], stroke_width=2, fill=self.colors['very_light_gray']
        )
        
        # Detail lines
        builder.add_path("M 12 36 L 16 32 L 32 16 L 48 32 L 52 36",
                        stroke=self.colors['blue_light'], stroke_width=1, fill='none')
        
        return builder
    
    def generate_128px(self, builder: SVGBuilder) -> SVGBuilder:
        # Detailed crown molding with ornate profile
        builder.add_path(
            "M 16 80 L 24 72 L 40 56 L 64 32 L 88 56 L 104 72 L 112 80",
            stroke=self.colors['blue'], stroke_width=3, fill=self.colors['very_light_gray']
        )
        
        # Multiple profile layers
        builder.add_path("M 24 72 L 32 64 L 64 32 L 96 64 L 104 72",
                        stroke=self.colors['blue_light'], stroke_width=2, fill='none')
        
        builder.add_path("M 28 68 L 36 60 L 64 32 L 92 60 L 100 68",
                        stroke=self.colors['blue_light'], stroke_width=1, fill='none', opacity=0.7)
        
        # Decorative elements
        for x in [32, 64, 96]:
            builder.add_circle(x, 64, 3, fill=self.colors['blue_dark'])
        
        return builder


class FAI_Cappello(SimpleShapeIcon):
    """Top crown icon"""
    
    def __init__(self):
        super().__init__(
            name="FAI_Cappello",
            category="Componenti",
            description="Cappello superiore"
        )
    
    def generate_16px(self, builder: SVGBuilder) -> SVGBuilder:
        builder.add_rect(2, 6, 12, 3, fill=self.colors['blue'])
        builder.add_rect(3, 9, 10, 5, fill=self.colors['very_light_gray'], 
                        stroke=self.colors['blue'], stroke_width=1)
        return builder
    
    def generate_32px(self, builder: SVGBuilder) -> SVGBuilder:
        # Top cap
        builder.add_rect(4, 12, 24, 6, fill=self.colors['blue'], rx=1)
        
        # Body
        builder.add_rect(6, 18, 20, 10, fill=self.colors['very_light_gray'],
                        stroke=self.colors['blue'], stroke_width=2)
        
        return builder
    
    def generate_64px(self, builder: SVGBuilder) -> SVGBuilder:
        # Top crown
        builder.add_rect(8, 24, 48, 12, fill=self.colors['blue'], rx=2)
        
        # Profile detail
        builder.add_path("M 8 36 L 12 32 L 52 32 L 56 36", 
                        fill=self.colors['blue_light'])
        
        # Body
        builder.add_rect(12, 36, 40, 20, fill=self.colors['very_light_gray'],
                        stroke=self.colors['blue'], stroke_width=2)
        
        return builder
    
    def generate_128px(self, builder: SVGBuilder) -> SVGBuilder:
        # Detailed top crown
        builder.add_rect(16, 48, 96, 24, fill=self.colors['blue'], rx=4)
        
        # Ornate profile
        builder.add_path("M 16 72 L 24 64 L 104 64 L 112 72",
                        fill=self.colors['blue_light'])
        
        # Decorative line
        for x in range(8):
            builder.add_rect(20 + x*12, 52, 8, 4, fill=self.colors['blue_dark'], rx=1)
        
        # Cabinet body
        builder.add_rect(24, 72, 80, 40, fill=self.colors['very_light_gray'],
                        stroke=self.colors['blue'], stroke_width=3)
        
        return builder


class FAI_Zoccolo(SimpleShapeIcon):
    """Base plinth icon"""
    
    def __init__(self):
        super().__init__(
            name="FAI_Zoccolo",
            category="Componenti",
            description="Zoccolo base"
        )
    
    def generate_16px(self, builder: SVGBuilder) -> SVGBuilder:
        builder.add_rect(3, 2, 10, 10, fill=self.colors['very_light_gray'],
                        stroke=self.colors['dark_gray'], stroke_width=1)
        builder.add_rect(2, 12, 12, 2, fill=self.colors['dark_gray'])
        return builder
    
    def generate_32px(self, builder: SVGBuilder) -> SVGBuilder:
        # Cabinet body
        builder.add_rect(6, 4, 20, 18, fill=self.colors['very_light_gray'],
                        stroke=self.colors['blue'], stroke_width=2)
        
        # Plinth base
        builder.add_rect(4, 22, 24, 6, fill=self.colors['dark_gray'])
        builder.add_rect(6, 24, 20, 2, fill=self.colors['medium_gray'])
        
        return builder
    
    def generate_64px(self, builder: SVGBuilder) -> SVGBuilder:
        # Cabinet
        builder.add_rect(12, 8, 40, 36, fill=self.colors['very_light_gray'],
                        stroke=self.colors['blue'], stroke_width=2)
        
        # Base plinth with profile
        builder.add_path("M 8 44 L 12 40 L 52 40 L 56 44 L 56 52 L 8 52 Z",
                        fill=self.colors['dark_gray'])
        
        # Detail
        builder.add_rect(12, 44, 40, 3, fill=self.colors['medium_gray'])
        
        return builder
    
    def generate_128px(self, builder: SVGBuilder) -> SVGBuilder:
        # Cabinet body
        builder.add_rect(24, 16, 80, 72, fill=self.colors['very_light_gray'],
                        stroke=self.colors['blue'], stroke_width=3)
        
        # Detailed plinth base
        builder.add_path("M 16 88 L 24 80 L 104 80 L 112 88 L 112 104 L 16 104 Z",
                        fill=self.colors['dark_gray'])
        
        # Profile layers
        builder.add_rect(24, 88, 80, 4, fill=self.colors['medium_gray'])
        builder.add_rect(20, 92, 88, 4, fill=self.colors['light_gray'], opacity=0.5)
        
        # Adjustable feet
        for x in [32, 64, 96]:
            builder.add_circle(x, 108, 4, fill=self.colors['black'])
            builder.add_circle(x, 108, 2, fill=self.colors['medium_gray'])
        
        return builder


class ComponentsGenerator(IconGenerator):
    """Generator for Components Panel icons"""
    
    def __init__(self):
        super().__init__()
    
    def get_icons(self):
        """Return dict of icon names to methods"""
        return {
            'FAI_Designer': self._generate_designer,
            'FAI_Anta': self._generate_anta,
            'FAI_Cassetto': self._generate_cassetto,
            'FAI_Ripiano': self._generate_ripiano,
            'FAI_Schienale': self._generate_schienale,
            'FAI_Cornice': self._generate_cornice,
            'FAI_Cappello': self._generate_cappello,
            'FAI_Zoccolo': self._generate_zoccolo,
        }
    
    def _generate_designer(self, size):
        icon = FAI_Designer()
        builder = self._create_svg(size)
        if size == 16:
            return icon.generate_16px(builder).get_svg()
        elif size == 32:
            return icon.generate_32px(builder).get_svg()
        elif size == 64:
            return icon.generate_64px(builder).get_svg()
        else:
            return icon.generate_128px(builder).get_svg()
    
    def _generate_anta(self, size):
        icon = FAI_Anta()
        builder = self._create_svg(size)
        if size == 16:
            return icon.generate_16px(builder).get_svg()
        elif size == 32:
            return icon.generate_32px(builder).get_svg()
        elif size == 64:
            return icon.generate_64px(builder).get_svg()
        else:
            return icon.generate_128px(builder).get_svg()
    
    def _generate_cassetto(self, size):
        icon = FAI_Cassetto()
        builder = self._create_svg(size)
        if size == 16:
            return icon.generate_16px(builder).get_svg()
        elif size == 32:
            return icon.generate_32px(builder).get_svg()
        elif size == 64:
            return icon.generate_64px(builder).get_svg()
        else:
            return icon.generate_128px(builder).get_svg()
    
    def _generate_ripiano(self, size):
        icon = FAI_Ripiano()
        builder = self._create_svg(size)
        if size == 16:
            return icon.generate_16px(builder).get_svg()
        elif size == 32:
            return icon.generate_32px(builder).get_svg()
        elif size == 64:
            return icon.generate_64px(builder).get_svg()
        else:
            return icon.generate_128px(builder).get_svg()
    
    def _generate_schienale(self, size):
        icon = FAI_Schienale()
        builder = self._create_svg(size)
        if size == 16:
            return icon.generate_16px(builder).get_svg()
        elif size == 32:
            return icon.generate_32px(builder).get_svg()
        elif size == 64:
            return icon.generate_64px(builder).get_svg()
        else:
            return icon.generate_128px(builder).get_svg()
    
    def _generate_cornice(self, size):
        icon = FAI_Cornice()
        builder = self._create_svg(size)
        if size == 16:
            return icon.generate_16px(builder).get_svg()
        elif size == 32:
            return icon.generate_32px(builder).get_svg()
        elif size == 64:
            return icon.generate_64px(builder).get_svg()
        else:
            return icon.generate_128px(builder).get_svg()
    
    def _generate_cappello(self, size):
        icon = FAI_Cappello()
        builder = self._create_svg(size)
        if size == 16:
            return icon.generate_16px(builder).get_svg()
        elif size == 32:
            return icon.generate_32px(builder).get_svg()
        elif size == 64:
            return icon.generate_64px(builder).get_svg()
        else:
            return icon.generate_128px(builder).get_svg()
    
    def _generate_zoccolo(self, size):
        icon = FAI_Zoccolo()
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
    'FAI_Designer',
    'FAI_Anta',
    'FAI_Cassetto',
    'FAI_Ripiano',
    'FAI_Schienale',
    'FAI_Cornice',
    'FAI_Cappello',
    'FAI_Zoccolo',
    'ComponentsGenerator'
]
