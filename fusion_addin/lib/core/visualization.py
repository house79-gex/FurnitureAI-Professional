"""
Visualizzatore di nesting per preview layout pannelli
Genera rappresentazioni grafiche del layout ottimizzato
"""

import math

class NestingVisualizer:
    """Visualizzatore di layout nesting"""
    
    def __init__(self, sheet_width=2800, sheet_height=2070):
        """
        Inizializza il visualizzatore
        
        Args:
            sheet_width: Larghezza pannello (mm)
            sheet_height: Altezza pannello (mm)
        """
        self.sheet_width = sheet_width
        self.sheet_height = sheet_height
    
    def create_svg(self, nesting_result, output_path):
        """
        Crea un file SVG con la visualizzazione del nesting
        
        Args:
            nesting_result: Risultato da NestingOptimizer.optimize()
            output_path: Path del file SVG di output
        
        Returns:
            bool: Successo operazione
        """
        try:
            scale = 0.2  # Scala per visualizzazione (mm to px)
            margin = 50  # Margine SVG
            
            sheets = nesting_result['sheets']
            
            # Calcola dimensioni totali SVG
            svg_width = int(self.sheet_width * scale + 2 * margin)
            svg_height = int((self.sheet_height * scale + margin) * len(sheets) + margin)
            
            # Genera SVG
            svg_content = self._generate_svg_header(svg_width, svg_height)
            
            # Aggiungi ogni foglio
            y_offset = margin
            for sheet in sheets:
                svg_content += self._generate_sheet_svg(
                    sheet,
                    margin,
                    y_offset,
                    scale
                )
                y_offset += self.sheet_height * scale + margin
            
            svg_content += '</svg>'
            
            # Salva file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(svg_content)
            
            return True
        except Exception as e:
            print(f"❌ Errore creazione SVG: {e}")
            return False
    
    def _generate_svg_header(self, width, height):
        """Genera header SVG"""
        return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
<defs>
    <style>
        .sheet {{ fill: #f0f0f0; stroke: #333; stroke-width: 2; }}
        .part {{ fill: #4CAF50; stroke: #2E7D32; stroke-width: 1; opacity: 0.8; }}
        .part-rotated {{ fill: #2196F3; stroke: #1565C0; stroke-width: 1; opacity: 0.8; }}
        .text {{ font-family: Arial; font-size: 10px; fill: #000; }}
        .label {{ font-family: Arial; font-size: 12px; font-weight: bold; fill: #333; }}
    </style>
</defs>
'''
    
    def _generate_sheet_svg(self, sheet, x_offset, y_offset, scale):
        """
        Genera SVG per un singolo foglio
        
        Args:
            sheet: Dizionario sheet dal nesting
            x_offset: Offset X (px)
            y_offset: Offset Y (px)
            scale: Scala mm to px
        
        Returns:
            str: Contenuto SVG
        """
        svg = f'<g id="sheet_{sheet["id"]}">\n'
        
        # Rettangolo foglio
        svg += f'  <rect class="sheet" x="{x_offset}" y="{y_offset}" '
        svg += f'width="{self.sheet_width * scale}" height="{self.sheet_height * scale}" />\n'
        
        # Label foglio
        svg += f'  <text class="label" x="{x_offset + 10}" y="{y_offset + 20}">'
        svg += f'Pannello {sheet["id"] + 1}</text>\n'
        
        # Parti piazzate
        for placement in sheet['placements']:
            part_class = 'part-rotated' if placement.rotated else 'part'
            
            x = x_offset + placement.x * scale
            y = y_offset + placement.y * scale
            w = placement.width * scale
            h = placement.height * scale
            
            # Rettangolo parte
            svg += f'  <rect class="{part_class}" x="{x}" y="{y}" '
            svg += f'width="{w}" height="{h}" />\n'
            
            # Dimensioni
            dim_text = f'{int(placement.width)}x{int(placement.height)}'
            if placement.rotated:
                dim_text += ' ↻'
            
            # Centra il testo
            text_x = x + w / 2
            text_y = y + h / 2
            
            svg += f'  <text class="text" x="{text_x}" y="{text_y}" '
            svg += f'text-anchor="middle" dominant-baseline="middle">{dim_text}</text>\n'
        
        svg += '</g>\n'
        return svg
    
    def generate_text_report(self, nesting_result):
        """
        Genera report testuale del nesting
        
        Args:
            nesting_result: Risultato da NestingOptimizer.optimize()
        
        Returns:
            str: Report formattato
        """
        report = []
        report.append("=" * 60)
        report.append("REPORT OTTIMIZZAZIONE NESTING")
        report.append("=" * 60)
        report.append("")
        
        stats = nesting_result['statistics']
        
        report.append("STATISTICHE:")
        report.append(f"  Pannelli utilizzati: {stats['total_sheets']}")
        report.append(f"  Area pannello singolo: {stats['sheet_area_m2']} m²")
        report.append(f"  Area totale disponibile: {stats['total_area_m2']} m²")
        report.append(f"  Area utilizzata: {stats['used_area_m2']} m²")
        report.append(f"  Area scarto: {stats['waste_area_m2']} m²")
        report.append(f"  Efficienza: {stats['efficiency_percent']}%")
        report.append(f"  Scarto: {stats['waste_percent']}%")
        report.append("")
        
        # Dettaglio per pannello
        for sheet in nesting_result['sheets']:
            report.append(f"PANNELLO {sheet['id'] + 1}:")
            report.append(f"  Parti piazzate: {len(sheet['placements'])}")
            
            for i, placement in enumerate(sheet['placements'], 1):
                rotated_str = " (ruotato)" if placement.rotated else ""
                report.append(f"    {i}. {placement.name}: {int(placement.width)}x{int(placement.height)} mm{rotated_str}")
                report.append(f"       Posizione: ({int(placement.x)}, {int(placement.y)}) mm")
            
            report.append("")
        
        report.append("=" * 60)
        
        return '\n'.join(report)
    
    def export_cut_instructions(self, nesting_result, output_path):
        """
        Esporta istruzioni di taglio in formato testo
        
        Args:
            nesting_result: Risultato nesting
            output_path: Path file output
        
        Returns:
            bool: Successo
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("ISTRUZIONI DI TAGLIO - FurnitureAI Professional\n")
                f.write("=" * 60 + "\n\n")
                
                for sheet in nesting_result['sheets']:
                    f.write(f"PANNELLO #{sheet['id'] + 1}\n")
                    f.write("-" * 60 + "\n")
                    
                    # Ordina per Y poi X (taglia dal basso verso l'alto)
                    placements = sorted(sheet['placements'], key=lambda p: (p.y, p.x))
                    
                    for i, placement in enumerate(placements, 1):
                        f.write(f"\nTaglio #{i}:\n")
                        f.write(f"  Nome: {placement.name}\n")
                        f.write(f"  Dimensioni: {int(placement.width)} x {int(placement.height)} mm\n")
                        if placement.rotated:
                            f.write(f"  ⚠️  RUOTATO 90°\n")
                        f.write(f"  Posizione: X={int(placement.x)} mm, Y={int(placement.y)} mm\n")
                    
                    f.write("\n" + "=" * 60 + "\n\n")
            
            return True
        except Exception as e:
            print(f"❌ Errore export istruzioni: {e}")
            return False
