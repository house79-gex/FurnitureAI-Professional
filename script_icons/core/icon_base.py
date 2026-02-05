"""
Icon generation base system
COMPLETE VERSION with all required classes
"""

import os
from pathlib import Path
from typing import Dict, List, Tuple


class IconBase:
    """Base class for icon generation - backward compatibility"""
    
    def __init__(self, size):
        self.size = size
        self.center = size / 2
    
    def _create_svg(self):
        """Create SVG builder"""
        from core.svg_builder import SVGBuilder
        return SVGBuilder(self.size, self.size)


class SimpleShapeIcon(IconBase):
    """Simple shape icon base class"""
    
    def __init__(self, size=None, name=None, category=None, description=None):
        """
        Initialize icon
        
        Args:
            size: Icon size (can be None if set later)
            name: Icon name
            category: Icon category/panel
            description: Icon description
        """
        if size is not None:
            super().__init__(size)
        self.name = name
        self.category = category
        self.description = description
        
        # Standard color palette
        self.colors = {
            # Primary colors
            'blue': '#0696D7',
            'blue_light': '#4AB8E8',
            'blue_dark': '#0566A7',
            
            # Secondary colors
            'green': '#28A745',
            'green_light': '#5CB85C',
            'green_dark': '#1E7A33',
            
            'orange': '#FD7E14',
            'orange_light': '#FFA94D',
            'orange_dark': '#E8590C',
            
            'purple': '#6F42C1',
            'purple_light': '#9370DB',
            'purple_dark': '#5A32A3',
            
            'red': '#DC3545',
            'red_light': '#E57373',
            'red_dark': '#B71C1C',
            
            'yellow': '#FFC107',
            'yellow_light': '#FFD54F',
            'yellow_dark': '#FFA000',
            
            # Grays
            'black': '#000000',
            'dark_gray': '#343A40',
            'medium_gray': '#6C757D',
            'light_gray': '#ADB5BD',
            'very_light_gray': '#E9ECEF',
            'white': '#FFFFFF',
        }
    
    def add_handle(self, builder, x, y, size, style='circle'):
        """Add a furniture handle"""
        if style == 'circle':
            r = max(2, size // 32)
            builder.add_circle(x, y, r, fill=self.colors['dark_gray'])
        elif style == 'bar':
            w = max(4, size // 16)
            h = max(2, size // 64)
            builder.add_rect(x - w//2, y - h//2, w, h, fill=self.colors['dark_gray'], rx=h//2)
    
    def add_ai_brain(self, builder, x, y, r, size):
        """Add an AI brain indicator"""
        builder.add_circle(x, y, r, fill=self.colors['purple'], opacity=0.9)
        
        # Add small nodes
        if size >= 32:
            import math
            for angle in [0, 120, 240]:
                node_x = x + (r * 0.6) * math.cos(math.radians(angle))
                node_y = y + (r * 0.6) * math.sin(math.radians(angle))
                builder.add_circle(node_x, node_y, max(1, r // 4), fill=self.colors['white'])


class IconGenerationSystem:
    """Main system for generating all icons"""
    
    def __init__(self):
        """Initialize the icon generation system"""
        self.sizes = [16, 32, 64, 128]
        self.output_dir = Path('output')
        
        # Import all generators
        self._import_generators()
    
    def _import_generators(self):
        """Import all panel generators"""
        try:
            from generators.design_generator import DesignGenerator
            from generators.components_generator import ComponentsGenerator
            from generators.edita_generator import EditaGenerator
            from generators.hardware_generator import HardwareGenerator
            from generators.lavorazioni_generator import LavorazioniGenerator
            from generators.qualita_generator import QualitaGenerator
            from generators.produzione_generator import ProduzioneGenerator
            from generators.guida_generator import GuidaGenerator
            from generators.impostazioni_generator import ImpostazioniGenerator
            
            self.generators = {
                'Design': DesignGenerator(),
                'Componenti': ComponentsGenerator(),
                'Edita': EditaGenerator(),
                'Hardware': HardwareGenerator(),
                'Lavorazioni': LavorazioniGenerator(),
                'Qualità': QualitaGenerator(),
                'Produzione': ProduzioneGenerator(),
                'Guida & Info': GuidaGenerator(),
                'Impostazioni': ImpostazioniGenerator()
            }
        except ImportError as e:
            print(f"Warning: Could not import all generators: {e}")
            self.generators = {}
    
    def generate_all(self) -> Dict:
        """
        Generate all icons for all panels
        
        Returns:
            Dictionary with generation results
        """
        results = {
            'icons': {},
            'panels': {}
        }
        
        for panel_name, generator in self.generators.items():
            print(f"\n📂 {panel_name} Panel ({len(generator.get_icons())} icons)")
            print("-" * 60)
            
            panel_results = {
                'total': len(generator.get_icons()),
                'successful': 0,
                'failed': 0,
                'icons': []
            }
            
            for icon_name, icon_func in generator.get_icons().items():
                icon_results = self._generate_icon(icon_name, icon_func, generator)
                results['icons'][icon_name] = icon_results
                panel_results['icons'].append(icon_name)
                
                if all(icon_results['sizes'].values()):
                    panel_results['successful'] += 1
                elif any(icon_results['sizes'].values()):
                    panel_results['successful'] += 0.5
                    panel_results['failed'] += 0.5
                else:
                    panel_results['failed'] += 1
            
            results['panels'][panel_name] = panel_results
        
        return results
    
    def _generate_icon(self, icon_name: str, icon_func, generator) -> Dict:
        """
        Generate a single icon at all sizes
        FIXED: Saves PNG with size in filename to flat directory
        
        Args:
            icon_name: Name of the icon
            icon_func: Function to generate the icon
            generator: Generator instance
            
        Returns:
            Dictionary with generation results for this icon
        """
        results = {
            'name': icon_name,
            'sizes': {},
            'errors': {}
        }
        
        svg_dir = self.output_dir / 'svg'
        png_dir = self.output_dir / 'png'  # FLAT: No size subdirectories
        
        svg_dir.mkdir(parents=True, exist_ok=True)
        png_dir.mkdir(parents=True, exist_ok=True)
        
        for size in self.sizes:
            try:
                # Generate SVG
                svg_content = icon_func(generator, size)
                
                # Save SVG with size in filename
                svg_path = svg_dir / f"{icon_name}_{size}.svg"
                with open(svg_path, 'w', encoding='utf-8') as f:
                    f.write(svg_content)
                
                # Convert to PNG - FLAT OUTPUT with size in filename
                png_path = png_dir / f"{icon_name}_{size}.png"
                
                if self._convert_to_png(str(svg_path), str(png_path), size):
                    results['sizes'][size] = True
                    print(f"  ✓ Generated {icon_name} at {size}×{size}px")
                else:
                    results['sizes'][size] = True  # SVG succeeded even if PNG failed
                    print(f"  ✓ Generated {icon_name} at {size}×{size}px (SVG only)")
                
            except Exception as e:
                results['sizes'][size] = False
                results['errors'][size] = str(e)
                print(f"  ✗ Error generating {icon_name} at {size}px: {e}")
        
        return results
    
    def _convert_to_png(self, svg_path: str, png_path: str, size: int) -> bool:
        """
        Convert SVG to PNG
        
        Args:
            svg_path: Path to SVG file
            png_path: Path to output PNG file
            size: PNG size
            
        Returns:
            True if conversion succeeded, False otherwise
        """
        try:
            import cairosvg
            cairosvg.svg2png(
                url=svg_path,
                write_to=png_path,
                output_width=size,
                output_height=size
            )
            return True
        except ImportError:
            # Try alternative converter
            try:
                from svglib.svglib import svg2rlg
                from reportlab.graphics import renderPM
                
                drawing = svg2rlg(svg_path)
                renderPM.drawToFile(drawing, png_path, fmt='PNG', dpi=72)
                return True
            except ImportError:
                # No PNG converter available
                return False
        except Exception as e:
            # Conversion failed but don't print error (already handled upstream)
            return False


class IconGenerator:
    """Base class for icon generators"""
    
    def __init__(self):
        """Initialize generator"""
        pass
    
    def get_icons(self) -> Dict:
        """
        Get dictionary of icon names to generation functions
        Must be implemented by subclasses
        
        Returns:
            Dictionary mapping icon names to generator functions
        """
        raise NotImplementedError("Subclasses must implement get_icons()")
    
    def _create_svg(self, size: int) -> 'SVGBuilder':
        """
        Create SVG builder for given size
        
        Args:
            size: Icon size
            
        Returns:
            SVGBuilder instance
        """
        from core.svg_builder import SVGBuilder
        return SVGBuilder(size, size)
    
    def _get_scaled_value(self, base_value: float, size: int, 
                         base_size: int = 32) -> float:
        """
        Get value scaled for icon size
        
        Args:
            base_value: Value at base size
            size: Target size
            base_size: Base size (default 32)
            
        Returns:
            Scaled value
        """
        return base_value * (size / base_size)
    
    def _get_stroke_width(self, size: int) -> float:
        """
        Get appropriate stroke width for size
        
        Args:
            size: Icon size
            
        Returns:
            Stroke width
        """
        if size <= 16:
            return 2
        elif size <= 32:
            return 1.5
        elif size <= 64:
            return 1
        else:
            return 0.75
