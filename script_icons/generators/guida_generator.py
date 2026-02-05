"""
Guida Panel Icon Generators
7 icons: FAI_GuidaRapida, FAI_TutorialVideo, FAI_EsempiProgetti, FAI_DocumentazioneAPI,
         FAI_Community, FAI_CheckUpdate, FAI_About
"""

import sys
import os
import math

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.icon_base import IconBase, SimpleShapeIcon
from core.svg_builder import SVGBuilder


class FAI_GuidaRapida(SimpleShapeIcon):
    """Quick guide - book with lightbulb"""
    
    def __init__(self):
        super().__init__(
            name="FAI_GuidaRapida",
            category="Guida",
            description="Guida rapida"
        )
    
    def generate_16px(self, builder: SVGBuilder) -> SVGBuilder:
        """16px: Book with bulb"""
        # Book
        builder.add_rect(2, 4, 8, 10, fill=self.colors['blue_light'], 
                        stroke=self.colors['blue'], stroke_width=1.5)
        builder.add_line(6, 4, 6, 14, stroke=self.colors['blue'], stroke_width=1)
        
        # Lightbulb
        builder.add_circle(12, 6, 3, fill=self.colors['yellow'])
        
        return builder
    
    def generate_32px(self, builder: SVGBuilder) -> SVGBuilder:
        """32px: Open book with idea"""
        # Book
        builder.add_rect(4, 8, 16, 20, fill=self.colors['blue_light'], 
                        stroke=self.colors['blue'], stroke_width=2, rx=1)
        builder.add_line(12, 8, 12, 28, stroke=self.colors['blue'], stroke_width=2)
        
        # Pages
        for i in range(3):
            builder.add_line(6, 12 + i*4, 10, 12 + i*4, 
                           stroke=self.colors['blue'], stroke_width=1)
            builder.add_line(14, 12 + i*4, 18, 12 + i*4, 
                           stroke=self.colors['blue'], stroke_width=1)
        
        # Lightbulb
        builder.add_circle(24, 12, 5, fill=self.colors['yellow'], opacity=0.8)
        builder.add_rect(22, 17, 4, 3, fill=self.colors['medium_gray'])
        
        return builder
    
    def generate_64px(self, builder: SVGBuilder) -> SVGBuilder:
        """64px: Detailed guide book"""
        # Open book
        builder.add_rect(8, 16, 24, 32, fill=self.colors['blue_light'], 
                        stroke=self.colors['blue'], stroke_width=2, rx=2)
        builder.add_line(20, 16, 20, 48, stroke=self.colors['blue'], stroke_width=2)
        
        # Left page content
        for i in range(5):
            builder.add_line(12, 22 + i*4, 18, 22 + i*4, 
                           stroke=self.colors['blue'], stroke_width=1)
        
        # Right page content
        for i in range(5):
            builder.add_line(24, 22 + i*4, 28, 22 + i*4, 
                           stroke=self.colors['blue'], stroke_width=1)
        
        # Lightbulb with glow
        builder.add_circle(48, 24, 10, fill=self.colors['yellow'], opacity=0.3)
        builder.add_circle(48, 24, 7, fill=self.colors['yellow'])
        builder.add_rect(45, 31, 6, 5, fill=self.colors['medium_gray'], rx=1)
        
        # Light rays
        for angle in [30, 60, 120, 150]:
            rad = math.radians(angle)
            builder.add_line(48, 24, 48 + 14*math.cos(rad), 24 + 14*math.sin(rad), 
                           stroke=self.colors['yellow'], stroke_width=1.5, opacity=0.5)
        
        return builder
    
    def generate_128px(self, builder: SVGBuilder) -> SVGBuilder:
        """128px: Complete quick guide"""
        # Large open book
        builder.add_rect(16, 32, 48, 64, fill=self.colors['blue_light'], 
                        stroke=self.colors['blue'], stroke_width=3, rx=4)
        builder.add_line(40, 32, 40, 96, stroke=self.colors['blue'], stroke_width=3)
        
        # Left page - numbered steps
        for i in range(5):
            y = 42 + i * 10
            builder.add_circle(24, y, 4, fill=self.colors['blue'], opacity=0.7)
            builder.add_line(30, y, 36, y, stroke=self.colors['blue'], stroke_width=1.5)
        
        # Right page - illustrations
        for i in range(3):
            y = 42 + i * 16
            builder.add_rect(46, y-4, 14, 8, fill=self.colors['very_light_gray'], 
                           stroke=self.colors['blue'], stroke_width=1)
        
        # Large lightbulb with detailed glow
        builder.add_circle(96, 48, 20, fill=self.colors['yellow'], opacity=0.2)
        builder.add_circle(96, 48, 15, fill=self.colors['yellow'], opacity=0.5)
        builder.add_circle(96, 48, 12, fill=self.colors['yellow'])
        
        # Filament
        builder.add_path("M 96 40 L 96 44 L 92 48 L 96 52 L 100 48 L 96 44", 
                        stroke=self.colors['orange'], stroke_width=2, fill='none')
        
        # Base
        builder.add_rect(90, 60, 12, 8, fill=self.colors['medium_gray'], rx=2)
        builder.add_rect(92, 68, 8, 4, fill=self.colors['dark_gray'], rx=1)
        
        # Light rays
        for angle in range(0, 180, 20):
            rad = math.radians(angle)
            length = 28 + (angle % 40)
            builder.add_line(96, 48, 96 + length*math.cos(rad), 48 + length*math.sin(rad), 
                           stroke=self.colors['yellow'], stroke_width=2, opacity=0.4)
        
        return builder


class FAI_TutorialVideo(SimpleShapeIcon):
    """Video tutorials - play button + film strip"""
    
    def __init__(self):
        super().__init__(
            name="FAI_TutorialVideo",
            category="Guida",
            description="Tutorial video"
        )
    
    def generate_16px(self, builder: SVGBuilder) -> SVGBuilder:
        """16px: Play button"""
        # Screen
        builder.add_rect(2, 2, 12, 10, fill=self.colors['dark_gray'], 
                        stroke=self.colors['blue'], stroke_width=1.5, rx=1)
        
        # Play button
        builder.add_polygon([(6, 5), (6, 9), (10, 7)], fill=self.colors['white'])
        
        return builder
    
    def generate_32px(self, builder: SVGBuilder) -> SVGBuilder:
        """32px: Video player"""
        # Screen
        builder.add_rect(4, 6, 24, 18, fill=self.colors['dark_gray'], 
                        stroke=self.colors['blue'], stroke_width=2, rx=2)
        
        # Play button
        builder.add_circle(16, 15, 6, fill=self.colors['white'], opacity=0.9)
        builder.add_polygon([(14, 13), (14, 17), (19, 15)], fill=self.colors['blue'])
        
        # Film strip holes
        for i in range(5):
            builder.add_circle(6 + i*4, 26, 1.5, fill=self.colors['blue_light'])
        
        return builder
    
    def generate_64px(self, builder: SVGBuilder) -> SVGBuilder:
        """64px: Video player with controls"""
        # Screen
        builder.add_rect(8, 12, 48, 36, fill=self.colors['dark_gray'], 
                        stroke=self.colors['blue'], stroke_width=2, rx=3)
        
        # Video content (simplified cabinet)
        builder.add_rect(16, 20, 16, 20, fill=self.colors['blue_light'], opacity=0.3)
        
        # Large play button
        builder.add_circle(32, 30, 10, fill=self.colors['white'], opacity=0.9)
        builder.add_polygon([(28, 26), (28, 34), (38, 30)], fill=self.colors['red'])
        
        # Controls bar
        builder.add_rect(8, 48, 48, 6, fill=self.colors['black'], opacity=0.7)
        builder.add_rect(12, 50, 20, 2, fill=self.colors['red'])
        
        # Film strip
        builder.add_rect(8, 54, 48, 4, fill=self.colors['orange_light'], opacity=0.5)
        for i in range(10):
            builder.add_rect(10 + i*4.5, 55, 2, 2, fill=self.colors['black'], opacity=0.3)
        
        return builder
    
    def generate_128px(self, builder: SVGBuilder) -> SVGBuilder:
        """128px: Complete video tutorial interface"""
        # Main screen
        builder.add_rect(16, 24, 96, 72, fill=self.colors['dark_gray'], 
                        stroke=self.colors['blue'], stroke_width=4, rx=6)
        
        # Video content preview (furniture being built)
        builder.add_rect(32, 40, 32, 40, fill=self.colors['blue_light'], 
                        opacity=0.2, stroke=self.colors['blue'], stroke_width=2)
        
        # Large play button with shadow
        builder.add_circle(64, 60, 20, fill=self.colors['black'], opacity=0.3)
        builder.add_circle(64, 60, 18, fill=self.colors['white'], opacity=0.95)
        builder.add_polygon([(56, 52), (56, 68), (76, 60)], fill=self.colors['red'])
        
        # Progress bar
        builder.add_rect(16, 96, 96, 8, fill=self.colors['black'], opacity=0.7, rx=4)
        builder.add_rect(20, 98, 48, 4, fill=self.colors['red'], rx=2)
        
        # Control buttons
        controls = [24, 44, 84, 104]
        for x in controls:
            builder.add_circle(x, 108, 6, fill=self.colors['white'], opacity=0.8)
        
        # Film strip at bottom
        builder.add_rect(16, 112, 96, 12, fill=self.colors['orange_light'], 
                        stroke=self.colors['orange'], stroke_width=2, rx=2)
        
        # Film perforations
        for i in range(20):
            builder.add_rect(20 + i*4.5, 114, 3, 3, fill=self.colors['dark_gray'], rx=1)
            builder.add_rect(20 + i*4.5, 119, 3, 3, fill=self.colors['dark_gray'], rx=1)
        
        # Frame indicators
        for i in range(6):
            builder.add_rect(26 + i*14, 115, 8, 6, fill=self.colors['blue'], opacity=0.3)
        
        # Duration label
        builder.add_rect(96, 100, 12, 6, fill=self.colors['blue'], opacity=0.7, rx=1)
        
        return builder


class FAI_EsempiProgetti(SimpleShapeIcon):
    """Project examples - gallery grid"""
    
    def __init__(self):
        super().__init__(
            name="FAI_EsempiProgetti",
            category="Guida",
            description="Esempi progetti"
        )
    
    def generate_16px(self, builder: SVGBuilder) -> SVGBuilder:
        """16px: Simple grid"""
        # 2x2 grid
        for i in range(2):
            for j in range(2):
                builder.add_rect(2 + i*7, 2 + j*7, 6, 6, 
                               fill=self.colors['blue_light'], 
                               stroke=self.colors['blue'], stroke_width=1)
        
        return builder
    
    def generate_32px(self, builder: SVGBuilder) -> SVGBuilder:
        """32px: Gallery grid"""
        # 3x2 grid of projects
        for i in range(3):
            for j in range(2):
                builder.add_rect(4 + i*9, 6 + j*10, 8, 9, 
                               fill=self.colors['very_light_gray'], 
                               stroke=self.colors['blue'], stroke_width=1.5)
                
                # Mini cabinet in each
                builder.add_rect(5 + i*9, 8 + j*10, 6, 5, 
                               fill=self.colors['blue_light'], opacity=0.5)
        
        return builder
    
    def generate_64px(self, builder: SVGBuilder) -> SVGBuilder:
        """64px: Detailed gallery"""
        # Gallery frame
        builder.add_rect(4, 4, 56, 56, fill=self.colors['light_gray'], 
                        stroke=self.colors['blue'], stroke_width=2, rx=2)
        
        # 3x3 grid of example projects
        for i in range(3):
            for j in range(3):
                x = 8 + i*18
                y = 8 + j*18
                
                builder.add_rect(x, y, 16, 16, 
                               fill=self.colors['white'], 
                               stroke=self.colors['blue'], stroke_width=1.5)
                
                # Different furniture types
                if (i + j) % 3 == 0:
                    # Cabinet
                    builder.add_rect(x+4, y+4, 8, 8, 
                                   fill=self.colors['blue_light'], opacity=0.6)
                elif (i + j) % 3 == 1:
                    # Drawer
                    builder.add_rect(x+3, y+5, 10, 6, 
                                   fill=self.colors['green'], opacity=0.5)
                else:
                    # Shelf
                    builder.add_rect(x+3, y+6, 10, 2, 
                                   fill=self.colors['orange'], opacity=0.6)
        
        return builder
    
    def generate_128px(self, builder: SVGBuilder) -> SVGBuilder:
        """128px: Complete project gallery"""
        # Gallery container
        builder.add_rect(8, 8, 112, 112, fill=self.colors['light_gray'], 
                        stroke=self.colors['blue'], stroke_width=3, rx=4)
        
        # Header
        builder.add_rect(8, 8, 112, 16, fill=self.colors['blue_light'], rx=4)
        
        # 4x3 grid of detailed project examples
        for i in range(4):
            for j in range(3):
                x = 14 + i*27
                y = 30 + j*28
                
                # Project card
                builder.add_rect(x, y, 24, 24, 
                               fill=self.colors['white'], 
                               stroke=self.colors['blue'], stroke_width=2, rx=2)
                
                # Project content (different furniture types)
                furniture_type = (i + j) % 5
                
                if furniture_type == 0:
                    # Kitchen cabinet
                    builder.add_rect(x+4, y+4, 16, 16, 
                                   fill=self.colors['blue_light'], opacity=0.5)
                    builder.add_line(x+12, y+4, x+12, y+20, 
                                   stroke=self.colors['blue'], stroke_width=1)
                    builder.add_circle(x+15, y+12, 1.5, fill=self.colors['medium_gray'])
                    
                elif furniture_type == 1:
                    # Wardrobe
                    builder.add_rect(x+4, y+4, 16, 16, 
                                   fill=self.colors['green'], opacity=0.4)
                    builder.add_line(x+12, y+4, x+12, y+20, 
                                   stroke=self.colors['green_dark'], stroke_width=2)
                    
                elif furniture_type == 2:
                    # Drawer unit
                    for d in range(3):
                        builder.add_rect(x+4, y+5+d*5, 16, 4, 
                                       fill=self.colors['orange'], opacity=0.5)
                        
                elif furniture_type == 3:
                    # Bookshelf
                    for s in range(4):
                        builder.add_rect(x+4, y+5+s*4, 16, 2, 
                                       fill=self.colors['purple'], opacity=0.5)
                else:
                    # Entertainment center
                    builder.add_rect(x+4, y+4, 16, 10, 
                                   fill=self.colors['red'], opacity=0.3)
                    builder.add_rect(x+4, y+15, 7, 5, 
                                   fill=self.colors['orange'], opacity=0.4)
                    builder.add_rect(x+13, y+15, 7, 5, 
                                   fill=self.colors['orange'], opacity=0.4)
        
        # "More" button
        builder.add_circle(104, 104, 12, fill=self.colors['blue'], opacity=0.8)
        builder.add_line(100, 104, 108, 104, stroke=self.colors['white'], stroke_width=2)
        builder.add_line(104, 100, 104, 108, stroke=self.colors['white'], stroke_width=2)
        
        return builder


class FAI_DocumentazioneAPI(SimpleShapeIcon):
    """API docs - code brackets + document"""
    
    def __init__(self):
        super().__init__(
            name="FAI_DocumentazioneAPI",
            category="Guida",
            description="Documentazione API"
        )
    
    def generate_16px(self, builder: SVGBuilder) -> SVGBuilder:
        """16px: Code brackets"""
        # Document
        builder.add_rect(3, 2, 10, 12, fill=self.colors['white'], 
                        stroke=self.colors['blue'], stroke_width=1)
        
        # Code brackets
        builder.add_path("M 6 6 L 5 8 L 6 10", stroke=self.colors['green'], 
                        stroke_width=1.5, fill='none')
        builder.add_path("M 10 6 L 11 8 L 10 10", stroke=self.colors['green'], 
                        stroke_width=1.5, fill='none')
        
        return builder
    
    def generate_32px(self, builder: SVGBuilder) -> SVGBuilder:
        """32px: Code document"""
        # Document
        builder.add_rect(6, 4, 20, 24, fill=self.colors['white'], 
                        stroke=self.colors['blue'], stroke_width=2, rx=1)
        
        # Code brackets
        builder.add_path("M 10 10 L 8 16 L 10 22", stroke=self.colors['green'], 
                        stroke_width=2, fill='none')
        builder.add_path("M 22 10 L 24 16 L 22 22", stroke=self.colors['green'], 
                        stroke_width=2, fill='none')
        
        # Code lines
        for i in range(3):
            builder.add_line(12, 12 + i*4, 20, 12 + i*4, 
                           stroke=self.colors['blue'], stroke_width=1)
        
        return builder
    
    def generate_64px(self, builder: SVGBuilder) -> SVGBuilder:
        """64px: API documentation"""
        # Document
        builder.add_rect(12, 8, 40, 48, fill=self.colors['white'], 
                        stroke=self.colors['blue'], stroke_width=2, rx=2)
        
        # Header "API"
        builder.add_rect(12, 8, 40, 10, fill=self.colors['green'], opacity=0.2, rx=2)
        
        # Large code brackets
        builder.add_path("M 16 22 L 12 32 L 16 42", stroke=self.colors['green'], 
                        stroke_width=3, fill='none')
        builder.add_path("M 48 22 L 52 32 L 48 42", stroke=self.colors['green'], 
                        stroke_width=3, fill='none')
        
        # Code content
        for i in range(5):
            length = 24 if i % 2 == 0 else 20
            builder.add_rect(20, 24 + i*6, length, 2, 
                           fill=self.colors['blue'], opacity=0.6, rx=1)
        
        return builder
    
    def generate_128px(self, builder: SVGBuilder) -> SVGBuilder:
        """128px: Complete API documentation"""
        # Document
        builder.add_rect(24, 16, 80, 96, fill=self.colors['white'], 
                        stroke=self.colors['blue'], stroke_width=3, rx=4)
        
        # Header section with "API Documentation"
        builder.add_rect(24, 16, 80, 20, fill=self.colors['green'], opacity=0.2, rx=4)
        
        # API badge
        builder.add_rect(32, 22, 16, 8, fill=self.colors['green'], rx=2)
        
        # Large code brackets
        builder.add_path("M 32 44 L 24 64 L 32 84", stroke=self.colors['green'], 
                        stroke_width=4, fill='none')
        builder.add_path("M 96 44 L 104 64 L 96 84", stroke=self.colors['green'], 
                        stroke_width=4, fill='none')
        
        # Code blocks with syntax highlighting
        code_blocks = [
            (44, 48, 32, 4, self.colors['purple']),   # Function
            (44, 56, 24, 3, self.colors['blue']),     # Method
            (48, 62, 20, 2, self.colors['orange']),   # Parameter
            (48, 68, 28, 2, self.colors['orange']),   # Parameter
            (44, 74, 16, 3, self.colors['blue']),     # Return
            (44, 82, 28, 4, self.colors['purple'])    # Function
        ]
        
        for x, y, w, h, color in code_blocks:
            builder.add_rect(x, y, w, h, fill=color, opacity=0.5, rx=1)
        
        # Curly braces for code blocks
        builder.add_path("M 40 52 L 38 58 L 40 64", stroke=self.colors['medium_gray'], 
                        stroke_width=2, fill='none')
        builder.add_path("M 80 52 L 82 58 L 80 64", stroke=self.colors['medium_gray'], 
                        stroke_width=2, fill='none')
        
        # Method parameters indicators
        for y in [62, 68]:
            builder.add_circle(44, y, 2, fill=self.colors['green'])
        
        # Documentation comments
        builder.add_rect(40, 92, 48, 3, fill=self.colors['light_gray'], opacity=0.5, rx=1)
        builder.add_rect(40, 98, 40, 3, fill=self.colors['light_gray'], opacity=0.5, rx=1)
        
        return builder


class FAI_Community(SimpleShapeIcon):
    """Community - people icons connected"""
    
    def __init__(self):
        super().__init__(
            name="FAI_Community",
            category="Guida",
            description="Community e supporto"
        )
    
    def generate_16px(self, builder: SVGBuilder) -> SVGBuilder:
        """16px: Three people"""
        # Simple person icons
        for i in range(3):
            x = 3 + i * 5
            builder.add_circle(x, 5, 2, fill=self.colors['blue'])
            builder.add_circle(x, 11, 3, fill=self.colors['blue'])
        
        return builder
    
    def generate_32px(self, builder: SVGBuilder) -> SVGBuilder:
        """32px: Connected people"""
        # People
        people = [(10, 12), (16, 8), (22, 12)]
        
        for x, y in people:
            # Head
            builder.add_circle(x, y, 3, fill=self.colors['blue'])
            # Body
            builder.add_circle(x, y+6, 4, fill=self.colors['blue_light'])
        
        # Connections
        builder.add_line(10, 16, 16, 14, stroke=self.colors['green'], stroke_width=1.5)
        builder.add_line(22, 16, 16, 14, stroke=self.colors['green'], stroke_width=1.5)
        
        return builder
    
    def generate_64px(self, builder: SVGBuilder) -> SVGBuilder:
        """64px: Community network"""
        # Central person (larger)
        builder.add_circle(32, 24, 6, fill=self.colors['blue'])
        builder.add_circle(32, 36, 8, fill=self.colors['blue_light'])
        
        # Surrounding people
        people = [(16, 20), (48, 20), (16, 44), (48, 44)]
        
        for x, y in people:
            builder.add_circle(x, y, 4, fill=self.colors['green'])
            builder.add_circle(x, y+8, 5, fill=self.colors['green_dark'], opacity=0.6)
            
            # Connection to center
            builder.add_line(x, y+4, 32, 30, stroke=self.colors['orange'], 
                           stroke_width=1.5, stroke_dasharray="3,2")
        
        return builder
    
    def generate_128px(self, builder: SVGBuilder) -> SVGBuilder:
        """128px: Complete community network"""
        # Central person (moderator/expert)
        builder.add_circle(64, 48, 12, fill=self.colors['blue'])
        builder.add_circle(64, 72, 16, fill=self.colors['blue_light'])
        
        # Badge/star on central person
        for angle in range(0, 360, 72):
            rad = math.radians(angle)
            x = 64 + 8 * math.cos(rad)
            y = 48 + 8 * math.sin(rad)
            builder.add_circle(x, y, 2, fill=self.colors['yellow'])
        
        # Community members in circle
        member_positions = [
            (32, 32, self.colors['green']),
            (96, 32, self.colors['green']),
            (24, 72, self.colors['purple']),
            (104, 72, self.colors['purple']),
            (32, 104, self.colors['orange']),
            (96, 104, self.colors['orange'])
        ]
        
        for x, y, color in member_positions:
            # Head
            builder.add_circle(x, y, 8, fill=color)
            # Body
            builder.add_circle(x, y+16, 10, fill=color, opacity=0.6)
            
            # Connection line to center
            builder.add_line(x, y+8, 64, 60, stroke=self.colors['light_gray'], 
                           stroke_width=2, stroke_dasharray="4,4", opacity=0.7)
        
        # Interaction nodes (messages/discussions)
        interactions = [(48, 32), (80, 32), (48, 88), (80, 88)]
        for ix, iy in interactions:
            builder.add_circle(ix, iy, 4, fill=self.colors['yellow'], opacity=0.8)
        
        # Community circle
        builder.add_circle(64, 64, 56, fill='none', stroke=self.colors['blue_light'], 
                          stroke_width=2, stroke_dasharray="8,8", opacity=0.3)
        
        return builder


class FAI_CheckUpdate(SimpleShapeIcon):
    """Check updates - cloud with down arrow"""
    
    def __init__(self):
        super().__init__(
            name="FAI_CheckUpdate",
            category="Guida",
            description="Verifica aggiornamenti"
        )
    
    def generate_16px(self, builder: SVGBuilder) -> SVGBuilder:
        """16px: Cloud with arrow"""
        # Cloud
        builder.add_path("M 4 8 Q 3 6 5 5 Q 6 4 8 5 Q 10 4 11 6 Q 13 6 12 8 Q 12 9 11 9 L 4 9 Q 3 9 4 8", 
                        fill=self.colors['blue_light'])
        
        # Download arrow
        builder.add_line(8, 10, 8, 13, stroke=self.colors['green'], stroke_width=2)
        builder.add_polygon([(8, 13), (6, 11), (10, 11)], fill=self.colors['green'])
        
        return builder
    
    def generate_32px(self, builder: SVGBuilder) -> SVGBuilder:
        """32px: Cloud with update"""
        # Cloud
        builder.add_path("M 8 16 Q 6 12 10 10 Q 12 8 16 10 Q 20 8 22 12 Q 26 12 24 16 Q 24 18 22 18 L 8 18 Q 6 18 8 16", 
                        fill=self.colors['blue_light'], stroke=self.colors['blue'], stroke_width=1.5)
        
        # Download arrow
        builder.add_line(16, 20, 16, 26, stroke=self.colors['green'], stroke_width=3)
        builder.add_polygon([(16, 26), (13, 23), (19, 23)], fill=self.colors['green'])
        
        # Progress indicator
        builder.add_circle(16, 14, 3, fill=self.colors['yellow'], opacity=0.7)
        
        return builder
    
    def generate_64px(self, builder: SVGBuilder) -> SVGBuilder:
        """64px: Update check system"""
        # Cloud
        builder.add_path("M 16 32 Q 12 24 20 20 Q 24 16 32 20 Q 40 16 44 24 Q 52 24 48 32 Q 48 36 44 36 L 16 36 Q 12 36 16 32", 
                        fill=self.colors['blue_light'], stroke=self.colors['blue'], stroke_width=2)
        
        # Download arrow with glow
        builder.add_line(32, 38, 32, 52, stroke=self.colors['green'], stroke_width=4)
        builder.add_polygon([(32, 52), (27, 47), (37, 47)], fill=self.colors['green'])
        
        # Circular progress
        builder.add_circle(32, 28, 6, fill='none', stroke=self.colors['yellow'], 
                          stroke_width=2, stroke_dasharray="12,6")
        
        # Version badge
        builder.add_rect(40, 20, 12, 6, fill=self.colors['orange'], opacity=0.8, rx=2)
        
        return builder
    
    def generate_128px(self, builder: SVGBuilder) -> SVGBuilder:
        """128px: Complete update system"""
        # Large cloud
        builder.add_path("M 32 64 Q 24 48 40 40 Q 48 32 64 40 Q 80 32 88 48 Q 104 48 96 64 Q 96 72 88 72 L 32 72 Q 24 72 32 64", 
                        fill=self.colors['blue_light'], stroke=self.colors['blue'], stroke_width=4)
        
        # Cloud details
        builder.add_path("M 40 56 Q 48 52 56 56", stroke=self.colors['white'], 
                        stroke_width=2, fill='none', opacity=0.5)
        
        # Large download arrow
        builder.add_line(64, 76, 64, 104, stroke=self.colors['green'], stroke_width=6)
        builder.add_polygon([(64, 104), (56, 96), (72, 96)], fill=self.colors['green'])
        
        # Arrow shaft details
        builder.add_rect(60, 76, 8, 20, fill=self.colors['green_dark'], opacity=0.3)
        
        # Circular progress indicator
        for i in range(12):
            angle = i * 30
            if i < 8:  # 75% complete
                rad = math.radians(angle - 90)
                x1 = 64 + 12 * math.cos(rad)
                y1 = 56 + 12 * math.sin(rad)
                x2 = 64 + 16 * math.cos(rad)
                y2 = 56 + 16 * math.sin(rad)
                builder.add_line(x1, y1, x2, y2, stroke=self.colors['yellow'], stroke_width=3)
        
        # Version info box
        builder.add_rect(80, 40, 32, 16, fill=self.colors['orange'], opacity=0.9, 
                        stroke=self.colors['orange_light'], stroke_width=2, rx=4)
        
        # Version number representation
        builder.add_circle(88, 48, 4, fill=self.colors['white'])
        builder.add_rect(94, 46, 6, 4, fill=self.colors['white'], rx=1)
        builder.add_rect(102, 46, 6, 4, fill=self.colors['white'], rx=1)
        
        # Network indicators (update available)
        for x in [40, 88]:
            builder.add_circle(x, 108, 6, fill=self.colors['green'], opacity=0.7)
            builder.add_circle(x, 108, 3, fill=self.colors['white'])
        
        return builder


class FAI_About(SimpleShapeIcon):
    """About - info "i" in circle"""
    
    def __init__(self):
        super().__init__(
            name="FAI_About",
            category="Guida",
            description="Informazioni About"
        )
    
    def generate_16px(self, builder: SVGBuilder) -> SVGBuilder:
        """16px: Info icon"""
        # Circle
        builder.add_circle(8, 8, 6, fill='none', stroke=self.colors['blue'], stroke_width=2)
        
        # "i" letter
        builder.add_circle(8, 6, 1, fill=self.colors['blue'])
        builder.add_line(8, 8, 8, 11, stroke=self.colors['blue'], stroke_width=2)
        
        return builder
    
    def generate_32px(self, builder: SVGBuilder) -> SVGBuilder:
        """32px: Info badge"""
        # Circle with gradient effect
        builder.add_circle(16, 16, 12, fill=self.colors['blue'], opacity=0.9)
        builder.add_circle(16, 16, 10, fill='none', stroke=self.colors['white'], stroke_width=2)
        
        # "i" letter
        builder.add_circle(16, 12, 2, fill=self.colors['white'])
        builder.add_line(16, 16, 16, 22, stroke=self.colors['white'], stroke_width=3)
        
        return builder
    
    def generate_64px(self, builder: SVGBuilder) -> SVGBuilder:
        """64px: Detailed info icon"""
        # Outer glow
        builder.add_circle(32, 32, 26, fill=self.colors['blue'], opacity=0.2)
        
        # Main circle
        builder.add_circle(32, 32, 22, fill=self.colors['blue'])
        builder.add_circle(32, 32, 20, fill='none', stroke=self.colors['white'], stroke_width=3)
        
        # "i" letter with details
        builder.add_circle(32, 22, 4, fill=self.colors['white'])
        builder.add_line(32, 30, 32, 44, stroke=self.colors['white'], stroke_width=5)
        builder.add_rect(28, 44, 8, 3, fill=self.colors['white'], rx=1)
        
        return builder
    
    def generate_128px(self, builder: SVGBuilder) -> SVGBuilder:
        """128px: Complete about information"""
        # Multiple glow layers
        builder.add_circle(64, 64, 54, fill=self.colors['blue'], opacity=0.1)
        builder.add_circle(64, 64, 48, fill=self.colors['blue'], opacity=0.2)
        
        # Main circle with border
        builder.add_circle(64, 64, 44, fill=self.colors['blue'])
        builder.add_circle(64, 64, 42, fill='none', stroke=self.colors['blue_light'], 
                          stroke_width=2, opacity=0.5)
        builder.add_circle(64, 64, 40, fill='none', stroke=self.colors['white'], stroke_width=4)
        
        # Large "i" letter
        # Dot
        builder.add_circle(64, 44, 8, fill=self.colors['white'])
        
        # Stem
        builder.add_rect(56, 60, 16, 32, fill=self.colors['white'], rx=8)
        
        # Base serif
        builder.add_rect(52, 92, 24, 6, fill=self.colors['white'], rx=3)
        
        # Decorative elements
        for angle in range(0, 360, 45):
            rad = math.radians(angle)
            x = 64 + 52 * math.cos(rad)
            y = 64 + 52 * math.sin(rad)
            builder.add_circle(x, y, 3, fill=self.colors['blue_light'], opacity=0.5)
        
        # Version/copyright indicator at bottom
        builder.add_rect(40, 110, 48, 8, fill=self.colors['blue_light'], opacity=0.3, rx=4)
        
        return builder


# Export all icon classes
__all__ = [
    'FAI_GuidaRapida',
    'FAI_TutorialVideo',
    'FAI_EsempiProgetti',
    'FAI_DocumentazioneAPI',
    'FAI_Community',
    'FAI_CheckUpdate',
    'FAI_About'
]
