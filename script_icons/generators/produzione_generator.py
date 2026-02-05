"""
Produzione Panel Icon Generators
7 icons: FAI_Preventivo, FAI_DistintaMateriali, FAI_ListaTaglio, FAI_Nesting,
         FAI_Disegni2D, FAI_Etichette, FAI_Esporta
"""

import sys
import os
import math

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.icon_base import IconBase, SimpleShapeIcon, IconGenerator
from core.svg_builder import SVGBuilder


class FAI_Preventivo(SimpleShapeIcon):
    """Quote - document with currency symbol"""
    
    def __init__(self):
        super().__init__(
            name="FAI_Preventivo",
            category="Produzione",
            description="Preventivo e quotazione"
        )
    
    def generate_16px(self, builder: SVGBuilder) -> SVGBuilder:
        """16px: Document with euro symbol"""
        # Document
        builder.add_rect(3, 2, 10, 12, fill=self.colors['white'], 
                        stroke=self.colors['blue'], stroke_width=1.5)
        
        # Euro symbol
        builder.add_path("M 8 6 Q 6 6 6 8 Q 6 10 8 10", stroke=self.colors['green'], 
                        stroke_width=1.5, fill='none')
        builder.add_line(5, 7, 8, 7, stroke=self.colors['green'], stroke_width=1)
        
        return builder
    
    def generate_32px(self, builder: SVGBuilder) -> SVGBuilder:
        """32px: Document with price"""
        # Document
        builder.add_rect(6, 4, 20, 24, fill=self.colors['white'], 
                        stroke=self.colors['blue'], stroke_width=2, rx=1)
        
        # Header
        builder.add_rect(6, 4, 20, 6, fill=self.colors['blue_light'], rx=1)
        
        # Text lines
        for i in range(3):
            builder.add_line(10, 14 + i*4, 22, 14 + i*4, 
                           stroke=self.colors['light_gray'], stroke_width=1)
        
        # Currency symbol
        builder.add_circle(19, 22, 4, fill=self.colors['green'], opacity=0.8)
        builder.add_path("M 19 20 Q 17 20 17 22 Q 17 24 19 24", 
                        stroke=self.colors['white'], stroke_width=2, fill='none')
        
        return builder
    
    def generate_64px(self, builder: SVGBuilder) -> SVGBuilder:
        """64px: Detailed quote document"""
        # Document with shadow
        builder.add_rect(14, 10, 40, 48, fill=self.colors['white'], 
                        stroke=self.colors['blue'], stroke_width=2, rx=2)
        
        # Header section
        builder.add_rect(14, 10, 40, 12, fill=self.colors['blue_light'], rx=2)
        
        # Item lines with prices
        items = [26, 34, 42, 50]
        for y in items:
            builder.add_line(18, y, 38, y, stroke=self.colors['light_gray'], stroke_width=1)
            builder.add_line(42, y, 50, y, stroke=self.colors['green'], stroke_width=1.5)
        
        # Total line
        builder.add_line(18, 54, 50, 54, stroke=self.colors['blue'], stroke_width=2)
        
        # Currency badge
        builder.add_circle(46, 16, 6, fill=self.colors['green'])
        builder.add_path("M 46 14 Q 44 14 44 16 Q 44 18 46 18", 
                        stroke=self.colors['white'], stroke_width=2, fill='none')
        
        return builder
    
    def generate_128px(self, builder: SVGBuilder) -> SVGBuilder:
        """128px: Complete quote with itemization"""
        # Document
        builder.add_rect(28, 20, 80, 96, fill=self.colors['white'], 
                        stroke=self.colors['blue'], stroke_width=3, rx=4)
        
        # Shadow
        builder.add_rect(30, 118, 76, 4, fill=self.colors['black'], opacity=0.1)
        
        # Header with company info
        builder.add_rect(28, 20, 80, 20, fill=self.colors['blue_light'], rx=4)
        
        # Title
        builder.add_rect(36, 28, 40, 6, fill=self.colors['blue'], opacity=0.3, rx=1)
        
        # Item list with descriptions and prices
        items = [
            (52, "Cabinet", "€ 450"),
            (64, "Hardware", "€ 80"),
            (76, "Materials", "€ 120"),
            (88, "Labor", "€ 200")
        ]
        
        for y, name, price in items:
            # Item line
            builder.add_rect(36, y, 32, 4, fill=self.colors['light_gray'], opacity=0.3, rx=1)
            builder.add_rect(72, y, 24, 4, fill=self.colors['green'], opacity=0.2, rx=1)
        
        # Subtotal, tax, total section
        builder.add_line(36, 96, 96, 96, stroke=self.colors['medium_gray'], stroke_width=1)
        builder.add_rect(72, 100, 24, 4, fill=self.colors['light_gray'], opacity=0.3, rx=1)
        
        # Total line (bold)
        builder.add_line(36, 108, 96, 108, stroke=self.colors['blue'], stroke_width=3)
        builder.add_rect(72, 104, 24, 6, fill=self.colors['green'], opacity=0.4, rx=2)
        
        # Currency badge
        builder.add_circle(96, 32, 10, fill=self.colors['green'])
        builder.add_path("M 96 28 Q 92 28 92 32 Q 92 36 96 36", 
                        stroke=self.colors['white'], stroke_width=3, fill='none')
        builder.add_line(90, 30, 94, 30, stroke=self.colors['white'], stroke_width=2)
        builder.add_line(90, 34, 94, 34, stroke=self.colors['white'], stroke_width=2)
        
        return builder


class FAI_DistintaMateriali(SimpleShapeIcon):
    """BOM - list with quantities"""
    
    def __init__(self):
        super().__init__(
            name="FAI_DistintaMateriali",
            category="Produzione",
            description="Distinta materiali (BOM)"
        )
    
    def generate_16px(self, builder: SVGBuilder) -> SVGBuilder:
        """16px: Simple list"""
        # Document
        builder.add_rect(2, 2, 12, 12, fill=self.colors['white'], 
                        stroke=self.colors['blue'], stroke_width=1.5)
        
        # List items
        for i in range(3):
            y = 5 + i * 3
            builder.add_circle(4, y, 1, fill=self.colors['orange'])
            builder.add_line(6, y, 12, y, stroke=self.colors['blue'], stroke_width=1)
        
        return builder
    
    def generate_32px(self, builder: SVGBuilder) -> SVGBuilder:
        """32px: List with quantities"""
        # Document
        builder.add_rect(4, 4, 24, 24, fill=self.colors['white'], 
                        stroke=self.colors['blue'], stroke_width=2, rx=1)
        
        # Header
        builder.add_rect(4, 4, 24, 6, fill=self.colors['orange_light'], rx=1)
        
        # List items with numbers
        for i in range(4):
            y = 14 + i * 4
            # Quantity box
            builder.add_rect(8, y-1.5, 4, 3, fill=self.colors['orange'], opacity=0.3, rx=1)
            # Description line
            builder.add_line(14, y, 24, y, stroke=self.colors['blue'], stroke_width=1)
        
        return builder
    
    def generate_64px(self, builder: SVGBuilder) -> SVGBuilder:
        """64px: Detailed BOM"""
        # Document
        builder.add_rect(8, 8, 48, 48, fill=self.colors['white'], 
                        stroke=self.colors['blue'], stroke_width=2, rx=2)
        
        # Header with columns
        builder.add_rect(8, 8, 48, 10, fill=self.colors['orange_light'], rx=2)
        builder.add_line(20, 18, 20, 56, stroke=self.colors['light_gray'], stroke_width=1)
        builder.add_line(40, 18, 40, 56, stroke=self.colors['light_gray'], stroke_width=1)
        
        # Items
        for i in range(5):
            y = 24 + i * 6
            # Quantity
            builder.add_rect(12, y-2, 6, 4, fill=self.colors['orange'], opacity=0.4, rx=1)
            # Material name
            builder.add_line(24, y, 36, y, stroke=self.colors['blue'], stroke_width=1)
            # Dimensions
            builder.add_line(42, y, 52, y, stroke=self.colors['green'], stroke_width=1)
        
        return builder
    
    def generate_128px(self, builder: SVGBuilder) -> SVGBuilder:
        """128px: Complete BOM with details"""
        # Document
        builder.add_rect(16, 16, 96, 96, fill=self.colors['white'], 
                        stroke=self.colors['blue'], stroke_width=3, rx=4)
        
        # Header row
        builder.add_rect(16, 16, 96, 16, fill=self.colors['orange_light'], rx=4)
        
        # Column headers (Qty | Part | Material | Dimensions)
        builder.add_line(40, 32, 40, 112, stroke=self.colors['light_gray'], stroke_width=1.5)
        builder.add_line(64, 32, 64, 112, stroke=self.colors['light_gray'], stroke_width=1.5)
        builder.add_line(88, 32, 88, 112, stroke=self.colors['light_gray'], stroke_width=1.5)
        
        # Data rows
        for i in range(8):
            y = 40 + i * 9
            # Alternating row background
            if i % 2 == 0:
                builder.add_rect(16, y-4, 96, 8, fill=self.colors['very_light_gray'], opacity=0.3)
            
            # Quantity (number)
            builder.add_rect(22, y-2, 12, 4, fill=self.colors['orange'], opacity=0.4, rx=1)
            
            # Part name
            builder.add_line(44, y, 60, y, stroke=self.colors['blue'], stroke_width=1.5)
            
            # Material
            builder.add_line(68, y, 84, y, stroke=self.colors['medium_gray'], stroke_width=1.5)
            
            # Dimensions
            builder.add_line(92, y, 104, y, stroke=self.colors['green'], stroke_width=1.5)
        
        # Total row
        builder.add_line(16, 106, 112, 106, stroke=self.colors['blue'], stroke_width=2)
        builder.add_rect(22, 106, 12, 4, fill=self.colors['orange'], rx=1)
        
        return builder


class FAI_ListaTaglio(SimpleShapeIcon):
    """Cut list - panels with dimensions"""
    
    def __init__(self):
        super().__init__(
            name="FAI_ListaTaglio",
            category="Produzione",
            description="Lista taglio pannelli"
        )
    
    def generate_16px(self, builder: SVGBuilder) -> SVGBuilder:
        """16px: Panel with dimension"""
        # Panel
        builder.add_rect(2, 4, 10, 8, fill=self.colors['very_light_gray'], 
                        stroke=self.colors['blue'], stroke_width=1.5)
        
        # Dimension line
        builder.add_line(2, 14, 12, 14, stroke=self.colors['orange'], stroke_width=1)
        
        return builder
    
    def generate_32px(self, builder: SVGBuilder) -> SVGBuilder:
        """32px: Panels with measurements"""
        # Large panel
        builder.add_rect(4, 8, 16, 12, fill=self.colors['very_light_gray'], 
                        stroke=self.colors['blue'], stroke_width=2)
        
        # Small panel
        builder.add_rect(4, 22, 8, 6, fill=self.colors['light_gray'], 
                        stroke=self.colors['blue'], stroke_width=1.5)
        
        # Dimension lines
        builder.add_line(4, 6, 20, 6, stroke=self.colors['orange'], stroke_width=1)
        builder.add_line(22, 8, 22, 20, stroke=self.colors['orange'], stroke_width=1)
        
        return builder
    
    def generate_64px(self, builder: SVGBuilder) -> SVGBuilder:
        """64px: Multiple panels with dimensions"""
        # Panel 1
        builder.add_rect(8, 16, 32, 20, fill=self.colors['very_light_gray'], 
                        stroke=self.colors['blue'], stroke_width=2)
        
        # Panel 2
        builder.add_rect(8, 40, 20, 16, fill=self.colors['light_gray'], 
                        stroke=self.colors['blue'], stroke_width=2)
        
        # Panel 3
        builder.add_rect(32, 40, 16, 10, fill=self.colors['white'], 
                        stroke=self.colors['blue'], stroke_width=1.5)
        
        # Dimension lines with arrows
        # Width dimension
        builder.add_line(8, 12, 40, 12, stroke=self.colors['orange'], stroke_width=2)
        builder.add_line(8, 10, 8, 14, stroke=self.colors['orange'], stroke_width=1)
        builder.add_line(40, 10, 40, 14, stroke=self.colors['orange'], stroke_width=1)
        
        # Height dimension
        builder.add_line(44, 16, 44, 36, stroke=self.colors['orange'], stroke_width=2)
        builder.add_line(42, 16, 46, 16, stroke=self.colors['orange'], stroke_width=1)
        builder.add_line(42, 36, 46, 36, stroke=self.colors['orange'], stroke_width=1)
        
        return builder
    
    def generate_128px(self, builder: SVGBuilder) -> SVGBuilder:
        """128px: Complete cut list with labels"""
        # Main panel with wood grain
        builder.add_rect(16, 32, 64, 40, fill=self.colors['very_light_gray'], 
                        stroke=self.colors['blue'], stroke_width=3)
        
        # Wood grain
        for i in range(5):
            builder.add_path(f"M 20 {36+i*8} Q 48 {37+i*8} 76 {36+i*8}", 
                           stroke=self.colors['light_gray'], stroke_width=0.5, fill='none')
        
        # Secondary panels
        builder.add_rect(16, 80, 40, 32, fill=self.colors['light_gray'], 
                        stroke=self.colors['blue'], stroke_width=2.5)
        builder.add_rect(64, 80, 32, 20, fill=self.colors['white'], 
                        stroke=self.colors['blue'], stroke_width=2)
        
        # Detailed dimension lines for main panel
        # Width
        builder.add_line(16, 24, 80, 24, stroke=self.colors['orange'], stroke_width=3)
        builder.add_line(16, 20, 16, 28, stroke=self.colors['orange'], stroke_width=2)
        builder.add_line(80, 20, 80, 28, stroke=self.colors['orange'], stroke_width=2)
        builder.add_polygon([(20, 24), (16, 22), (16, 26)], fill=self.colors['orange'])
        builder.add_polygon([(76, 24), (80, 22), (80, 26)], fill=self.colors['orange'])
        
        # Height
        builder.add_line(84, 32, 84, 72, stroke=self.colors['orange'], stroke_width=3)
        builder.add_line(80, 32, 88, 32, stroke=self.colors['orange'], stroke_width=2)
        builder.add_line(80, 72, 88, 72, stroke=self.colors['orange'], stroke_width=2)
        builder.add_polygon([(84, 36), (82, 32), (86, 32)], fill=self.colors['orange'])
        builder.add_polygon([(84, 68), (82, 72), (86, 72)], fill=self.colors['orange'])
        
        # Labels
        builder.add_rect(100, 32, 24, 8, fill=self.colors['orange'], opacity=0.8, rx=2)
        builder.add_rect(100, 44, 24, 8, fill=self.colors['orange'], opacity=0.8, rx=2)
        
        # Quantity indicators
        builder.add_circle(24, 40, 8, fill=self.colors['blue'], opacity=0.8)
        builder.add_circle(28, 88, 6, fill=self.colors['blue'], opacity=0.8)
        
        return builder


class FAI_Nesting(SimpleShapeIcon):
    """Nesting - optimized panel layout"""
    
    def __init__(self):
        super().__init__(
            name="FAI_Nesting",
            category="Produzione",
            description="Ottimizzazione nesting"
        )
    
    def generate_16px(self, builder: SVGBuilder) -> SVGBuilder:
        """16px: Simple nested shapes"""
        # Sheet
        builder.add_rect(1, 1, 14, 14, fill='none', stroke=self.colors['blue'], stroke_width=1.5)
        
        # Nested parts
        builder.add_rect(2, 2, 6, 5, fill=self.colors['green'], opacity=0.5)
        builder.add_rect(9, 2, 5, 4, fill=self.colors['orange'], opacity=0.5)
        builder.add_rect(2, 8, 4, 6, fill=self.colors['purple'], opacity=0.5)
        
        return builder
    
    def generate_32px(self, builder: SVGBuilder) -> SVGBuilder:
        """32px: Optimized layout"""
        # Sheet outline
        builder.add_rect(2, 2, 28, 28, fill=self.colors['very_light_gray'], 
                        stroke=self.colors['blue'], stroke_width=2)
        
        # Nested parts with different colors
        builder.add_rect(4, 4, 12, 10, fill=self.colors['green'], opacity=0.4, 
                        stroke=self.colors['green_dark'], stroke_width=1)
        builder.add_rect(18, 4, 10, 8, fill=self.colors['orange'], opacity=0.4, 
                        stroke=self.colors['orange_light'], stroke_width=1)
        builder.add_rect(4, 16, 8, 12, fill=self.colors['purple'], opacity=0.4, 
                        stroke=self.colors['purple'], stroke_width=1)
        builder.add_rect(14, 14, 14, 14, fill=self.colors['blue'], opacity=0.3, 
                        stroke=self.colors['blue_dark'], stroke_width=1)
        
        return builder
    
    def generate_64px(self, builder: SVGBuilder) -> SVGBuilder:
        """64px: Detailed nesting with waste"""
        # Sheet
        builder.add_rect(4, 4, 56, 56, fill=self.colors['very_light_gray'], 
                        stroke=self.colors['blue'], stroke_width=3)
        
        # Optimized parts
        parts = [
            (8, 8, 24, 18, self.colors['green']),
            (34, 8, 22, 14, self.colors['orange']),
            (8, 28, 18, 28, self.colors['purple']),
            (28, 24, 28, 20, self.colors['blue']),
            (34, 46, 22, 10, self.colors['red'])
        ]
        
        for x, y, w, h, color in parts:
            builder.add_rect(x, y, w, h, fill=color, opacity=0.4, 
                           stroke=color, stroke_width=1.5)
        
        # Waste areas (hatched)
        builder.add_rect(8, 58, 48, 2, fill=self.colors['red'], opacity=0.2)
        
        return builder
    
    def generate_128px(self, builder: SVGBuilder) -> SVGBuilder:
        """128px: Complete nesting optimization"""
        # Large sheet
        builder.add_rect(8, 8, 112, 112, fill=self.colors['very_light_gray'], 
                        stroke=self.colors['blue'], stroke_width=4)
        
        # Grid for optimization
        for i in range(1, 8):
            builder.add_line(8 + i*16, 8, 8 + i*16, 120, 
                           stroke=self.colors['light_gray'], stroke_width=0.5, opacity=0.3)
            builder.add_line(8, 8 + i*16, 120, 8 + i*16, 
                           stroke=self.colors['light_gray'], stroke_width=0.5, opacity=0.3)
        
        # Optimally nested parts with labels
        parts = [
            (16, 16, 48, 36, self.colors['green'], "A"),
            (68, 16, 44, 28, self.colors['orange'], "B"),
            (16, 56, 36, 56, self.colors['purple'], "C"),
            (56, 48, 56, 40, self.colors['blue'], "D"),
            (68, 92, 44, 20, self.colors['red'], "E")
        ]
        
        for x, y, w, h, color, label in parts:
            builder.add_rect(x, y, w, h, fill=color, opacity=0.4, 
                           stroke=color, stroke_width=2)
            
            # Part label
            builder.add_circle(x + w//2, y + h//2, 8, fill=self.colors['white'], 
                             stroke=color, stroke_width=2)
        
        # Waste indication (cross-hatch small areas)
        waste_areas = [(16, 116), (56, 116)]
        for wx, wy in waste_areas:
            for i in range(3):
                builder.add_line(wx + i*2, wy, wx + i*2, wy+4, 
                               stroke=self.colors['red'], stroke_width=0.5, opacity=0.5)
        
        # Efficiency indicator
        builder.add_rect(96, 124, 24, 4, fill=self.colors['light_gray'], rx=2)
        builder.add_rect(96, 124, 20, 4, fill=self.colors['green'], rx=2)
        
        return builder


class FAI_Disegni2D(SimpleShapeIcon):
    """2D drawings - technical drawing with dimensions"""
    
    def __init__(self):
        super().__init__(
            name="FAI_Disegni2D",
            category="Produzione",
            description="Disegni tecnici 2D"
        )
    
    def generate_16px(self, builder: SVGBuilder) -> SVGBuilder:
        """16px: Simple blueprint"""
        # Blueprint background
        builder.add_rect(2, 2, 12, 12, fill=self.colors['blue'], opacity=0.2)
        
        # Drawing
        builder.add_rect(4, 4, 8, 8, fill='none', stroke=self.colors['white'], stroke_width=1.5)
        builder.add_line(8, 4, 8, 12, stroke=self.colors['white'], stroke_width=1)
        
        return builder
    
    def generate_32px(self, builder: SVGBuilder) -> SVGBuilder:
        """32px: Technical drawing"""
        # Blueprint
        builder.add_rect(4, 4, 24, 24, fill=self.colors['blue'], opacity=0.2, 
                        stroke=self.colors['blue'], stroke_width=2)
        
        # Cabinet views
        builder.add_rect(8, 8, 12, 16, fill='none', stroke=self.colors['white'], stroke_width=1.5)
        builder.add_line(14, 8, 14, 24, stroke=self.colors['white'], stroke_width=1, stroke_dasharray="2,1")
        
        # Dimension line
        builder.add_line(8, 6, 20, 6, stroke=self.colors['orange'], stroke_width=1)
        
        return builder
    
    def generate_64px(self, builder: SVGBuilder) -> SVGBuilder:
        """64px: Detailed technical drawing"""
        # Blueprint sheet
        builder.add_rect(8, 8, 48, 48, fill=self.colors['blue'], opacity=0.15, 
                        stroke=self.colors['blue'], stroke_width=2, rx=1)
        
        # Front view
        builder.add_rect(16, 16, 20, 28, fill='none', stroke=self.colors['white'], stroke_width=2)
        builder.add_line(16, 30, 36, 30, stroke=self.colors['white'], stroke_width=1, stroke_dasharray="3,2")
        
        # Side view
        builder.add_rect(40, 16, 8, 28, fill='none', stroke=self.colors['white'], stroke_width=1.5)
        
        # Dimension lines
        builder.add_line(16, 12, 36, 12, stroke=self.colors['orange'], stroke_width=1.5)
        builder.add_line(16, 10, 16, 14, stroke=self.colors['orange'], stroke_width=1)
        builder.add_line(36, 10, 36, 14, stroke=self.colors['orange'], stroke_width=1)
        
        return builder
    
    def generate_128px(self, builder: SVGBuilder) -> SVGBuilder:
        """128px: Complete technical drawing set"""
        # Blueprint sheet with title block
        builder.add_rect(16, 16, 96, 96, fill=self.colors['blue'], opacity=0.1, 
                        stroke=self.colors['blue'], stroke_width=3, rx=2)
        
        # Title block
        builder.add_rect(16, 96, 96, 16, fill=self.colors['blue'], opacity=0.2, rx=2)
        
        # Front elevation
        builder.add_rect(32, 32, 40, 56, fill='none', stroke=self.colors['white'], stroke_width=3)
        builder.add_line(32, 60, 72, 60, stroke=self.colors['white'], stroke_width=2, stroke_dasharray="4,3")
        builder.add_line(52, 32, 52, 88, stroke=self.colors['white'], stroke_width=2, stroke_dasharray="4,3")
        
        # Internal details
        builder.add_rect(36, 36, 32, 20, fill='none', stroke=self.colors['white'], stroke_width=1.5)
        
        # Side elevation
        builder.add_rect(80, 32, 16, 56, fill='none', stroke=self.colors['white'], stroke_width=2)
        builder.add_line(80, 60, 96, 60, stroke=self.colors['white'], stroke_width=1.5, stroke_dasharray="4,3")
        
        # Top view
        builder.add_rect(32, 92, 40, 12, fill='none', stroke=self.colors['white'], stroke_width=1.5, stroke_dasharray="2,2")
        
        # Comprehensive dimension lines
        # Width
        builder.add_line(32, 24, 72, 24, stroke=self.colors['orange'], stroke_width=2)
        builder.add_line(32, 22, 32, 26, stroke=self.colors['orange'], stroke_width=1.5)
        builder.add_line(72, 22, 72, 26, stroke=self.colors['orange'], stroke_width=1.5)
        builder.add_polygon([(36, 24), (32, 22), (32, 26)], fill=self.colors['orange'])
        builder.add_polygon([(68, 24), (72, 22), (72, 26)], fill=self.colors['orange'])
        
        # Height
        builder.add_line(24, 32, 24, 88, stroke=self.colors['orange'], stroke_width=2)
        builder.add_line(22, 32, 26, 32, stroke=self.colors['orange'], stroke_width=1.5)
        builder.add_line(22, 88, 26, 88, stroke=self.colors['orange'], stroke_width=1.5)
        builder.add_polygon([(24, 36), (22, 32), (26, 32)], fill=self.colors['orange'])
        builder.add_polygon([(24, 84), (22, 88), (26, 88)], fill=self.colors['orange'])
        
        # Depth
        builder.add_line(104, 32, 104, 88, stroke=self.colors['orange'], stroke_width=2)
        builder.add_line(102, 32, 106, 32, stroke=self.colors['orange'], stroke_width=1.5)
        builder.add_line(102, 88, 106, 88, stroke=self.colors['orange'], stroke_width=1.5)
        
        # Center lines
        builder.add_line(52, 28, 52, 30, stroke=self.colors['blue_light'], stroke_width=2)
        
        return builder


class FAI_Etichette(SimpleShapeIcon):
    """Labels - QR code label"""
    
    def __init__(self):
        super().__init__(
            name="FAI_Etichette",
            category="Produzione",
            description="Etichette e codici"
        )
    
    def generate_16px(self, builder: SVGBuilder) -> SVGBuilder:
        """16px: Simple QR pattern"""
        # Label
        builder.add_rect(2, 4, 12, 8, fill=self.colors['white'], 
                        stroke=self.colors['blue'], stroke_width=1)
        
        # QR-like pattern
        for i in range(3):
            for j in range(3):
                if (i + j) % 2 == 0:
                    builder.add_rect(4 + i*3, 6 + j*2, 2, 1.5, fill=self.colors['black'])
        
        return builder
    
    def generate_32px(self, builder: SVGBuilder) -> SVGBuilder:
        """32px: Label with QR code"""
        # Label sheet
        builder.add_rect(6, 8, 20, 16, fill=self.colors['white'], 
                        stroke=self.colors['blue'], stroke_width=2, rx=1)
        
        # QR code area
        builder.add_rect(8, 10, 8, 8, fill='none', stroke=self.colors['black'], stroke_width=1)
        
        # QR pattern
        for i in range(3):
            for j in range(3):
                if (i + j) % 2 == 0:
                    builder.add_rect(9 + i*2, 11 + j*2, 1.5, 1.5, fill=self.colors['black'])
        
        # Text lines
        builder.add_line(18, 12, 24, 12, stroke=self.colors['blue'], stroke_width=1)
        builder.add_line(18, 16, 24, 16, stroke=self.colors['blue'], stroke_width=1)
        builder.add_line(18, 20, 24, 20, stroke=self.colors['blue'], stroke_width=1)
        
        return builder
    
    def generate_64px(self, builder: SVGBuilder) -> SVGBuilder:
        """64px: Detailed label with barcode"""
        # Label
        builder.add_rect(12, 16, 40, 32, fill=self.colors['white'], 
                        stroke=self.colors['blue'], stroke_width=2, rx=2)
        
        # QR code
        builder.add_rect(16, 20, 16, 16, fill='none', stroke=self.colors['black'], stroke_width=1)
        
        # Detailed QR pattern
        for i in range(5):
            for j in range(5):
                if (i * j + i + j) % 3 != 0:
                    builder.add_rect(17 + i*3, 21 + j*3, 2, 2, fill=self.colors['black'])
        
        # Text info
        builder.add_line(36, 24, 48, 24, stroke=self.colors['blue'], stroke_width=1.5)
        builder.add_line(36, 28, 48, 28, stroke=self.colors['blue'], stroke_width=1.5)
        builder.add_line(36, 32, 44, 32, stroke=self.colors['blue'], stroke_width=1.5)
        
        # Barcode
        for i in range(8):
            w = 2 if i % 3 == 0 else 1
            builder.add_rect(16 + i*4, 40, w, 6, fill=self.colors['black'])
        
        return builder
    
    def generate_128px(self, builder: SVGBuilder) -> SVGBuilder:
        """128px: Complete labeling system"""
        # Large label sheet
        builder.add_rect(24, 32, 80, 64, fill=self.colors['white'], 
                        stroke=self.colors['blue'], stroke_width=3, rx=4)
        
        # Header bar
        builder.add_rect(24, 32, 80, 12, fill=self.colors['blue_light'], rx=4)
        
        # QR code section
        builder.add_rect(32, 52, 32, 32, fill='none', stroke=self.colors['black'], stroke_width=2)
        
        # Detailed QR pattern
        for i in range(8):
            for j in range(8):
                if ((i * j + i + j) % 3 != 0) or (i == 0 or i == 7 or j == 0 or j == 7):
                    size = 3 if (i < 2 or i > 5 or j < 2 or j > 5) else 2.5
                    builder.add_rect(33 + i*3.8, 53 + j*3.8, size, size, fill=self.colors['black'])
        
        # Info section
        info_lines = [56, 64, 72, 80, 88]
        for i, y in enumerate(info_lines):
            length = 32 if i < 3 else 24
            builder.add_rect(72, y-2, length, 3, fill=self.colors['blue'], opacity=0.3, rx=1)
        
        # Barcode at bottom
        builder.add_rect(32, 88, 64, 4, fill=self.colors['light_gray'], rx=1)
        for i in range(20):
            w = 2.5 if i % 4 in [0, 3] else 1.5
            builder.add_rect(33 + i*3.1, 88, w, 4, fill=self.colors['black'])
        
        # Print icon
        builder.add_rect(88, 36, 12, 8, fill=self.colors['medium_gray'], rx=1)
        builder.add_rect(90, 38, 8, 4, fill=self.colors['white'])
        
        return builder


class FAI_Esporta(SimpleShapeIcon):
    """Export - CNC machine icon"""
    
    def __init__(self):
        super().__init__(
            name="FAI_Esporta",
            category="Produzione",
            description="Esporta per CNC"
        )
    
    def generate_16px(self, builder: SVGBuilder) -> SVGBuilder:
        """16px: Simple export arrow"""
        # Box
        builder.add_rect(2, 6, 12, 8, fill=self.colors['very_light_gray'], 
                        stroke=self.colors['blue'], stroke_width=1.5)
        
        # Arrow up
        builder.add_line(8, 10, 8, 2, stroke=self.colors['green'], stroke_width=2)
        builder.add_polygon([(8, 2), (6, 4), (10, 4)], fill=self.colors['green'])
        
        return builder
    
    def generate_32px(self, builder: SVGBuilder) -> SVGBuilder:
        """32px: CNC machine outline"""
        # Machine base
        builder.add_rect(4, 20, 24, 8, fill=self.colors['medium_gray'])
        
        # Work table
        builder.add_rect(8, 16, 16, 4, fill=self.colors['light_gray'], 
                        stroke=self.colors['blue'], stroke_width=1.5)
        
        # Spindle
        builder.add_rect(14, 8, 4, 8, fill=self.colors['orange'])
        builder.add_circle(16, 8, 3, fill=self.colors['dark_gray'])
        
        # Export arrow
        builder.add_line(26, 16, 26, 8, stroke=self.colors['green'], stroke_width=2)
        builder.add_polygon([(26, 8), (24, 10), (28, 10)], fill=self.colors['green'])
        
        return builder
    
    def generate_64px(self, builder: SVGBuilder) -> SVGBuilder:
        """64px: Detailed CNC export"""
        # CNC machine
        # Base
        builder.add_rect(8, 44, 48, 12, fill=self.colors['medium_gray'], rx=2)
        
        # Work table
        builder.add_rect(16, 36, 32, 8, fill=self.colors['light_gray'], 
                        stroke=self.colors['blue'], stroke_width=2)
        
        # Gantry
        builder.add_rect(12, 20, 4, 16, fill=self.colors['dark_gray'])
        builder.add_rect(44, 20, 4, 16, fill=self.colors['dark_gray'])
        builder.add_rect(12, 20, 36, 4, fill=self.colors['dark_gray'])
        
        # Spindle with tool
        builder.add_rect(28, 24, 8, 12, fill=self.colors['orange'], rx=1)
        builder.add_circle(32, 24, 4, fill=self.colors['medium_gray'])
        builder.add_polygon([(32, 36), (30, 40), (34, 40)], fill=self.colors['dark_gray'])
        
        # Export arrow
        builder.add_line(52, 32, 52, 16, stroke=self.colors['green'], stroke_width=3)
        builder.add_polygon([(52, 16), (48, 20), (56, 20)], fill=self.colors['green'])
        
        return builder
    
    def generate_128px(self, builder: SVGBuilder) -> SVGBuilder:
        """128px: Complete CNC export system"""
        # CNC machine detailed
        # Machine base with feet
        builder.add_rect(16, 88, 96, 24, fill=self.colors['medium_gray'], rx=4)
        for x in [24, 56, 88, 104]:
            builder.add_rect(x, 112, 8, 4, fill=self.colors['dark_gray'])
        
        # Work table (bed)
        builder.add_rect(32, 72, 64, 16, fill=self.colors['light_gray'], 
                        stroke=self.colors['blue'], stroke_width=3, rx=2)
        
        # T-slots on table
        for i in range(5):
            builder.add_line(36 + i*12, 76, 36 + i*12, 84, 
                           stroke=self.colors['medium_gray'], stroke_width=1.5)
        
        # Gantry system
        builder.add_rect(24, 40, 8, 32, fill=self.colors['dark_gray'], rx=2)
        builder.add_rect(88, 40, 8, 32, fill=self.colors['dark_gray'], rx=2)
        builder.add_rect(24, 40, 72, 8, fill=self.colors['dark_gray'], rx=2)
        
        # Spindle assembly
        builder.add_rect(56, 48, 16, 24, fill=self.colors['orange'], rx=2)
        builder.add_circle(64, 48, 8, fill=self.colors['medium_gray'], 
                          stroke=self.colors['dark_gray'], stroke_width=2)
        
        # Tool holder
        builder.add_polygon([(64, 72), (60, 80), (68, 80)], fill=self.colors['dark_gray'])
        builder.add_rect(62, 80, 4, 8, fill=self.colors['black'])
        
        # Control panel
        builder.add_rect(104, 56, 16, 20, fill=self.colors['blue_dark'], rx=2)
        builder.add_rect(106, 58, 12, 8, fill=self.colors['green'], opacity=0.3)
        
        # Export arrow with file format
        builder.add_line(104, 64, 104, 32, stroke=self.colors['green'], stroke_width=5)
        builder.add_polygon([(104, 32), (98, 38), (110, 38)], fill=self.colors['green'])
        
        # File icon
        builder.add_rect(96, 20, 16, 20, fill=self.colors['white'], 
                        stroke=self.colors['green'], stroke_width=2, rx=2)
        builder.add_polygon([(112, 20), (112, 28), (104, 28)], fill=self.colors['green_dark'])
        
        return builder


class ProduzioneGenerator(IconGenerator):
    """Generator for Produzione Panel icons"""
    
    def __init__(self):
        super().__init__()
    
    def get_icons(self):
        """Return dict of icon names to methods"""
        return {
            'FAI_Preventivo': self._generate_preventivo,
            'FAI_DistintaMateriali': self._generate_distinta_materiali,
            'FAI_ListaTaglio': self._generate_lista_taglio,
            'FAI_Nesting': self._generate_nesting,
            'FAI_Disegni2D': self._generate_disegni_2d,
            'FAI_Etichette': self._generate_etichette,
            'FAI_Esporta': self._generate_esporta,
        }
    
    def _generate_preventivo(self, size):
        icon = FAI_Preventivo()
        builder = self._create_svg(size)
        if size == 16:
            return icon.generate_16px(builder).get_svg()
        elif size == 32:
            return icon.generate_32px(builder).get_svg()
        elif size == 64:
            return icon.generate_64px(builder).get_svg()
        else:
            return icon.generate_128px(builder).get_svg()
    
    def _generate_distinta_materiali(self, size):
        icon = FAI_DistintaMateriali()
        builder = self._create_svg(size)
        if size == 16:
            return icon.generate_16px(builder).get_svg()
        elif size == 32:
            return icon.generate_32px(builder).get_svg()
        elif size == 64:
            return icon.generate_64px(builder).get_svg()
        else:
            return icon.generate_128px(builder).get_svg()
    
    def _generate_lista_taglio(self, size):
        icon = FAI_ListaTaglio()
        builder = self._create_svg(size)
        if size == 16:
            return icon.generate_16px(builder).get_svg()
        elif size == 32:
            return icon.generate_32px(builder).get_svg()
        elif size == 64:
            return icon.generate_64px(builder).get_svg()
        else:
            return icon.generate_128px(builder).get_svg()
    
    def _generate_nesting(self, size):
        icon = FAI_Nesting()
        builder = self._create_svg(size)
        if size == 16:
            return icon.generate_16px(builder).get_svg()
        elif size == 32:
            return icon.generate_32px(builder).get_svg()
        elif size == 64:
            return icon.generate_64px(builder).get_svg()
        else:
            return icon.generate_128px(builder).get_svg()
    
    def _generate_disegni_2d(self, size):
        icon = FAI_Disegni2D()
        builder = self._create_svg(size)
        if size == 16:
            return icon.generate_16px(builder).get_svg()
        elif size == 32:
            return icon.generate_32px(builder).get_svg()
        elif size == 64:
            return icon.generate_64px(builder).get_svg()
        else:
            return icon.generate_128px(builder).get_svg()
    
    def _generate_etichette(self, size):
        icon = FAI_Etichette()
        builder = self._create_svg(size)
        if size == 16:
            return icon.generate_16px(builder).get_svg()
        elif size == 32:
            return icon.generate_32px(builder).get_svg()
        elif size == 64:
            return icon.generate_64px(builder).get_svg()
        else:
            return icon.generate_128px(builder).get_svg()
    
    def _generate_esporta(self, size):
        icon = FAI_Esporta()
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
    'FAI_Preventivo',
    'FAI_DistintaMateriali',
    'FAI_ListaTaglio',
    'FAI_Nesting',
    'FAI_Disegni2D',
    'FAI_Etichette',
    'FAI_Esporta',
    'ProduzioneGenerator'
]
