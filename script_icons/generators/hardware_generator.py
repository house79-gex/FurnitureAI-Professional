"""
Hardware Panel Icon Generators
3 icons: FAI_Ferramenta, FAI_Accessori, FAI_Cataloghi
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.icon_base import IconBase, SimpleShapeIcon, IconGenerator
from core.svg_builder import SVGBuilder


class FAI_Ferramenta(SimpleShapeIcon):
    """Hardware - hinge + drawer slide"""
    
    def __init__(self):
        super().__init__(
            name="FAI_Ferramenta",
            category="Hardware",
            description="Ferramenta e guide"
        )
    
    def generate_16px(self, builder: SVGBuilder) -> SVGBuilder:
        """16px: Simple hinge"""
        # Hinge plates
        builder.add_rect(2, 4, 5, 8, fill=self.colors['medium_gray'])
        builder.add_rect(9, 4, 5, 8, fill=self.colors['medium_gray'])
        
        # Pin
        builder.add_circle(8, 8, 2, fill=self.colors['dark_gray'])
        
        return builder
    
    def generate_32px(self, builder: SVGBuilder) -> SVGBuilder:
        """32px: Hinge with screws"""
        # Left plate
        builder.add_rect(4, 8, 10, 16, fill=self.colors['medium_gray'], rx=1)
        builder.add_circle(9, 12, 1.5, fill=self.colors['dark_gray'])
        builder.add_circle(9, 20, 1.5, fill=self.colors['dark_gray'])
        
        # Right plate
        builder.add_rect(18, 8, 10, 16, fill=self.colors['medium_gray'], rx=1)
        builder.add_circle(23, 12, 1.5, fill=self.colors['dark_gray'])
        builder.add_circle(23, 20, 1.5, fill=self.colors['dark_gray'])
        
        # Center pin
        builder.add_circle(16, 16, 4, fill=self.colors['dark_gray'])
        builder.add_circle(16, 16, 2, fill=self.colors['black'])
        
        return builder
    
    def generate_64px(self, builder: SVGBuilder) -> SVGBuilder:
        """64px: Detailed hinge and drawer slide"""
        # Hinge - left plate
        builder.add_rect(8, 16, 16, 32, fill=self.colors['medium_gray'], rx=2)
        for y in [22, 30, 38]:
            builder.add_circle(16, y, 2, fill=self.colors['dark_gray'])
        
        # Hinge - right plate
        builder.add_rect(40, 16, 16, 32, fill=self.colors['medium_gray'], rx=2)
        for y in [22, 30, 38]:
            builder.add_circle(48, y, 2, fill=self.colors['dark_gray'])
        
        # Center barrel
        builder.add_circle(32, 32, 8, fill=self.colors['dark_gray'])
        builder.add_circle(32, 32, 4, fill=self.colors['black'])
        
        # Drawer slide rail below
        builder.add_rect(12, 52, 40, 4, fill=self.colors['light_gray'], 
                        stroke=self.colors['medium_gray'], stroke_width=1)
        builder.add_rect(16, 50, 8, 8, fill=self.colors['medium_gray'], rx=2)
        
        return builder
    
    def generate_128px(self, builder: SVGBuilder) -> SVGBuilder:
        """128px: Complete hardware set"""
        # European hinge
        # Left mounting plate
        builder.add_rect(16, 32, 32, 64, fill=self.colors['medium_gray'], rx=4)
        for y in [44, 60, 76, 92]:
            builder.add_circle(32, y, 3, fill=self.colors['dark_gray'])
            builder.add_circle(32, y, 1.5, fill=self.colors['black'])
        
        # Right mounting plate
        builder.add_rect(80, 32, 32, 64, fill=self.colors['medium_gray'], rx=4)
        for y in [44, 60, 76, 92]:
            builder.add_circle(96, y, 3, fill=self.colors['dark_gray'])
            builder.add_circle(96, y, 1.5, fill=self.colors['black'])
        
        # Center mechanism
        builder.add_circle(64, 64, 16, fill=self.colors['dark_gray'])
        builder.add_circle(64, 64, 8, fill=self.colors['black'])
        
        # Hinge arms
        builder.add_rect(48, 60, 16, 8, fill=self.colors['light_gray'], rx=2)
        builder.add_rect(64, 60, 16, 8, fill=self.colors['light_gray'], rx=2)
        
        # Drawer slide system below
        builder.add_rect(24, 104, 80, 8, fill=self.colors['light_gray'], 
                        stroke=self.colors['medium_gray'], stroke_width=2, rx=2)
        
        # Slide rollers
        for x in [32, 64, 96]:
            builder.add_circle(x, 108, 6, fill=self.colors['medium_gray'], 
                             stroke=self.colors['dark_gray'], stroke_width=2)
            builder.add_circle(x, 108, 3, fill=self.colors['white'])
        
        return builder


class FAI_Accessori(SimpleShapeIcon):
    """Accessories - handles and knobs collection"""
    
    def __init__(self):
        super().__init__(
            name="FAI_Accessori",
            category="Hardware",
            description="Maniglie e pomelli"
        )
    
    def generate_16px(self, builder: SVGBuilder) -> SVGBuilder:
        """16px: Simple handle"""
        builder.add_rect(4, 6, 8, 4, fill=self.colors['medium_gray'], rx=2)
        builder.add_circle(6, 8, 1, fill=self.colors['dark_gray'])
        builder.add_circle(10, 8, 1, fill=self.colors['dark_gray'])
        
        return builder
    
    def generate_32px(self, builder: SVGBuilder) -> SVGBuilder:
        """32px: Handle and knob"""
        # Bar handle
        builder.add_rect(6, 8, 20, 6, fill=self.colors['medium_gray'], rx=3)
        builder.add_rect(8, 9, 16, 4, fill=self.colors['light_gray'], rx=2)
        
        # Knob
        builder.add_circle(16, 24, 5, fill=self.colors['medium_gray'])
        builder.add_circle(16, 24, 3, fill=self.colors['light_gray'])
        builder.add_circle(16, 24, 1.5, fill=self.colors['white'])
        
        return builder
    
    def generate_64px(self, builder: SVGBuilder) -> SVGBuilder:
        """64px: Multiple accessory types"""
        # Bar handle
        builder.add_rect(12, 16, 40, 12, fill=self.colors['medium_gray'], rx=6)
        builder.add_rect(14, 18, 36, 8, fill=self.colors['light_gray'], rx=4)
        
        # Mounting screws
        builder.add_circle(16, 22, 2, fill=self.colors['dark_gray'])
        builder.add_circle(48, 22, 2, fill=self.colors['dark_gray'])
        
        # Round knob
        builder.add_circle(24, 48, 8, fill=self.colors['medium_gray'])
        builder.add_circle(24, 48, 6, fill=self.colors['light_gray'])
        builder.add_circle(24, 48, 3, fill=self.colors['white'])
        
        # Cup pull handle
        builder.add_path("M 44 40 L 44 52 Q 48 56 52 52 L 52 40", 
                        stroke=self.colors['medium_gray'], stroke_width=4, fill='none')
        builder.add_rect(42, 38, 12, 4, fill=self.colors['medium_gray'], rx=2)
        
        return builder
    
    def generate_128px(self, builder: SVGBuilder) -> SVGBuilder:
        """128px: Complete accessory catalog"""
        # Modern bar handle
        builder.add_rect(24, 32, 80, 20, fill=self.colors['medium_gray'], rx=10)
        builder.add_rect(28, 36, 72, 12, fill=self.colors['light_gray'], rx=6)
        
        # Mounting points
        for x in [32, 96]:
            builder.add_circle(x, 42, 4, fill=self.colors['dark_gray'])
            builder.add_circle(x, 42, 2, fill=self.colors['black'])
        
        # Decorative knob
        builder.add_circle(48, 80, 16, fill=self.colors['medium_gray'])
        builder.add_circle(48, 80, 12, fill=self.colors['light_gray'])
        builder.add_circle(48, 80, 8, fill=self.colors['white'])
        builder.add_circle(48, 80, 4, fill=self.colors['medium_gray'])
        
        # Vintage cup pull
        builder.add_path("M 88 68 L 88 92 Q 96 100 104 92 L 104 68", 
                        stroke=self.colors['medium_gray'], stroke_width=6, fill='none')
        builder.add_rect(84, 64, 24, 8, fill=self.colors['medium_gray'], rx=4)
        
        # Shell pull
        builder.add_path("M 16 92 Q 16 108 32 112 Q 32 108 32 92", 
                        fill=self.colors['light_gray'], stroke=self.colors['medium_gray'], stroke_width=2)
        for i in range(5):
            builder.add_line(16 + i*4, 92, 16 + i*4, 108, 
                           stroke=self.colors['medium_gray'], stroke_width=0.5)
        
        return builder


class FAI_Cataloghi(SimpleShapeIcon):
    """Catalogs - folder with download arrow"""
    
    def __init__(self):
        super().__init__(
            name="FAI_Cataloghi",
            category="Hardware",
            description="Cataloghi componenti"
        )
    
    def generate_16px(self, builder: SVGBuilder) -> SVGBuilder:
        """16px: Simple folder with arrow"""
        # Folder
        builder.add_rect(2, 4, 12, 10, fill=self.colors['orange'])
        builder.add_rect(2, 2, 6, 2, fill=self.colors['orange_light'])
        
        # Download arrow
        builder.add_line(8, 7, 8, 11, stroke=self.colors['white'], stroke_width=2)
        builder.add_polygon([(8, 11), (6, 9), (10, 9)], fill=self.colors['white'])
        
        return builder
    
    def generate_32px(self, builder: SVGBuilder) -> SVGBuilder:
        """32px: Folder with document"""
        # Folder tab
        builder.add_rect(4, 4, 12, 6, fill=self.colors['orange'], rx=1)
        
        # Folder body
        builder.add_rect(4, 10, 24, 18, fill=self.colors['orange'], 
                        stroke=self.colors['orange_light'], stroke_width=2, rx=2)
        
        # Document inside
        builder.add_rect(10, 14, 12, 10, fill=self.colors['white'], opacity=0.9)
        
        # Download arrow
        builder.add_line(16, 16, 16, 21, stroke=self.colors['blue'], stroke_width=2)
        builder.add_polygon([(16, 21), (14, 19), (18, 19)], fill=self.colors['blue'])
        
        return builder
    
    def generate_64px(self, builder: SVGBuilder) -> SVGBuilder:
        """64px: Open catalog with multiple pages"""
        # Folder tab
        builder.add_rect(8, 8, 24, 12, fill=self.colors['orange'], rx=2)
        
        # Folder body
        builder.add_rect(8, 20, 48, 36, fill=self.colors['orange'], 
                        stroke=self.colors['orange_light'], stroke_width=2, rx=3)
        
        # Multiple documents
        for i in range(3):
            builder.add_rect(14 + i*2, 26 + i*2, 20, 24, fill=self.colors['white'], 
                           stroke=self.colors['light_gray'], stroke_width=1)
        
        # Download indicator
        builder.add_circle(48, 32, 10, fill=self.colors['green'], opacity=0.9)
        builder.add_line(48, 28, 48, 34, stroke=self.colors['white'], stroke_width=3)
        builder.add_polygon([(48, 34), (45, 31), (51, 31)], fill=self.colors['white'])
        
        return builder
    
    def generate_128px(self, builder: SVGBuilder) -> SVGBuilder:
        """128px: Complete catalog system"""
        # Large folder tab
        builder.add_rect(16, 16, 48, 24, fill=self.colors['orange'], rx=4)
        
        # Folder body
        builder.add_rect(16, 40, 96, 72, fill=self.colors['orange'], 
                        stroke=self.colors['orange_light'], stroke_width=3, rx=5)
        
        # Shadow
        builder.add_rect(18, 42, 92, 6, fill=self.colors['dark_gray'], opacity=0.2)
        
        # Multiple catalog pages
        pages = [(24, 52, 32, 52), (48, 52, 32, 52), (72, 52, 32, 52)]
        for i, (x, y, w, h) in enumerate(pages):
            builder.add_rect(x, y, w, h, fill=self.colors['white'], 
                           stroke=self.colors['light_gray'], stroke_width=1.5)
            
            # Page content - hardware icons
            if i == 0:
                # Hinge icon
                builder.add_circle(40, 70, 6, fill=self.colors['medium_gray'])
            elif i == 1:
                # Handle icon
                builder.add_rect(56, 68, 16, 4, fill=self.colors['medium_gray'], rx=2)
            else:
                # Knob icon
                builder.add_circle(88, 70, 5, fill=self.colors['medium_gray'])
            
            # Text lines
            for j in range(3):
                builder.add_line(x+4, y+h-16+j*4, x+w-4, y+h-16+j*4, 
                               stroke=self.colors['light_gray'], stroke_width=1)
        
        # Download badge
        builder.add_circle(96, 64, 16, fill=self.colors['green'], opacity=0.9)
        builder.add_line(96, 56, 96, 68, stroke=self.colors['white'], stroke_width=4)
        builder.add_polygon([(96, 68), (91, 63), (101, 63)], fill=self.colors['white'])
        
        # Cloud icon
        builder.add_path("M 92 52 Q 88 48 84 52 Q 80 52 80 56 Q 80 60 84 60 L 108 60 Q 112 60 112 56 Q 112 52 108 52", 
                        fill=self.colors['white'], opacity=0.3)
        
        return builder


class HardwareGenerator(IconGenerator):
    """Generator for Hardware Panel icons"""
    
    def __init__(self):
        super().__init__()
    
    def get_icons(self):
        """Return dict of icon names to methods"""
        return {
            'FAI_Ferramenta': self._generate_ferramenta,
            'FAI_Accessori': self._generate_accessori,
            'FAI_Cataloghi': self._generate_cataloghi,
        }
    
    def _generate_ferramenta(self, size):
        icon = FAI_Ferramenta()
        builder = self._create_svg(size)
        if size == 16:
            return icon.generate_16px(builder).get_svg()
        elif size == 32:
            return icon.generate_32px(builder).get_svg()
        elif size == 64:
            return icon.generate_64px(builder).get_svg()
        else:
            return icon.generate_128px(builder).get_svg()
    
    def _generate_accessori(self, size):
        icon = FAI_Accessori()
        builder = self._create_svg(size)
        if size == 16:
            return icon.generate_16px(builder).get_svg()
        elif size == 32:
            return icon.generate_32px(builder).get_svg()
        elif size == 64:
            return icon.generate_64px(builder).get_svg()
        else:
            return icon.generate_128px(builder).get_svg()
    
    def _generate_cataloghi(self, size):
        icon = FAI_Cataloghi()
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
    'FAI_Ferramenta',
    'FAI_Accessori',
    'FAI_Cataloghi',
    'HardwareGenerator'
]
