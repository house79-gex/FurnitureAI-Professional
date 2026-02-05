"""
Impostazioni Panel Icon Generators
5 icons: FAI_ConfiguraIA, FAI_Preferenze, FAI_LibreriaMateriali,
         FAI_CataloghiMateriali, FAI_ListiniPrezzi
"""

import sys
import os
import math

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.icon_base import IconBase, SimpleShapeIcon, IconGenerator
from core.svg_builder import SVGBuilder


class FAI_ConfiguraIA(SimpleShapeIcon):
    """AI config - gear + AI brain"""
    
    def __init__(self):
        super().__init__(
            name="FAI_ConfiguraIA",
            category="Impostazioni",
            description="Configurazione IA"
        )
    
    def generate_16px(self, builder: SVGBuilder) -> SVGBuilder:
        """16px: Gear with brain"""
        # Simple gear
        builder.add_circle(6, 8, 4, fill='none', stroke=self.colors['blue'], stroke_width=2)
        builder.add_circle(6, 8, 2, fill=self.colors['blue_light'])
        
        # AI brain
        builder.add_circle(11, 5, 3, fill=self.colors['purple'], opacity=0.8)
        
        return builder
    
    def generate_32px(self, builder: SVGBuilder) -> SVGBuilder:
        """32px: Gear with AI symbol"""
        # Gear teeth (simplified)
        for angle in range(0, 360, 60):
            rad = math.radians(angle)
            x = 12 + 8 * math.cos(rad)
            y = 16 + 8 * math.sin(rad)
            builder.add_rect(x-1.5, y-1.5, 3, 3, fill=self.colors['blue'])
        
        # Gear center
        builder.add_circle(12, 16, 6, fill=self.colors['blue_light'], 
                          stroke=self.colors['blue'], stroke_width=2)
        builder.add_circle(12, 16, 3, fill=self.colors['white'])
        
        # AI brain
        builder.add_circle(22, 10, 6, fill=self.colors['purple'], opacity=0.8)
        
        # Neural connections
        for angle in [0, 120, 240]:
            rad = math.radians(angle)
            builder.add_line(22, 10, 22 + 3*math.cos(rad), 10 + 3*math.sin(rad), 
                           stroke=self.colors['white'], stroke_width=1)
        
        return builder
    
    def generate_64px(self, builder: SVGBuilder) -> SVGBuilder:
        """64px: Detailed gear and AI"""
        # Gear with teeth
        for angle in range(0, 360, 45):
            rad = math.radians(angle)
            x = 24 + 16 * math.cos(rad)
            y = 32 + 16 * math.sin(rad)
            builder.add_rect(x-2, y-2, 4, 4, fill=self.colors['blue'], rx=1)
        
        # Gear body
        builder.add_circle(24, 32, 12, fill=self.colors['blue_light'], 
                          stroke=self.colors['blue'], stroke_width=2)
        builder.add_circle(24, 32, 8, fill='none', stroke=self.colors['blue'], stroke_width=1.5)
        builder.add_circle(24, 32, 4, fill=self.colors['white'])
        
        # AI brain
        builder.add_circle(44, 20, 10, fill=self.colors['purple'], opacity=0.9)
        
        # Neural network
        for angle in range(0, 360, 60):
            rad = math.radians(angle)
            x = 44 + 6 * math.cos(rad)
            y = 20 + 6 * math.sin(rad)
            builder.add_circle(x, y, 2, fill=self.colors['white'])
            builder.add_line(44, 20, x, y, stroke=self.colors['white'], stroke_width=1, opacity=0.7)
        
        return builder
    
    def generate_128px(self, builder: SVGBuilder) -> SVGBuilder:
        """128px: Complete AI configuration interface"""
        # Large gear with detailed teeth
        for angle in range(0, 360, 30):
            rad = math.radians(angle)
            x = 48 + 32 * math.cos(rad)
            y = 64 + 32 * math.sin(rad)
            builder.add_rect(x-3, y-3, 6, 6, fill=self.colors['blue'], rx=2)
        
        # Gear body with layers
        builder.add_circle(48, 64, 28, fill=self.colors['blue_light'])
        builder.add_circle(48, 64, 24, fill='none', stroke=self.colors['blue'], stroke_width=3)
        builder.add_circle(48, 64, 20, fill=self.colors['blue_light'], opacity=0.5)
        builder.add_circle(48, 64, 16, fill='none', stroke=self.colors['blue'], stroke_width=2)
        builder.add_circle(48, 64, 8, fill=self.colors['white'])
        
        # Bolt holes
        for angle in range(0, 360, 90):
            rad = math.radians(angle)
            x = 48 + 12 * math.cos(rad)
            y = 64 + 12 * math.sin(rad)
            builder.add_circle(x, y, 3, fill=self.colors['medium_gray'])
        
        # AI brain with detailed neural network
        builder.add_circle(88, 40, 20, fill=self.colors['purple'], opacity=0.9)
        
        # Neural nodes and connections
        for ring in [12, 16]:
            for angle in range(0, 360, 60):
                rad = math.radians(angle)
                x = 88 + ring * math.cos(rad)
                y = 40 + ring * math.sin(rad)
                builder.add_circle(x, y, 3, fill=self.colors['white'])
                
                # Connections to center
                builder.add_line(88, 40, x, y, stroke=self.colors['white'], 
                               stroke_width=1.5, opacity=0.5)
        
        # Center node
        builder.add_circle(88, 40, 5, fill=self.colors['white'])
        
        # Inter-node connections
        for angle in [0, 60, 120]:
            rad1 = math.radians(angle)
            rad2 = math.radians(angle + 60)
            x1 = 88 + 16 * math.cos(rad1)
            y1 = 40 + 16 * math.sin(rad1)
            x2 = 88 + 16 * math.cos(rad2)
            y2 = 40 + 16 * math.sin(rad2)
            builder.add_line(x1, y1, x2, y2, stroke=self.colors['white'], 
                           stroke_width=1, opacity=0.3)
        
        # Configuration sliders below
        for i in range(3):
            y = 92 + i * 12
            builder.add_rect(32, y, 64, 4, fill=self.colors['light_gray'], rx=2)
            builder.add_rect(32, y, 32 + i*8, 4, fill=self.colors['purple'], rx=2)
        
        return builder


class FAI_Preferenze(SimpleShapeIcon):
    """Preferences - sliders/settings panel"""
    
    def __init__(self):
        super().__init__(
            name="FAI_Preferenze",
            category="Impostazioni",
            description="Preferenze sistema"
        )
    
    def generate_16px(self, builder: SVGBuilder) -> SVGBuilder:
        """16px: Simple sliders"""
        # Three sliders
        for i in range(3):
            y = 4 + i * 4
            builder.add_line(2, y, 14, y, stroke=self.colors['blue'], stroke_width=1.5)
            builder.add_circle(6 + i*2, y, 2, fill=self.colors['orange'])
        
        return builder
    
    def generate_32px(self, builder: SVGBuilder) -> SVGBuilder:
        """32px: Settings sliders"""
        # Four sliders with different positions
        positions = [8, 18, 12, 22]
        for i, pos in enumerate(positions):
            y = 8 + i * 6
            # Track
            builder.add_rect(4, y-1, 24, 2, fill=self.colors['light_gray'], rx=1)
            # Filled portion
            builder.add_rect(4, y-1, pos-4, 2, fill=self.colors['blue'], rx=1)
            # Handle
            builder.add_circle(pos, y, 3, fill=self.colors['orange'], 
                             stroke=self.colors['white'], stroke_width=1)
        
        return builder
    
    def generate_64px(self, builder: SVGBuilder) -> SVGBuilder:
        """64px: Detailed preferences panel"""
        # Panel background
        builder.add_rect(8, 8, 48, 48, fill=self.colors['very_light_gray'], 
                        stroke=self.colors['blue'], stroke_width=2, rx=2)
        
        # Header
        builder.add_rect(8, 8, 48, 10, fill=self.colors['blue_light'], rx=2)
        
        # Sliders with labels
        slider_data = [(20, 16), (35, 28), (25, 40), (42, 48)]
        
        for i, (pos, y_base) in enumerate(slider_data):
            y = y_base
            # Label indicator
            builder.add_rect(12, y-2, 4, 4, fill=self.colors['blue'], opacity=0.5, rx=1)
            
            # Track
            builder.add_rect(18, y-1, 32, 2, fill=self.colors['light_gray'], rx=1)
            # Filled
            builder.add_rect(18, y-1, pos-18, 2, fill=self.colors['blue'], rx=1)
            # Handle
            builder.add_circle(pos, y, 4, fill=self.colors['orange'], 
                             stroke=self.colors['white'], stroke_width=2)
        
        return builder
    
    def generate_128px(self, builder: SVGBuilder) -> SVGBuilder:
        """128px: Complete preferences interface"""
        # Main panel
        builder.add_rect(16, 16, 96, 96, fill=self.colors['very_light_gray'], 
                        stroke=self.colors['blue'], stroke_width=3, rx=4)
        
        # Header bar
        builder.add_rect(16, 16, 96, 20, fill=self.colors['blue_light'], rx=4)
        
        # Settings icon in header
        builder.add_circle(28, 26, 6, fill='none', stroke=self.colors['blue'], stroke_width=2)
        builder.add_circle(28, 26, 3, fill=self.colors['blue'])
        
        # Multiple preference sliders with labels and values
        slider_configs = [
            (48, 52, "Volume", self.colors['green']),
            (72, 68, "Brightness", self.colors['yellow']),
            (60, 84, "Quality", self.colors['blue']),
            (84, 100, "Speed", self.colors['orange'])
        ]
        
        for pos, y_base, label, color in slider_configs:
            # Label area
            builder.add_rect(24, y_base-6, 16, 8, fill=color, opacity=0.2, rx=2)
            
            # Track
            builder.add_rect(44, y_base-2, 60, 4, fill=self.colors['light_gray'], rx=2)
            
            # Filled portion
            builder.add_rect(44, y_base-2, pos-44, 4, fill=color, rx=2)
            
            # Handle with shadow
            builder.add_circle(pos+1, y_base+1, 7, fill=self.colors['black'], opacity=0.2)
            builder.add_circle(pos, y_base, 7, fill=color, 
                             stroke=self.colors['white'], stroke_width=3)
            builder.add_circle(pos, y_base, 5, fill=self.colors['white'], opacity=0.5)
            
            # Value indicator
            builder.add_rect(106, y_base-3, 8, 6, fill=color, opacity=0.3, rx=1)
        
        # Toggle switches at bottom
        for i in range(3):
            x = 32 + i * 24
            y = 108
            
            # Switch background
            builder.add_rect(x, y-4, 16, 8, fill=self.colors['light_gray'], rx=4)
            
            # Switch knob (on/off states)
            if i % 2 == 0:
                builder.add_circle(x+12, y, 5, fill=self.colors['green'])
            else:
                builder.add_circle(x+4, y, 5, fill=self.colors['medium_gray'])
        
        return builder


class FAI_LibreriaMateriali(SimpleShapeIcon):
    """Material library - bookshelf with materials"""
    
    def __init__(self):
        super().__init__(
            name="FAI_LibreriaMateriali",
            category="Impostazioni",
            description="Libreria materiali"
        )
    
    def generate_16px(self, builder: SVGBuilder) -> SVGBuilder:
        """16px: Simple bookshelf"""
        # Shelves
        builder.add_rect(2, 4, 12, 2, fill=self.colors['medium_gray'])
        builder.add_rect(2, 10, 12, 2, fill=self.colors['medium_gray'])
        
        # Material swatches
        builder.add_rect(3, 6, 3, 3, fill=self.colors['blue'])
        builder.add_rect(7, 6, 3, 3, fill=self.colors['orange'])
        builder.add_rect(11, 6, 3, 3, fill=self.colors['green'])
        
        return builder
    
    def generate_32px(self, builder: SVGBuilder) -> SVGBuilder:
        """32px: Bookshelf with materials"""
        # Frame
        builder.add_rect(4, 4, 24, 24, fill='none', stroke=self.colors['blue'], stroke_width=2)
        
        # Shelves
        builder.add_rect(4, 12, 24, 2, fill=self.colors['medium_gray'])
        builder.add_rect(4, 20, 24, 2, fill=self.colors['medium_gray'])
        
        # Material samples on shelves
        materials = [
            (6, 6, self.colors['blue']),
            (12, 6, self.colors['orange']),
            (18, 6, self.colors['green']),
            (6, 14, self.colors['purple']),
            (12, 14, self.colors['red']),
            (18, 14, self.colors['yellow'])
        ]
        
        for x, y, color in materials:
            builder.add_rect(x, y, 5, 5, fill=color, stroke=self.colors['white'], stroke_width=1)
        
        return builder
    
    def generate_64px(self, builder: SVGBuilder) -> SVGBuilder:
        """64px: Detailed material library"""
        # Bookshelf frame
        builder.add_rect(8, 8, 48, 48, fill=self.colors['light_gray'], 
                        stroke=self.colors['blue'], stroke_width=2, rx=2)
        
        # Multiple shelves
        for i in range(3):
            y = 20 + i * 14
            builder.add_rect(8, y, 48, 3, fill=self.colors['medium_gray'])
        
        # Material swatches on each shelf
        for shelf in range(3):
            for col in range(4):
                x = 12 + col * 11
                y = 10 + shelf * 14
                
                # Different material types
                colors = [self.colors['blue'], self.colors['orange'], 
                         self.colors['green'], self.colors['purple']]
                color = colors[(shelf + col) % 4]
                
                builder.add_rect(x, y, 8, 8, fill=color, 
                               stroke=self.colors['white'], stroke_width=1)
                
                # Texture indication
                if (shelf + col) % 2 == 0:
                    for i in range(3):
                        builder.add_line(x+1, y+2+i*2, x+7, y+2+i*2, 
                                       stroke=self.colors['white'], stroke_width=0.5, opacity=0.5)
        
        return builder
    
    def generate_128px(self, builder: SVGBuilder) -> SVGBuilder:
        """128px: Complete material library system"""
        # Large bookshelf
        builder.add_rect(16, 16, 96, 96, fill=self.colors['light_gray'], 
                        stroke=self.colors['blue'], stroke_width=3, rx=4)
        
        # Decorative top
        builder.add_rect(16, 16, 96, 12, fill=self.colors['blue_light'], rx=4)
        
        # Five shelves
        for i in range(5):
            y = 32 + i * 16
            builder.add_rect(16, y, 96, 4, fill=self.colors['medium_gray'])
        
        # Material swatches organized by type
        material_types = [
            ("Wood", [self.colors['orange'], self.colors['orange_light'], 
                     self.colors['yellow'], self.colors['red']]),
            ("Metal", [self.colors['medium_gray'], self.colors['dark_gray'], 
                      self.colors['blue_dark'], self.colors['black']]),
            ("Glass", [self.colors['blue_light'], self.colors['blue'], 
                      self.colors['white'], self.colors['purple']]),
            ("Fabric", [self.colors['red'], self.colors['purple'], 
                       self.colors['blue'], self.colors['green']]),
            ("Stone", [self.colors['medium_gray'], self.colors['dark_gray'], 
                      self.colors['light_gray'], self.colors['blue_dark']])
        ]
        
        for shelf_idx, (mat_type, colors) in enumerate(material_types):
            y_base = 20 + shelf_idx * 16
            
            for col_idx, color in enumerate(colors):
                x = 24 + col_idx * 20
                
                # Material swatch
                builder.add_rect(x, y_base, 16, 14, fill=color, 
                               stroke=self.colors['white'], stroke_width=2)
                
                # Texture patterns
                if "Wood" in mat_type:
                    for i in range(4):
                        builder.add_path(f"M {x+2} {y_base+3+i*3} Q {x+8} {y_base+4+i*3} {x+14} {y_base+3+i*3}", 
                                       stroke=self.colors['black'], stroke_width=0.5, 
                                       fill='none', opacity=0.3)
                elif "Metal" in mat_type:
                    builder.add_rect(x+2, y_base+2, 12, 10, fill=self.colors['white'], 
                                   opacity=0.2)
                elif "Glass" in mat_type:
                    builder.add_circle(x+4, y_base+4, 2, fill=self.colors['white'], opacity=0.5)
                elif "Fabric" in mat_type:
                    for i in range(7):
                        for j in range(7):
                            if (i + j) % 2 == 0:
                                builder.add_circle(x+2+i*2, y_base+2+j*2, 0.5, 
                                                 fill=self.colors['white'], opacity=0.4)
        
        # Category labels (simplified)
        for i in range(5):
            builder.add_rect(20, 20 + i*16, 4, 4, fill=self.colors['blue'], rx=1)
        
        return builder


class FAI_CataloghiMateriali(SimpleShapeIcon):
    """Material catalogs - folder stack"""
    
    def __init__(self):
        super().__init__(
            name="FAI_CataloghiMateriali",
            category="Impostazioni",
            description="Cataloghi materiali"
        )
    
    def generate_16px(self, builder: SVGBuilder) -> SVGBuilder:
        """16px: Stacked folders"""
        # Three stacked folders
        for i in range(3):
            y = 3 + i * 3
            builder.add_rect(2, y, 12, 3, fill=self.colors['orange'], opacity=0.7-i*0.15)
        
        return builder
    
    def generate_32px(self, builder: SVGBuilder) -> SVGBuilder:
        """32px: Folder stack with tabs"""
        # Stacked folders
        for i in range(3):
            y = 6 + i * 6
            # Tab
            builder.add_rect(4 + i*2, y, 8, 3, fill=self.colors['orange'], rx=1)
            # Folder body
            builder.add_rect(4, y+3, 24, 6, fill=self.colors['orange'], 
                           opacity=0.8-i*0.2, rx=1)
        
        return builder
    
    def generate_64px(self, builder: SVGBuilder) -> SVGBuilder:
        """64px: Detailed catalog stack"""
        # Multiple catalogs
        for i in range(4):
            y = 12 + i * 10
            offset = i * 2
            
            # Folder tab
            builder.add_rect(8 + offset, y, 16, 6, fill=self.colors['orange'], rx=2)
            
            # Folder body
            builder.add_rect(8, y+6, 48, 10, fill=self.colors['orange'], 
                           opacity=0.9-i*0.15, stroke=self.colors['orange_light'], 
                           stroke_width=1.5, rx=2)
            
            # Material indicator dots
            for j in range(3):
                builder.add_circle(16 + j*8, y+11, 2, 
                                 fill=self.colors['white'], opacity=0.7)
        
        return builder
    
    def generate_128px(self, builder: SVGBuilder) -> SVGBuilder:
        """128px: Complete catalog system"""
        # Main catalog stack
        catalogs = [
            (24, "Wood", self.colors['orange']),
            (44, "Metal", self.colors['medium_gray']),
            (64, "Glass", self.colors['blue']),
            (84, "Fabric", self.colors['purple']),
            (104, "Stone", self.colors['dark_gray'])
        ]
        
        for i, (y, mat_type, color) in enumerate(catalogs):
            offset = i * 4
            
            # Folder tab with label
            builder.add_rect(16 + offset, y, 32, 12, fill=color, rx=3)
            
            # Tab label area
            builder.add_rect(20 + offset, y+3, 8, 6, fill=self.colors['white'], 
                           opacity=0.3, rx=1)
            
            # Folder body
            builder.add_rect(16, y+12, 96, 16, fill=color, opacity=0.9-i*0.1, 
                           stroke=color, stroke_width=2, rx=3)
            
            # Material swatches preview in catalog
            for j in range(6):
                swatch_x = 24 + j * 14
                builder.add_rect(swatch_x, y+15, 10, 10, fill=self.colors['white'], 
                               stroke=color, stroke_width=1.5)
                
                # Mini texture preview
                if "Wood" in mat_type:
                    for k in range(3):
                        builder.add_line(swatch_x+1, y+17+k*3, swatch_x+9, y+17+k*3, 
                                       stroke=color, stroke_width=0.5, opacity=0.5)
                elif "Metal" in mat_type:
                    builder.add_rect(swatch_x+2, y+17, 6, 6, fill=color, opacity=0.3)
        
        # Download/sync indicator
        builder.add_circle(104, 32, 12, fill=self.colors['green'], opacity=0.8)
        builder.add_line(104, 28, 104, 34, stroke=self.colors['white'], stroke_width=3)
        builder.add_polygon([(104, 34), (100, 30), (108, 30)], fill=self.colors['white'])
        
        return builder


class FAI_ListiniPrezzi(SimpleShapeIcon):
    """Price lists - document with currency"""
    
    def __init__(self):
        super().__init__(
            name="FAI_ListiniPrezzi",
            category="Impostazioni",
            description="Listini prezzi"
        )
    
    def generate_16px(self, builder: SVGBuilder) -> SVGBuilder:
        """16px: Document with price"""
        # Document
        builder.add_rect(3, 2, 10, 12, fill=self.colors['white'], 
                        stroke=self.colors['blue'], stroke_width=1.5)
        
        # Price lines
        for i in range(3):
            builder.add_line(5, 5 + i*3, 11, 5 + i*3, 
                           stroke=self.colors['green'], stroke_width=1)
        
        return builder
    
    def generate_32px(self, builder: SVGBuilder) -> SVGBuilder:
        """32px: Price list document"""
        # Document
        builder.add_rect(6, 4, 20, 24, fill=self.colors['white'], 
                        stroke=self.colors['blue'], stroke_width=2, rx=1)
        
        # Header
        builder.add_rect(6, 4, 20, 6, fill=self.colors['green'], opacity=0.2, rx=1)
        
        # Price entries
        for i in range(4):
            y = 12 + i * 4
            # Item description
            builder.add_line(10, y, 16, y, stroke=self.colors['blue'], stroke_width=1)
            # Price
            builder.add_line(18, y, 22, y, stroke=self.colors['green'], stroke_width=1.5)
        
        # Currency symbol
        builder.add_circle(22, 8, 3, fill=self.colors['green'])
        builder.add_path("M 22 6 Q 20 6 20 8 Q 20 10 22 10", 
                        stroke=self.colors['white'], stroke_width=1.5, fill='none')
        
        return builder
    
    def generate_64px(self, builder: SVGBuilder) -> SVGBuilder:
        """64px: Detailed price list"""
        # Document with shadow
        builder.add_rect(14, 10, 40, 48, fill=self.colors['white'], 
                        stroke=self.colors['blue'], stroke_width=2, rx=2)
        
        # Header section
        builder.add_rect(14, 10, 40, 12, fill=self.colors['green'], opacity=0.2, rx=2)
        
        # Price list table
        # Column divider
        builder.add_line(42, 22, 42, 54, stroke=self.colors['light_gray'], stroke_width=1)
        
        # Entries with items and prices
        for i in range(6):
            y = 26 + i * 5
            # Item name
            builder.add_line(18, y, 38, y, stroke=self.colors['blue'], stroke_width=1)
            # Price
            builder.add_rect(44, y-1.5, 8, 3, fill=self.colors['green'], opacity=0.5, rx=1)
        
        # Total line
        builder.add_line(18, 54, 50, 54, stroke=self.colors['green'], stroke_width=2)
        
        # Currency badge
        builder.add_circle(48, 16, 5, fill=self.colors['green'])
        builder.add_path("M 48 14 Q 46 14 46 16 Q 46 18 48 18", 
                        stroke=self.colors['white'], stroke_width=2, fill='none')
        
        return builder
    
    def generate_128px(self, builder: SVGBuilder) -> SVGBuilder:
        """128px: Complete price list system"""
        # Main document
        builder.add_rect(28, 20, 80, 96, fill=self.colors['white'], 
                        stroke=self.colors['blue'], stroke_width=3, rx=4)
        
        # Shadow
        builder.add_rect(30, 118, 76, 4, fill=self.colors['black'], opacity=0.1)
        
        # Header with title and date
        builder.add_rect(28, 20, 80, 24, fill=self.colors['green'], opacity=0.15, rx=4)
        
        # Title area
        builder.add_rect(36, 28, 40, 8, fill=self.colors['green'], opacity=0.3, rx=2)
        
        # Date area
        builder.add_rect(80, 28, 20, 8, fill=self.colors['blue'], opacity=0.2, rx=2)
        
        # Table structure
        # Column headers
        builder.add_line(36, 52, 100, 52, stroke=self.colors['blue'], stroke_width=2)
        
        # Column dividers
        builder.add_line(64, 52, 64, 108, stroke=self.colors['light_gray'], stroke_width=1.5)
        builder.add_line(84, 52, 84, 108, stroke=self.colors['light_gray'], stroke_width=1.5)
        
        # Price entries (12 rows)
        for i in range(10):
            y = 60 + i * 5
            
            # Alternating row background
            if i % 2 == 0:
                builder.add_rect(28, y-2, 80, 4, fill=self.colors['very_light_gray'], opacity=0.5)
            
            # Item code/name
            builder.add_rect(36, y-1, 24, 2, fill=self.colors['blue'], opacity=0.4, rx=1)
            
            # Description
            builder.add_rect(66, y-1, 16, 2, fill=self.colors['medium_gray'], opacity=0.3, rx=1)
            
            # Price
            builder.add_rect(86, y-1, 12, 2, fill=self.colors['green'], opacity=0.5, rx=1)
        
        # Total section
        builder.add_line(36, 108, 100, 108, stroke=self.colors['green'], stroke_width=3)
        builder.add_rect(80, 110, 20, 4, fill=self.colors['green'], rx=2)
        
        # Currency indicators
        builder.add_circle(96, 32, 8, fill=self.colors['green'])
        builder.add_path("M 96 28 Q 92 28 92 32 Q 92 36 96 36", 
                        stroke=self.colors['white'], stroke_width=3, fill='none')
        builder.add_line(90, 30, 94, 30, stroke=self.colors['white'], stroke_width=2)
        builder.add_line(90, 34, 94, 34, stroke=self.colors['white'], stroke_width=2)
        
        # Print/export icon
        builder.add_rect(100, 108, 8, 6, fill=self.colors['blue'], rx=1)
        builder.add_rect(101, 109, 6, 3, fill=self.colors['white'])
        
        return builder


class ImpostazioniGenerator(IconGenerator):
    """Generator for Impostazioni Panel icons"""
    
    def __init__(self):
        super().__init__()
    
    def get_icons(self):
        """Return dict of icon names to methods"""
        return {
            'FAI_ConfiguraIA': self._generate_configura_ia,
            'FAI_Preferenze': self._generate_preferenze,
            'FAI_LibreriaMateriali': self._generate_libreria_materiali,
            'FAI_CataloghiMateriali': self._generate_cataloghi_materiali,
            'FAI_ListiniPrezzi': self._generate_listini_prezzi,
        }
    
    def _generate_configura_ia(self, size):
        icon = FAI_ConfiguraIA()
        builder = self._create_svg(size)
        if size == 16:
            return icon.generate_16px(builder).get_svg()
        elif size == 32:
            return icon.generate_32px(builder).get_svg()
        elif size == 64:
            return icon.generate_64px(builder).get_svg()
        else:
            return icon.generate_128px(builder).get_svg()
    
    def _generate_preferenze(self, size):
        icon = FAI_Preferenze()
        builder = self._create_svg(size)
        if size == 16:
            return icon.generate_16px(builder).get_svg()
        elif size == 32:
            return icon.generate_32px(builder).get_svg()
        elif size == 64:
            return icon.generate_64px(builder).get_svg()
        else:
            return icon.generate_128px(builder).get_svg()
    
    def _generate_libreria_materiali(self, size):
        icon = FAI_LibreriaMateriali()
        builder = self._create_svg(size)
        if size == 16:
            return icon.generate_16px(builder).get_svg()
        elif size == 32:
            return icon.generate_32px(builder).get_svg()
        elif size == 64:
            return icon.generate_64px(builder).get_svg()
        else:
            return icon.generate_128px(builder).get_svg()
    
    def _generate_cataloghi_materiali(self, size):
        icon = FAI_CataloghiMateriali()
        builder = self._create_svg(size)
        if size == 16:
            return icon.generate_16px(builder).get_svg()
        elif size == 32:
            return icon.generate_32px(builder).get_svg()
        elif size == 64:
            return icon.generate_64px(builder).get_svg()
        else:
            return icon.generate_128px(builder).get_svg()
    
    def _generate_listini_prezzi(self, size):
        icon = FAI_ListiniPrezzi()
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
    'FAI_ConfiguraIA',
    'FAI_Preferenze',
    'FAI_LibreriaMateriali',
    'FAI_CataloghiMateriali',
    'FAI_ListiniPrezzi',
    'ImpostazioniGenerator'
]
