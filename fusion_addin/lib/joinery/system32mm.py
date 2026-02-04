"""
Sistema 32mm per foratura standard mobili
Implementa lo standard industriale per fori di mensole, cerniere e connettori
"""

import adsk.core
import adsk.fusion
import math

class System32mm:
    """Gestore del sistema di foratura 32mm standard"""
    
    def __init__(self, component):
        """
        Inizializza il sistema 32mm
        
        Args:
            component: Componente Fusion su cui operare
        """
        self.component = component
        self.hole_diameter = 5.0  # Diametro foro standard (mm)
        self.hole_depth = 12.0    # Profondità foro standard (mm)
        self.spacing = 32.0       # Spaziatura standard (mm)
        self.edge_offset = 37.0   # Distanza dal bordo (mm)
    
    def add_shelf_holes(self, body, params):
        """
        Aggiunge fori per mensole regolabili
        
        Args:
            body: BRepBody su cui praticare i fori
            params: Dizionario parametri
                - start_height: Altezza inizio fori (mm)
                - end_height: Altezza fine fori (mm)
                - rows: Numero di file (1 o 2, default 1)
                - side: Lato ('left', 'right', 'both', default 'both')
        
        Returns:
            list: Lista di feature fori create
        """
        start_height = params.get('start_height', 100)
        end_height = params.get('end_height', 600)
        rows = params.get('rows', 1)
        side = params.get('side', 'both')
        
        # Calcola numero di fori
        height_range = end_height - start_height
        hole_count = int(height_range / self.spacing) + 1
        
        holes = []
        
        # Determina quali lati forare
        sides_to_drill = []
        if side in ['left', 'both']:
            sides_to_drill.append('left')
        if side in ['right', 'both']:
            sides_to_drill.append('right')
        
        for drill_side in sides_to_drill:
            for row in range(rows):
                row_offset = self.edge_offset if row == 0 else self.edge_offset + 32
                
                for i in range(hole_count):
                    z_position = start_height + (i * self.spacing)
                    
                    hole = self._create_shelf_hole(
                        body,
                        drill_side,
                        row_offset,
                        z_position
                    )
                    if hole:
                        holes.append(hole)
        
        return holes
    
    def add_hinge_holes(self, body, params):
        """
        Aggiunge fori per cerniere (sistema Blum Clip Top)
        
        Args:
            body: BRepBody su cui praticare i fori
            params: Dizionario parametri
                - hinge_count: Numero cerniere (default 2)
                - door_height: Altezza anta (mm)
                - hole_type: Tipo foro ('cup', 'mounting', 'both', default 'both')
        
        Returns:
            list: Lista di feature fori create
        """
        hinge_count = params.get('hinge_count', 2)
        door_height = params.get('door_height', 700)
        hole_type = params.get('hole_type', 'both')
        
        holes = []
        
        # Calcola posizioni cerniere (distribuzione uniforme)
        if hinge_count == 2:
            positions = [door_height * 0.15, door_height * 0.85]
        elif hinge_count == 3:
            positions = [door_height * 0.1, door_height * 0.5, door_height * 0.9]
        else:
            spacing = door_height / (hinge_count + 1)
            positions = [spacing * (i + 1) for i in range(hinge_count)]
        
        for pos in positions:
            if hole_type in ['cup', 'both']:
                # Foro tazza cerniera: diametro 35mm, profondità 12mm
                cup_hole = self._create_hinge_cup_hole(body, pos)
                if cup_hole:
                    holes.append(cup_hole)
            
            if hole_type in ['mounting', 'both']:
                # Fori di fissaggio: diametro 5mm, sistema 32mm
                mounting_holes = self._create_hinge_mounting_holes(body, pos)
                holes.extend(mounting_holes)
        
        return holes
    
    def add_connector_holes(self, body, params):
        """
        Aggiunge fori per connettori minifix/rafix
        
        Args:
            body: BRepBody su cui praticare i fori
            params: Dizionario parametri
                - positions: Lista di posizioni Z (mm)
                - connector_type: Tipo ('minifix', 'rafix', default 'minifix')
                - side: Lato ('top', 'bottom', 'left', 'right')
        
        Returns:
            list: Lista di feature fori create
        """
        positions = params.get('positions', [])
        connector_type = params.get('connector_type', 'minifix')
        side = params.get('side', 'top')
        
        holes = []
        
        for pos in positions:
            if connector_type == 'minifix':
                # Minifix: foro diametro 5mm per spina + foro diametro 10mm per dado
                hole = self._create_minifix_hole(body, side, pos)
            elif connector_type == 'rafix':
                # Rafix: foro diametro 5mm + foro diametro 8mm
                hole = self._create_rafix_hole(body, side, pos)
            else:
                hole = None
            
            if hole:
                holes.append(hole)
        
        return holes
    
    def _create_shelf_hole(self, body, side, y_offset, z_position):
        """
        Crea un singolo foro per mensola
        
        Args:
            body: BRepBody
            side: Lato ('left' o 'right')
            y_offset: Offset Y dal bordo (mm)
            z_position: Posizione Z (mm)
        
        Returns:
            Feature creata o None
        """
        try:
            # Ottieni dimensioni corpo
            bbox = body.boundingBox
            thickness = (bbox.maxPoint.x - bbox.minPoint.x) * 10  # cm to mm
            
            # Determina posizione X
            if side == 'left':
                x_position = 0
                direction = adsk.core.Vector3D.create(1, 0, 0)  # Fora verso destra
            else:
                x_position = thickness
                direction = adsk.core.Vector3D.create(-1, 0, 0)  # Fora verso sinistra
            
            # Crea foro
            holes = self.component.features.holeFeatures
            
            # Punto di inizio
            point = adsk.core.Point3D.create(
                x_position / 10.0,
                y_offset / 10.0,
                z_position / 10.0
            )
            
            # Crea input per foro
            hole_input = holes.createSimpleInput(adsk.core.ValueInput.createByReal(self.hole_diameter / 20.0))
            hole_input.setPositionByPoint(point)
            hole_input.setDistanceExtent(adsk.core.ValueInput.createByReal(self.hole_depth / 10.0))
            hole_input.setDirection(direction)
            
            hole_feature = holes.add(hole_input)
            return hole_feature
        except:
            return None
    
    def _create_hinge_cup_hole(self, body, z_position):
        """
        Crea foro tazza cerniera (35mm diametro)
        
        Args:
            body: BRepBody
            z_position: Posizione Z (mm)
        
        Returns:
            Feature o None
        """
        try:
            holes = self.component.features.holeFeatures
            
            # Foro da bordo anta, centrato
            point = adsk.core.Point3D.create(
                0.5,  # Centro spessore (circa)
                0,
                z_position / 10.0
            )
            
            direction = adsk.core.Vector3D.create(0, 1, 0)  # Fora in profondità
            
            hole_input = holes.createSimpleInput(adsk.core.ValueInput.createByReal(35.0 / 20.0))
            hole_input.setPositionByPoint(point)
            hole_input.setDistanceExtent(adsk.core.ValueInput.createByReal(12.0 / 10.0))
            hole_input.setDirection(direction)
            
            hole_feature = holes.add(hole_input)
            return hole_feature
        except:
            return None
    
    def _create_hinge_mounting_holes(self, body, z_position):
        """
        Crea fori di montaggio cerniera (5mm diametro, sistema 32mm)
        
        Args:
            body: BRepBody
            z_position: Posizione Z centrale (mm)
        
        Returns:
            list: Lista di feature
        """
        holes_features = []
        
        # Due fori distanti 32mm (o 48mm per alcuni modelli)
        offsets = [-16, 16]  # -16mm e +16mm dal centro
        
        for offset in offsets:
            try:
                holes = self.component.features.holeFeatures
                
                point = adsk.core.Point3D.create(
                    0.5,
                    0.5,
                    (z_position + offset) / 10.0
                )
                
                direction = adsk.core.Vector3D.create(1, 0, 0)
                
                hole_input = holes.createSimpleInput(adsk.core.ValueInput.createByReal(5.0 / 20.0))
                hole_input.setPositionByPoint(point)
                hole_input.setDistanceExtent(adsk.core.ValueInput.createByReal(self.hole_depth / 10.0))
                hole_input.setDirection(direction)
                
                hole_feature = holes.add(hole_input)
                holes_features.append(hole_feature)
            except:
                pass
        
        return holes_features
    
    def _create_minifix_hole(self, body, side, position):
        """
        Crea foro per connettore minifix
        
        Args:
            body: BRepBody
            side: Lato di foratura
            position: Posizione (mm)
        
        Returns:
            Feature o None
        """
        # Semplificazione: crea un foro standard da 5mm
        try:
            holes = self.component.features.holeFeatures
            
            # Determina punto e direzione in base al lato
            if side == 'top':
                point = adsk.core.Point3D.create(position / 10.0, 0, 1.0)
                direction = adsk.core.Vector3D.create(0, 0, -1)
            elif side == 'bottom':
                point = adsk.core.Point3D.create(position / 10.0, 0, 0)
                direction = adsk.core.Vector3D.create(0, 0, 1)
            else:
                return None
            
            hole_input = holes.createSimpleInput(adsk.core.ValueInput.createByReal(5.0 / 20.0))
            hole_input.setPositionByPoint(point)
            hole_input.setDistanceExtent(adsk.core.ValueInput.createByReal(self.hole_depth / 10.0))
            hole_input.setDirection(direction)
            
            hole_feature = holes.add(hole_input)
            return hole_feature
        except:
            return None
    
    def _create_rafix_hole(self, body, side, position):
        """
        Crea foro per connettore rafix
        
        Args:
            body: BRepBody
            side: Lato di foratura
            position: Posizione (mm)
        
        Returns:
            Feature o None
        """
        # Similar to minifix, simplified
        return self._create_minifix_hole(body, side, position)
    
    def calculate_hole_positions(self, start, end, spacing=None):
        """
        Calcola posizioni fori con spaziatura standard
        
        Args:
            start: Posizione iniziale (mm)
            end: Posizione finale (mm)
            spacing: Spaziatura (mm, default self.spacing)
        
        Returns:
            list: Lista di posizioni (mm)
        """
        if spacing is None:
            spacing = self.spacing
        
        positions = []
        current = start
        
        while current <= end:
            positions.append(current)
            current += spacing
        
        return positions
