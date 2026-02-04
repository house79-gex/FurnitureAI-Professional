"""
Ottimizzazione nesting per pannelli - riduce scarti di materiale
Algoritmo di impacchettamento 2D per taglio pannelli
"""

import math
from collections import namedtuple

Rectangle = namedtuple('Rectangle', ['width', 'height', 'id', 'quantity', 'name'])
Placement = namedtuple('Placement', ['x', 'y', 'width', 'height', 'id', 'name', 'rotated'])

class NestingOptimizer:
    """Ottimizzatore di nesting per pannelli"""
    
    def __init__(self, sheet_width=2800, sheet_height=2070):
        """
        Inizializza l'ottimizzatore
        
        Args:
            sheet_width: Larghezza pannello standard (mm)
            sheet_height: Altezza pannello standard (mm)
        """
        self.sheet_width = sheet_width
        self.sheet_height = sheet_height
        self.blade_width = 4  # Larghezza lama sega (mm)
        self.margin = 10  # Margine sicurezza (mm)
    
    def optimize(self, parts, allow_rotation=True):
        """
        Ottimizza il posizionamento delle parti
        
        Args:
            parts: Lista di dizionari con 'width', 'height', 'quantity', 'name'
            allow_rotation: Permetti rotazione pezzi di 90°
        
        Returns:
            dict: Risultati ottimizzazione con layout e statistiche
        """
        # Converti in rettangoli
        rectangles = []
        for i, part in enumerate(parts):
            for q in range(part.get('quantity', 1)):
                rect = Rectangle(
                    width=part['width'],
                    height=part['height'],
                    id=f"{i}_{q}",
                    quantity=1,
                    name=part.get('name', f"Parte_{i}")
                )
                rectangles.append(rect)
        
        # Ordina per area decrescente (strategia greedy)
        rectangles.sort(key=lambda r: r.width * r.height, reverse=True)
        
        # Esegui nesting con algoritmo guillotine
        sheets = self._guillotine_pack(rectangles, allow_rotation)
        
        # Calcola statistiche
        stats = self._calculate_stats(sheets, rectangles)
        
        return {
            'sheets': sheets,
            'statistics': stats,
            'parts_count': len(rectangles),
            'sheets_count': len(sheets)
        }
    
    def _guillotine_pack(self, rectangles, allow_rotation):
        """
        Algoritmo di packing guillotine
        
        Args:
            rectangles: Lista di Rectangle
            allow_rotation: Permetti rotazione
        
        Returns:
            list: Lista di sheet (pannelli) con placements
        """
        sheets = []
        current_sheet = {
            'id': 0,
            'placements': [],
            'free_rectangles': [
                {
                    'x': self.margin,
                    'y': self.margin,
                    'width': self.sheet_width - 2 * self.margin,
                    'height': self.sheet_height - 2 * self.margin
                }
            ]
        }
        
        for rect in rectangles:
            placed = False
            
            # Prova a piazzare nel foglio corrente
            placement = self._find_placement(rect, current_sheet['free_rectangles'], allow_rotation)
            
            if placement:
                current_sheet['placements'].append(placement)
                self._split_free_rectangle(
                    current_sheet['free_rectangles'],
                    placement
                )
                placed = True
            
            # Se non entra, crea nuovo foglio
            if not placed:
                sheets.append(current_sheet)
                
                current_sheet = {
                    'id': len(sheets),
                    'placements': [],
                    'free_rectangles': [
                        {
                            'x': self.margin,
                            'y': self.margin,
                            'width': self.sheet_width - 2 * self.margin,
                            'height': self.sheet_height - 2 * self.margin
                        }
                    ]
                }
                
                # Riprova sul nuovo foglio
                placement = self._find_placement(rect, current_sheet['free_rectangles'], allow_rotation)
                if placement:
                    current_sheet['placements'].append(placement)
                    self._split_free_rectangle(
                        current_sheet['free_rectangles'],
                        placement
                    )
        
        # Aggiungi l'ultimo foglio
        if current_sheet['placements']:
            sheets.append(current_sheet)
        
        return sheets
    
    def _find_placement(self, rect, free_rects, allow_rotation):
        """
        Trova il miglior posizionamento per un rettangolo
        
        Args:
            rect: Rectangle da piazzare
            free_rects: Lista di rettangoli liberi
            allow_rotation: Permetti rotazione
        
        Returns:
            Placement o None
        """
        best_placement = None
        best_score = float('inf')
        
        for free_rect in free_rects:
            # Prova senza rotazione
            if (rect.width + self.blade_width <= free_rect['width'] and 
                rect.height + self.blade_width <= free_rect['height']):
                
                # Score: preferisci fit più stretto
                score = (free_rect['width'] - rect.width) + (free_rect['height'] - rect.height)
                
                if score < best_score:
                    best_score = score
                    best_placement = Placement(
                        x=free_rect['x'],
                        y=free_rect['y'],
                        width=rect.width,
                        height=rect.height,
                        id=rect.id,
                        name=rect.name,
                        rotated=False
                    )
            
            # Prova con rotazione
            if allow_rotation:
                if (rect.height + self.blade_width <= free_rect['width'] and 
                    rect.width + self.blade_width <= free_rect['height']):
                    
                    score = (free_rect['width'] - rect.height) + (free_rect['height'] - rect.width)
                    
                    if score < best_score:
                        best_score = score
                        best_placement = Placement(
                            x=free_rect['x'],
                            y=free_rect['y'],
                            width=rect.height,  # Ruotato
                            height=rect.width,   # Ruotato
                            id=rect.id,
                            name=rect.name,
                            rotated=True
                        )
        
        return best_placement
    
    def _split_free_rectangle(self, free_rects, placement):
        """
        Divide i rettangoli liberi dopo un piazzamento
        
        Args:
            free_rects: Lista di rettangoli liberi (modificata in place)
            placement: Placement appena effettuato
        """
        new_free_rects = []
        
        for free_rect in free_rects:
            # Controlla se il placement interseca questo rettangolo libero
            if self._intersects(placement, free_rect):
                # Crea nuovi rettangoli dalle parti rimanenti
                
                # Rettangolo a destra
                if placement.x + placement.width + self.blade_width < free_rect['x'] + free_rect['width']:
                    new_free_rects.append({
                        'x': placement.x + placement.width + self.blade_width,
                        'y': free_rect['y'],
                        'width': (free_rect['x'] + free_rect['width']) - (placement.x + placement.width + self.blade_width),
                        'height': free_rect['height']
                    })
                
                # Rettangolo sopra
                if placement.y + placement.height + self.blade_width < free_rect['y'] + free_rect['height']:
                    new_free_rects.append({
                        'x': free_rect['x'],
                        'y': placement.y + placement.height + self.blade_width,
                        'width': free_rect['width'],
                        'height': (free_rect['y'] + free_rect['height']) - (placement.y + placement.height + self.blade_width)
                    })
            else:
                # Non interseca, mantieni il rettangolo libero
                new_free_rects.append(free_rect)
        
        # Sostituisci la lista
        free_rects.clear()
        free_rects.extend(new_free_rects)
    
    def _intersects(self, placement, free_rect):
        """
        Controlla se un placement interseca un rettangolo libero
        
        Args:
            placement: Placement
            free_rect: Dizionario rettangolo libero
        
        Returns:
            bool: True se interseca
        """
        return not (
            placement.x + placement.width <= free_rect['x'] or
            placement.x >= free_rect['x'] + free_rect['width'] or
            placement.y + placement.height <= free_rect['y'] or
            placement.y >= free_rect['y'] + free_rect['height']
        )
    
    def _calculate_stats(self, sheets, rectangles):
        """
        Calcola statistiche di utilizzo
        
        Args:
            sheets: Lista di sheet
            rectangles: Lista di Rectangle
        
        Returns:
            dict: Statistiche
        """
        total_sheet_area = len(sheets) * self.sheet_width * self.sheet_height
        
        used_area = 0
        for rect in rectangles:
            used_area += rect.width * rect.height
        
        efficiency = (used_area / total_sheet_area * 100) if total_sheet_area > 0 else 0
        waste = total_sheet_area - used_area
        
        return {
            'total_sheets': len(sheets),
            'sheet_area_m2': round(self.sheet_width * self.sheet_height / 1000000, 4),
            'total_area_m2': round(total_sheet_area / 1000000, 4),
            'used_area_m2': round(used_area / 1000000, 4),
            'waste_area_m2': round(waste / 1000000, 4),
            'efficiency_percent': round(efficiency, 2),
            'waste_percent': round(100 - efficiency, 2)
        }
