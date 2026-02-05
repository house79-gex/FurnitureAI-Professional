"""
Edit Panel Icon Generators
7 icons: FAI_EditaStruttura, FAI_EditaLayout, FAI_EditaInterno, FAI_EditaAperture,
         FAI_ApplicaMateriali, FAI_DuplicaMobile, FAI_ModSolido
"""

import sys
import os
import math

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.icon_base import IconBase, SimpleShapeIcon
from core.svg_builder import SVGBuilder


class FAI_EditaStruttura(SimpleShapeIcon):
    """Edit structure - pencil + cabinet wireframe"""
    
    def __init__(self):
        super().__init__(
            name="FAI_EditaStruttura",
            category="Edita",
            description="Modifica struttura mobile"
        )
    
    def generate_16px(self, builder: SVGBuilder) -> SVGBuilder:
        """16px: Simple cabinet outline + pencil"""
        # Cabinet wireframe
        builder.add_rect(2, 4, 8, 10, fill='none', stroke=self.colors['blue'], stroke_width=1.5)
        
        # Pencil
        builder.add_line(10, 2, 14, 6, stroke=self.colors['orange'], stroke_width=2)
        builder.add_polygon([(14, 6), (15, 7), (13, 9)], fill=self.colors['dark_gray'])
        
        return builder
    
    def generate_32px(self, builder: SVGBuilder) -> SVGBuilder:
        """32px: Cabinet wireframe + pencil with details"""
        # Cabinet wireframe
        builder.add_rect(4, 8, 16, 20, fill='none', stroke=self.colors['blue'], stroke_width=2)
        builder.add_line(4, 18, 20, 18, stroke=self.colors['blue'], stroke_width=1, stroke_dasharray="2,2")
        
        # Pencil
        builder.add_line(20, 4, 28, 12, stroke=self.colors['orange'], stroke_width=3)
        builder.add_polygon([(28, 12), (30, 14), (26, 16)], fill=self.colors['dark_gray'])
        builder.add_circle(20, 4, 2, fill=self.colors['red'])
        
        return builder
    
    def generate_64px(self, builder: SVGBuilder) -> SVGBuilder:
        """64px: Detailed wireframe with editing points"""
        # Cabinet wireframe
        builder.add_rect(8, 16, 32, 40, fill='none', stroke=self.colors['blue'], stroke_width=2)
        builder.add_line(8, 36, 40, 36, stroke=self.colors['blue'], stroke_width=1.5, stroke_dasharray="3,2")
        builder.add_line(24, 16, 24, 56, stroke=self.colors['blue'], stroke_width=1.5, stroke_dasharray="3,2")
        
        # Edit handles
        for x, y in [(8, 16), (40, 16), (8, 56), (40, 56)]:
            builder.add_circle(x, y, 3, fill=self.colors['green'], stroke=self.colors['white'], stroke_width=1)
        
        # Pencil
        builder.add_line(40, 8, 54, 22, stroke=self.colors['orange'], stroke_width=4)
        builder.add_polygon([(54, 22), (58, 26), (50, 30)], fill=self.colors['dark_gray'])
        builder.add_circle(40, 8, 3, fill=self.colors['red'])
        
        return builder
    
    def generate_128px(self, builder: SVGBuilder) -> SVGBuilder:
        """128px: Detailed structure editor with dimensions"""
        # Cabinet wireframe with dimensions
        builder.add_rect(16, 32, 64, 80, fill=self.colors['very_light_gray'], 
                        stroke=self.colors['blue'], stroke_width=3, opacity=0.3)
        
        # Internal divisions
        builder.add_line(16, 72, 80, 72, stroke=self.colors['blue'], stroke_width=2, stroke_dasharray="4,3")
        builder.add_line(48, 32, 48, 112, stroke=self.colors['blue'], stroke_width=2, stroke_dasharray="4,3")
        
        # Edit handles at corners
        for x, y in [(16, 32), (80, 32), (16, 112), (80, 112)]:
            builder.add_rect(x-4, y-4, 8, 8, fill=self.colors['green'], 
                           stroke=self.colors['white'], stroke_width=2)
        
        # Dimension lines
        builder.add_line(16, 28, 80, 28, stroke=self.colors['medium_gray'], stroke_width=1)
        builder.add_line(84, 32, 84, 112, stroke=self.colors['medium_gray'], stroke_width=1)
        
        # Large pencil
        builder.add_line(80, 16, 108, 44, stroke=self.colors['orange'], stroke_width=6)
        builder.add_polygon([(108, 44), (116, 52), (104, 56)], fill=self.colors['dark_gray'])
        builder.add_circle(80, 16, 5, fill=self.colors['red'], stroke=self.colors['orange'], stroke_width=2)
        
        return builder


class FAI_EditaLayout(SimpleShapeIcon):
    """Edit layout - grid with editing tools"""
    
    def __init__(self):
        super().__init__(
            name="FAI_EditaLayout",
            category="Edita",
            description="Modifica layout planimetria"
        )
    
    def generate_16px(self, builder: SVGBuilder) -> SVGBuilder:
        """16px: Simple grid"""
        for i in range(4):
            builder.add_line(4*i, 0, 4*i, 16, stroke=self.colors['blue_light'], stroke_width=1)
            builder.add_line(0, 4*i, 16, 4*i, stroke=self.colors['blue_light'], stroke_width=1)
        
        # Selection box
        builder.add_rect(4, 4, 4, 4, fill='none', stroke=self.colors['green'], stroke_width=2)
        
        return builder
    
    def generate_32px(self, builder: SVGBuilder) -> SVGBuilder:
        """32px: Grid with furniture item"""
        # Grid
        for i in range(5):
            builder.add_line(6*i+4, 4, 6*i+4, 28, stroke=self.colors['blue_light'], stroke_width=1)
            builder.add_line(4, 6*i+4, 28, 6*i+4, stroke=self.colors['blue_light'], stroke_width=1)
        
        # Furniture item
        builder.add_rect(10, 10, 12, 8, fill=self.colors['very_light_gray'], 
                        stroke=self.colors['blue'], stroke_width=2)
        
        # Selection handles
        for x, y in [(10, 10), (22, 10), (10, 18), (22, 18)]:
            builder.add_circle(x, y, 2, fill=self.colors['green'])
        
        return builder
    
    def generate_64px(self, builder: SVGBuilder) -> SVGBuilder:
        """64px: Detailed grid with multiple items"""
        # Grid
        for i in range(9):
            builder.add_line(7*i+8, 8, 7*i+8, 56, stroke=self.colors['blue_light'], stroke_width=1)
            builder.add_line(8, 7*i+8, 56, 7*i+8, stroke=self.colors['blue_light'], stroke_width=1)
        
        # Furniture items
        builder.add_rect(15, 15, 20, 14, fill=self.colors['very_light_gray'], 
                        stroke=self.colors['blue'], stroke_width=2)
        builder.add_rect(36, 29, 14, 20, fill=self.colors['light_gray'], 
                        stroke=self.colors['blue'], stroke_width=1.5)
        
        # Selection handles on first item
        for x, y in [(15, 15), (35, 15), (15, 29), (35, 29)]:
            builder.add_rect(x-2, y-2, 4, 4, fill=self.colors['green'], 
                           stroke=self.colors['white'], stroke_width=1)
        
        return builder
    
    def generate_128px(self, builder: SVGBuilder) -> SVGBuilder:
        """128px: Complete layout editor with toolbar"""
        # Grid
        for i in range(17):
            builder.add_line(7*i+16, 16, 7*i+16, 112, stroke=self.colors['blue_light'], 
                           stroke_width=1, opacity=0.5)
            builder.add_line(16, 7*i+16, 112, 7*i+16, stroke=self.colors['blue_light'], 
                           stroke_width=1, opacity=0.5)
        
        # Multiple furniture items
        items = [(30, 30, 40, 28), (72, 44, 28, 40), (30, 72, 28, 28)]
        for x, y, w, h in items:
            builder.add_rect(x, y, w, h, fill=self.colors['very_light_gray'], 
                           stroke=self.colors['blue'], stroke_width=2)
        
        # Selected item with handles
        sx, sy, sw, sh = items[0]
        for x, y in [(sx, sy), (sx+sw, sy), (sx, sy+sh), (sx+sw, sy+sh)]:
            builder.add_rect(x-3, y-3, 6, 6, fill=self.colors['green'], 
                           stroke=self.colors['white'], stroke_width=2)
        
        # Snap indicators
        builder.add_line(30, 16, 30, 112, stroke=self.colors['orange'], stroke_width=1, 
                        stroke_dasharray="4,4", opacity=0.7)
        
        return builder


class FAI_EditaInterno(SimpleShapeIcon):
    """Edit interior - cabinet with internal divisions"""
    
    def __init__(self):
        super().__init__(
            name="FAI_EditaInterno",
            category="Edita",
            description="Modifica divisioni interne"
        )
    
    def generate_16px(self, builder: SVGBuilder) -> SVGBuilder:
        """16px: Cabinet with divisions"""
        builder.add_rect(2, 2, 12, 12, fill='none', stroke=self.colors['blue'], stroke_width=2)
        builder.add_line(8, 2, 8, 14, stroke=self.colors['orange'], stroke_width=1.5)
        builder.add_line(2, 8, 14, 8, stroke=self.colors['orange'], stroke_width=1.5)
        
        return builder
    
    def generate_32px(self, builder: SVGBuilder) -> SVGBuilder:
        """32px: Cabinet with adjustable shelves"""
        # Cabinet
        builder.add_rect(4, 4, 24, 24, fill=self.colors['very_light_gray'], 
                        stroke=self.colors['blue'], stroke_width=2)
        
        # Divisions
        builder.add_line(16, 4, 16, 28, stroke=self.colors['orange'], stroke_width=2)
        builder.add_line(4, 16, 28, 16, stroke=self.colors['orange'], stroke_width=2)
        
        # Adjustment handles
        builder.add_circle(16, 16, 3, fill=self.colors['green'])
        
        return builder
    
    def generate_64px(self, builder: SVGBuilder) -> SVGBuilder:
        """64px: Detailed interior with multiple divisions"""
        # Cabinet
        builder.add_rect(8, 8, 48, 48, fill=self.colors['very_light_gray'], 
                        stroke=self.colors['blue'], stroke_width=3)
        
        # Vertical division
        builder.add_line(32, 8, 32, 56, stroke=self.colors['orange'], stroke_width=2.5)
        
        # Horizontal shelves
        builder.add_line(8, 26, 56, 26, stroke=self.colors['orange'], stroke_width=2.5)
        builder.add_line(8, 44, 56, 44, stroke=self.colors['orange'], stroke_width=2.5)
        
        # Adjustment handles
        for y in [26, 44]:
            builder.add_rect(28, y-3, 8, 6, fill=self.colors['green'], 
                           stroke=self.colors['white'], stroke_width=1, rx=2)
        
        return builder
    
    def generate_128px(self, builder: SVGBuilder) -> SVGBuilder:
        """128px: Complete interior editor with dimensions"""
        # Cabinet body
        builder.add_rect(16, 16, 96, 96, fill=self.colors['very_light_gray'], 
                        stroke=self.colors['blue'], stroke_width=4)
        
        # Vertical division
        builder.add_line(64, 16, 64, 112, stroke=self.colors['orange'], stroke_width=4)
        
        # Horizontal shelves
        for y in [52, 76, 94]:
            builder.add_line(16, y, 112, y, stroke=self.colors['orange'], stroke_width=3)
            
            # Dimension labels
            builder.add_circle(64, y, 4, fill=self.colors['white'], stroke=self.colors['green'], stroke_width=2)
        
        # Adjustable handles with arrows
        for y in [52, 76, 94]:
            builder.add_rect(60, y-4, 8, 8, fill=self.colors['green'], 
                           stroke=self.colors['white'], stroke_width=2)
            # Up/down arrows
            builder.add_polygon([(64, y-8), (62, y-6), (66, y-6)], fill=self.colors['white'])
            builder.add_polygon([(64, y+8), (62, y+6), (66, y+6)], fill=self.colors['white'])
        
        # 32mm system holes
        for x in [20, 108]:
            for y in range(20, 108, 8):
                builder.add_circle(x, y, 1.5, fill=self.colors['medium_gray'], opacity=0.5)
        
        return builder


class FAI_EditaAperture(SimpleShapeIcon):
    """Edit openings - door with adjustment arrows"""
    
    def __init__(self):
        super().__init__(
            name="FAI_EditaAperture",
            category="Edita",
            description="Modifica aperture porte"
        )
    
    def generate_16px(self, builder: SVGBuilder) -> SVGBuilder:
        """16px: Door with arrow"""
        builder.add_rect(4, 2, 8, 12, fill=self.colors['very_light_gray'], 
                        stroke=self.colors['blue'], stroke_width=1.5)
        
        # Arrow
        builder.add_line(8, 8, 12, 8, stroke=self.colors['green'], stroke_width=2)
        builder.add_polygon([(12, 8), (10, 7), (10, 9)], fill=self.colors['green'])
        
        return builder
    
    def generate_32px(self, builder: SVGBuilder) -> SVGBuilder:
        """32px: Door with opening arc"""
        # Door
        builder.add_rect(8, 4, 16, 24, fill=self.colors['very_light_gray'], 
                        stroke=self.colors['blue'], stroke_width=2)
        self.add_handle(builder, 20, 16, 32, 'circle')
        
        # Opening arc
        builder.add_path("M 8 28 Q 16 20 24 28", stroke=self.colors['green'], 
                        stroke_width=2, fill='none', stroke_dasharray="3,2")
        
        # Arrow
        builder.add_polygon([(24, 28), (22, 26), (22, 30)], fill=self.colors['green'])
        
        return builder
    
    def generate_64px(self, builder: SVGBuilder) -> SVGBuilder:
        """64px: Door with adjustment controls"""
        # Door
        builder.add_rect(16, 8, 32, 48, fill=self.colors['very_light_gray'], 
                        stroke=self.colors['blue'], stroke_width=2)
        self.add_handle(builder, 40, 32, 64, 'bar')
        
        # Opening arc with angle
        builder.add_path("M 16 56 Q 32 40 48 56", stroke=self.colors['green'], 
                        stroke_width=2.5, fill='none')
        
        # Arrow
        builder.add_polygon([(48, 56), (44, 52), (44, 58)], fill=self.colors['green'])
        
        # Angle indicator
        builder.add_circle(16, 56, 3, fill=self.colors['orange'])
        
        # Adjustment arrows
        builder.add_polygon([(52, 24), (50, 26), (54, 26)], fill=self.colors['orange'])
        builder.add_polygon([(52, 44), (50, 42), (54, 42)], fill=self.colors['orange'])
        
        return builder
    
    def generate_128px(self, builder: SVGBuilder) -> SVGBuilder:
        """128px: Detailed opening editor"""
        # Door with frame
        builder.add_rect(32, 16, 64, 96, fill=self.colors['very_light_gray'], 
                        stroke=self.colors['blue'], stroke_width=3)
        builder.add_rect(36, 20, 56, 88, fill='none', stroke=self.colors['blue_light'], stroke_width=2)
        
        # Handle
        self.add_handle(builder, 80, 64, 128, 'bar')
        
        # Opening arc with angle measurement
        builder.add_path("M 32 112 Q 64 80 96 112", stroke=self.colors['green'], 
                        stroke_width=4, fill='none')
        
        # Arrow
        builder.add_polygon([(96, 112), (90, 106), (90, 116)], fill=self.colors['green'])
        
        # Angle arc
        builder.add_path("M 36 112 Q 38 108 40 112", stroke=self.colors['orange'], 
                        stroke_width=2, fill='none')
        
        # Hinge points
        for y in [32, 64, 96]:
            builder.add_rect(28, y-4, 8, 8, fill=self.colors['medium_gray'])
            builder.add_circle(32, y, 2, fill=self.colors['dark_gray'])
        
        # Adjustment controls
        for y in [48, 80]:
            builder.add_rect(100, y-4, 12, 8, fill=self.colors['orange'], rx=2)
            builder.add_polygon([(106, y-8), (104, y-6), (108, y-6)], fill=self.colors['white'])
            builder.add_polygon([(106, y+8), (104, y+6), (108, y+6)], fill=self.colors['white'])
        
        return builder


class FAI_ApplicaMateriali(SimpleShapeIcon):
    """Apply materials - paint brush + material swatches"""
    
    def __init__(self):
        super().__init__(
            name="FAI_ApplicaMateriali",
            category="Edita",
            description="Applica materiali e finiture"
        )
    
    def generate_16px(self, builder: SVGBuilder) -> SVGBuilder:
        """16px: Brush + color swatch"""
        # Brush
        builder.add_line(3, 13, 7, 9, stroke=self.colors['dark_gray'], stroke_width=2)
        builder.add_polygon([(7, 9), (9, 7), (11, 9), (9, 11)], fill=self.colors['orange'])
        
        # Swatch
        builder.add_rect(10, 2, 4, 4, fill=self.colors['blue'])
        
        return builder
    
    def generate_32px(self, builder: SVGBuilder) -> SVGBuilder:
        """32px: Brush with swatches"""
        # Brush
        builder.add_line(6, 26, 14, 18, stroke=self.colors['dark_gray'], stroke_width=3)
        builder.add_polygon([(14, 18), (18, 14), (22, 18), (18, 22)], fill=self.colors['orange'])
        
        # Material swatches
        colors = [self.colors['blue'], self.colors['green'], self.colors['red']]
        for i, color in enumerate(colors):
            builder.add_rect(18 + i*4, 4, 3, 3, fill=color)
        
        return builder
    
    def generate_64px(self, builder: SVGBuilder) -> SVGBuilder:
        """64px: Detailed brush and palette"""
        # Brush handle
        builder.add_line(12, 52, 28, 36, stroke=self.colors['dark_gray'], stroke_width=4)
        builder.add_circle(12, 52, 3, fill=self.colors['medium_gray'])
        
        # Brush bristles
        builder.add_polygon([(28, 36), (36, 28), (40, 32), (32, 40)], fill=self.colors['orange'])
        
        # Material palette
        materials = [
            (44, 8, self.colors['blue']),
            (52, 8, self.colors['green']),
            (44, 16, self.colors['red']),
            (52, 16, self.colors['purple'])
        ]
        for x, y, color in materials:
            builder.add_rect(x, y, 6, 6, fill=color, stroke=self.colors['white'], stroke_width=1)
        
        return builder
    
    def generate_128px(self, builder: SVGBuilder) -> SVGBuilder:
        """128px: Complete material application tool"""
        # Large brush
        builder.add_line(24, 104, 56, 72, stroke=self.colors['dark_gray'], stroke_width=6)
        builder.add_circle(24, 104, 5, fill=self.colors['medium_gray'])
        
        # Metal ferrule
        builder.add_rect(50, 66, 12, 8, fill=self.colors['medium_gray'])
        
        # Bristles
        builder.add_polygon([(56, 72), (72, 56), (80, 64), (64, 80)], fill=self.colors['orange'])
        
        # Material library panel
        builder.add_rect(80, 16, 32, 96, fill=self.colors['light_gray'], 
                        stroke=self.colors['medium_gray'], stroke_width=2, rx=2)
        
        # Material swatches with textures
        materials = [
            (84, 20, self.colors['blue'], "Wood"),
            (84, 36, self.colors['green'], "Metal"),
            (84, 52, self.colors['red'], "Glass"),
            (84, 68, self.colors['purple'], "Fabric"),
            (84, 84, self.colors['yellow'], "Stone"),
            (84, 100, self.colors['orange'], "Plastic")
        ]
        
        for x, y, color, name in materials:
            builder.add_rect(x, y, 24, 12, fill=color, 
                           stroke=self.colors['white'], stroke_width=1.5, rx=1)
            
            # Texture pattern
            if name == "Wood":
                for i in range(3):
                    builder.add_line(x+2, y+3+i*3, x+22, y+3+i*3, 
                                   stroke=self.colors['white'], stroke_width=0.5, opacity=0.5)
        
        return builder


class FAI_DuplicaMobile(SimpleShapeIcon):
    """Duplicate furniture - two overlapping cabinets"""
    
    def __init__(self):
        super().__init__(
            name="FAI_DuplicaMobile",
            category="Edita",
            description="Duplica mobile"
        )
    
    def generate_16px(self, builder: SVGBuilder) -> SVGBuilder:
        """16px: Two overlapping rectangles"""
        builder.add_rect(2, 4, 8, 8, fill=self.colors['very_light_gray'], 
                        stroke=self.colors['blue'], stroke_width=1.5)
        builder.add_rect(6, 8, 8, 8, fill=self.colors['white'], 
                        stroke=self.colors['green'], stroke_width=1.5)
        
        return builder
    
    def generate_32px(self, builder: SVGBuilder) -> SVGBuilder:
        """32px: Two cabinets with arrow"""
        # Original
        builder.add_rect(4, 8, 12, 16, fill=self.colors['very_light_gray'], 
                        stroke=self.colors['blue'], stroke_width=2)
        self.add_handle(builder, 12, 16, 32, 'circle')
        
        # Arrow
        builder.add_line(16, 16, 20, 16, stroke=self.colors['green'], stroke_width=2)
        builder.add_polygon([(20, 16), (18, 14), (18, 18)], fill=self.colors['green'])
        
        # Duplicate
        builder.add_rect(20, 12, 12, 16, fill=self.colors['white'], 
                        stroke=self.colors['green'], stroke_width=2)
        self.add_handle(builder, 28, 20, 32, 'circle')
        
        return builder
    
    def generate_64px(self, builder: SVGBuilder) -> SVGBuilder:
        """64px: Detailed duplication with offset"""
        # Original cabinet
        builder.add_rect(8, 16, 24, 32, fill=self.colors['very_light_gray'], 
                        stroke=self.colors['blue'], stroke_width=2)
        builder.add_line(8, 32, 32, 32, stroke=self.colors['blue'], stroke_width=1.5)
        self.add_handle(builder, 28, 32, 64, 'bar')
        
        # Arrow
        builder.add_line(32, 32, 38, 32, stroke=self.colors['green'], stroke_width=3)
        builder.add_polygon([(38, 32), (35, 30), (35, 34)], fill=self.colors['green'])
        
        # Duplicate cabinet (slightly offset)
        builder.add_rect(40, 20, 24, 32, fill=self.colors['white'], 
                        stroke=self.colors['green'], stroke_width=2.5)
        builder.add_line(40, 36, 64, 36, stroke=self.colors['green'], stroke_width=1.5)
        self.add_handle(builder, 60, 36, 64, 'bar')
        
        return builder
    
    def generate_128px(self, builder: SVGBuilder) -> SVGBuilder:
        """128px: Complete duplication with multiple copies"""
        # Original cabinet
        builder.add_rect(16, 32, 48, 64, fill=self.colors['very_light_gray'], 
                        stroke=self.colors['blue'], stroke_width=3)
        builder.add_line(16, 64, 64, 64, stroke=self.colors['blue'], stroke_width=2)
        self.add_handle(builder, 56, 64, 128, 'bar')
        
        # Copy indicator
        builder.add_circle(56, 40, 12, fill=self.colors['blue'], opacity=0.8)
        builder.add_line(52, 40, 60, 40, stroke=self.colors['white'], stroke_width=2)
        builder.add_line(56, 36, 56, 44, stroke=self.colors['white'], stroke_width=2)
        
        # Arrow
        builder.add_line(64, 64, 76, 64, stroke=self.colors['green'], stroke_width=4)
        builder.add_polygon([(76, 64), (72, 60), (72, 68)], fill=self.colors['green'])
        
        # Duplicated cabinet
        builder.add_rect(80, 36, 48, 64, fill=self.colors['white'], 
                        stroke=self.colors['green'], stroke_width=3)
        builder.add_line(80, 68, 128, 68, stroke=self.colors['green'], stroke_width=2)
        self.add_handle(builder, 120, 68, 128, 'bar')
        
        # Multiple copy indicators (3x)
        builder.add_rect(100, 20, 8, 6, fill=self.colors['green'], rx=1)
        
        return builder


class FAI_ModSolido(SimpleShapeIcon):
    """3D solid editor - 3D cube with editing handles"""
    
    def __init__(self):
        super().__init__(
            name="FAI_ModSolido",
            category="Edita",
            description="Editor solido 3D"
        )
    
    def generate_16px(self, builder: SVGBuilder) -> SVGBuilder:
        """16px: Simple 3D cube"""
        # 3D cube
        builder.add_polygon([(4, 6), (8, 4), (12, 6), (8, 8)], fill=self.colors['blue_light'])
        builder.add_polygon([(4, 6), (4, 10), (8, 12), (8, 8)], fill=self.colors['blue'])
        builder.add_polygon([(12, 6), (12, 10), (8, 12), (8, 8)], fill=self.colors['blue_dark'])
        
        return builder
    
    def generate_32px(self, builder: SVGBuilder) -> SVGBuilder:
        """32px: 3D cube with edit handles"""
        # 3D cube faces
        builder.add_polygon([(8, 12), (16, 8), (24, 12), (16, 16)], fill=self.colors['blue_light'])
        builder.add_polygon([(8, 12), (8, 20), (16, 24), (16, 16)], fill=self.colors['blue'])
        builder.add_polygon([(24, 12), (24, 20), (16, 24), (16, 16)], fill=self.colors['blue_dark'])
        
        # Edit handles
        for x, y in [(8, 12), (24, 12), (16, 24)]:
            builder.add_circle(x, y, 2, fill=self.colors['green'], stroke=self.colors['white'], stroke_width=1)
        
        return builder
    
    def generate_64px(self, builder: SVGBuilder) -> SVGBuilder:
        """64px: Detailed 3D solid with axes"""
        # 3D cube
        builder.add_polygon([(16, 24), (32, 16), (48, 24), (32, 32)], fill=self.colors['blue_light'])
        builder.add_polygon([(16, 24), (16, 40), (32, 48), (32, 32)], fill=self.colors['blue'])
        builder.add_polygon([(48, 24), (48, 40), (32, 48), (32, 32)], fill=self.colors['blue_dark'])
        
        # Edit handles at vertices
        for x, y in [(16, 24), (48, 24), (16, 40), (48, 40), (32, 16), (32, 48)]:
            builder.add_rect(x-3, y-3, 6, 6, fill=self.colors['green'], 
                           stroke=self.colors['white'], stroke_width=1)
        
        # Axis arrows
        builder.add_line(32, 32, 52, 32, stroke=self.colors['red'], stroke_width=2)
        builder.add_polygon([(52, 32), (49, 30), (49, 34)], fill=self.colors['red'])
        
        return builder
    
    def generate_128px(self, builder: SVGBuilder) -> SVGBuilder:
        """128px: Complete 3D editor with XYZ axes"""
        # Large 3D cube
        builder.add_polygon([(32, 48), (64, 32), (96, 48), (64, 64)], fill=self.colors['blue_light'])
        builder.add_polygon([(32, 48), (32, 80), (64, 96), (64, 64)], fill=self.colors['blue'])
        builder.add_polygon([(96, 48), (96, 80), (64, 96), (64, 64)], fill=self.colors['blue_dark'])
        
        # Edge lines
        builder.add_line(32, 48, 32, 80, stroke=self.colors['blue_dark'], stroke_width=2)
        builder.add_line(96, 48, 96, 80, stroke=self.colors['blue_dark'], stroke_width=2)
        builder.add_line(32, 80, 64, 96, stroke=self.colors['blue_dark'], stroke_width=2)
        builder.add_line(96, 80, 64, 96, stroke=self.colors['blue_dark'], stroke_width=2)
        
        # Edit handles at all vertices
        vertices = [(32, 48), (96, 48), (32, 80), (96, 80), (64, 32), (64, 96)]
        for x, y in vertices:
            builder.add_rect(x-4, y-4, 8, 8, fill=self.colors['green'], 
                           stroke=self.colors['white'], stroke_width=2)
        
        # XYZ axis arrows
        # X axis (red)
        builder.add_line(64, 64, 104, 64, stroke=self.colors['red'], stroke_width=3)
        builder.add_polygon([(104, 64), (100, 61), (100, 67)], fill=self.colors['red'])
        
        # Y axis (green)
        builder.add_line(64, 64, 64, 104, stroke=self.colors['green_dark'], stroke_width=3)
        builder.add_polygon([(64, 104), (61, 100), (67, 100)], fill=self.colors['green_dark'])
        
        # Z axis (blue)
        builder.add_line(64, 64, 44, 54, stroke=self.colors['blue'], stroke_width=3)
        builder.add_polygon([(44, 54), (47, 56), (45, 60)], fill=self.colors['blue'])
        
        # Axis labels
        builder.add_circle(108, 64, 8, fill=self.colors['red'], opacity=0.2)
        builder.add_circle(64, 108, 8, fill=self.colors['green'], opacity=0.2)
        builder.add_circle(40, 50, 8, fill=self.colors['blue'], opacity=0.2)
        
        return builder


# Export all icon classes
__all__ = [
    'FAI_EditaStruttura',
    'FAI_EditaLayout',
    'FAI_EditaInterno',
    'FAI_EditaAperture',
    'FAI_ApplicaMateriali',
    'FAI_DuplicaMobile',
    'FAI_ModSolido'
]
