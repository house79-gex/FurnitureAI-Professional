"""
Giunzioni a spinotto (dowel joints) per assemblaggio mobili
Implementa spinotti diametro 8mm standard per falegnameria
"""

import adsk.core
import adsk.fusion
import math

class DowelJoints:
    """Generatore di giunzioni a spinotto"""
    
    def __init__(self, component):
        """
        Inizializza il generatore
        
        Args:
            component: Componente Fusion
        """
        self.component = component
        self.dowel_diameter = 8.0   # Diametro spinotto (mm)
        self.dowel_length = 35.0    # Lunghezza spinotto (mm)
        self.hole_depth = 20.0      # Profondità foro (mm)
        self.tolerance = 0.1        # Tolleranza foro (mm)
    
    def add_dowel_joint(self, body1, body2, params):
        """
        Crea una giunzione a spinotti tra due corpi
        
        Args:
            body1: Primo BRepBody
            body2: Secondo BRepBody
            params: Dizionario parametri
                - joint_type: Tipo ('corner', 'edge', 'face')
                - dowel_count: Numero spinotti (default 2)
                - spacing: Spaziatura spinotti (mm, default 50)
                - offset: Offset dal bordo (mm, default 25)
        
        Returns:
            dict: Informazioni giunzione con posizioni fori
        """
        joint_type = params.get('joint_type', 'corner')
        dowel_count = params.get('dowel_count', 2)
        spacing = params.get('spacing', 50)
        offset = params.get('offset', 25)
        
        joint_info = {
            'type': joint_type,
            'dowel_count': dowel_count,
            'body1_holes': [],
            'body2_holes': []
        }
        
        if joint_type == 'corner':
            # Giunzione ad angolo (es. fianco + fondo)
            positions = self._calculate_corner_positions(body1, body2, dowel_count, spacing, offset)
            
            for pos in positions:
                hole1 = self._create_dowel_hole(body1, pos, 'vertical')
                hole2 = self._create_dowel_hole(body2, pos, 'horizontal')
                
                if hole1:
                    joint_info['body1_holes'].append(hole1)
                if hole2:
                    joint_info['body2_holes'].append(hole2)
        
        elif joint_type == 'edge':
            # Giunzione su bordo (es. ripiano + fianco)
            positions = self._calculate_edge_positions(body1, body2, dowel_count, spacing)
            
            for pos in positions:
                hole1 = self._create_dowel_hole(body1, pos, 'horizontal')
                hole2 = self._create_dowel_hole(body2, pos, 'horizontal')
                
                if hole1:
                    joint_info['body1_holes'].append(hole1)
                if hole2:
                    joint_info['body2_holes'].append(hole2)
        
        return joint_info
    
    def add_dowel_holes_pattern(self, body, params):
        """
        Aggiunge un pattern di fori per spinotti
        
        Args:
            body: BRepBody
            params: Dizionario parametri
                - face: Faccia su cui praticare fori
                - positions: Lista di coordinate [(x, y), ...]
                - direction: Direzione foratura ('x', 'y', 'z')
        
        Returns:
            list: Lista di feature fori
        """
        positions = params.get('positions', [])
        direction = params.get('direction', 'z')
        
        holes = []
        
        for pos in positions:
            hole = self._create_dowel_hole_at_position(body, pos, direction)
            if hole:
                holes.append(hole)
        
        return holes
    
    def _calculate_corner_positions(self, body1, body2, count, spacing, offset):
        """
        Calcola posizioni spinotti per giunzione ad angolo
        
        Args:
            body1, body2: Corpi da unire
            count: Numero spinotti
            spacing: Spaziatura
            offset: Offset dal bordo
        
        Returns:
            list: Lista di posizioni
        """
        positions = []
        
        # Ottieni dimensioni
        bbox1 = body1.boundingBox
        width1 = (bbox1.maxPoint.x - bbox1.minPoint.x) * 10  # cm to mm
        
        # Calcola posizioni distribuite
        if count == 1:
            positions.append({'x': width1 / 2, 'y': offset, 'z': 0})
        else:
            start = offset
            end = width1 - offset
            step = (end - start) / (count - 1) if count > 1 else 0
            
            for i in range(count):
                positions.append({
                    'x': start + (step * i),
                    'y': offset,
                    'z': 0
                })
        
        return positions
    
    def _calculate_edge_positions(self, body1, body2, count, spacing):
        """
        Calcola posizioni spinotti per giunzione su bordo
        
        Args:
            body1, body2: Corpi da unire
            count: Numero spinotti
            spacing: Spaziatura
        
        Returns:
            list: Lista di posizioni
        """
        positions = []
        
        # Semplificazione: distribuzione uniforme
        bbox1 = body1.boundingBox
        length = (bbox1.maxPoint.x - bbox1.minPoint.x) * 10
        
        if count == 1:
            positions.append({'x': length / 2, 'y': 0, 'z': 0})
        else:
            margin = 30  # mm dal bordo
            available = length - 2 * margin
            step = available / (count - 1) if count > 1 else 0
            
            for i in range(count):
                positions.append({
                    'x': margin + (step * i),
                    'y': 0,
                    'z': 0
                })
        
        return positions
    
    def _create_dowel_hole(self, body, position, direction):
        """
        Crea un foro per spinotto
        
        Args:
            body: BRepBody
            position: Dizionario con x, y, z
            direction: Direzione ('horizontal', 'vertical')
        
        Returns:
            Feature o None
        """
        try:
            holes = self.component.features.holeFeatures
            
            # Determina punto e vettore direzione
            point = adsk.core.Point3D.create(
                position['x'] / 10.0,
                position['y'] / 10.0,
                position['z'] / 10.0
            )
            
            if direction == 'vertical':
                dir_vector = adsk.core.Vector3D.create(0, 0, 1)
            else:  # horizontal
                dir_vector = adsk.core.Vector3D.create(0, 1, 0)
            
            # Diametro con tolleranza
            actual_diameter = self.dowel_diameter + self.tolerance
            
            hole_input = holes.createSimpleInput(
                adsk.core.ValueInput.createByReal(actual_diameter / 20.0)
            )
            hole_input.setPositionByPoint(point)
            hole_input.setDistanceExtent(
                adsk.core.ValueInput.createByReal(self.hole_depth / 10.0)
            )
            hole_input.setDirection(dir_vector)
            
            hole_feature = holes.add(hole_input)
            return hole_feature
        except:
            return None
    
    def _create_dowel_hole_at_position(self, body, position, direction):
        """
        Crea foro a posizione specifica
        
        Args:
            body: BRepBody
            position: Tupla (x, y) in mm
            direction: Direzione ('x', 'y', 'z')
        
        Returns:
            Feature o None
        """
        try:
            holes = self.component.features.holeFeatures
            
            # Crea punto 3D
            if direction == 'z':
                point = adsk.core.Point3D.create(
                    position[0] / 10.0,
                    position[1] / 10.0,
                    0
                )
                dir_vector = adsk.core.Vector3D.create(0, 0, 1)
            elif direction == 'y':
                point = adsk.core.Point3D.create(
                    position[0] / 10.0,
                    0,
                    position[1] / 10.0
                )
                dir_vector = adsk.core.Vector3D.create(0, 1, 0)
            else:  # 'x'
                point = adsk.core.Point3D.create(
                    0,
                    position[0] / 10.0,
                    position[1] / 10.0
                )
                dir_vector = adsk.core.Vector3D.create(1, 0, 0)
            
            actual_diameter = self.dowel_diameter + self.tolerance
            
            hole_input = holes.createSimpleInput(
                adsk.core.ValueInput.createByReal(actual_diameter / 20.0)
            )
            hole_input.setPositionByPoint(point)
            hole_input.setDistanceExtent(
                adsk.core.ValueInput.createByReal(self.hole_depth / 10.0)
            )
            hole_input.setDirection(dir_vector)
            
            hole_feature = holes.add(hole_input)
            return hole_feature
        except:
            return None
    
    def create_dowel_visualization(self, joint_info):
        """
        Crea una visualizzazione 3D degli spinotti
        
        Args:
            joint_info: Dizionario con info giunzione
        
        Returns:
            list: Lista di corpi spinotti creati
        """
        dowels = []
        
        try:
            # Per ogni coppia di fori, crea un cilindro spinotto
            for i in range(min(len(joint_info['body1_holes']), len(joint_info['body2_holes']))):
                # Crea cilindro
                sketches = self.component.sketches
                xy_plane = self.component.xYConstructionPlane
                
                sketch = sketches.add(xy_plane)
                circles = sketch.sketchCurves.sketchCircles
                
                # Centro in origine (sarà spostato dopo)
                circle = circles.addByCenterRadius(
                    adsk.core.Point3D.create(0, 0, 0),
                    self.dowel_diameter / 20.0
                )
                
                # Estrudi
                extrudes = self.component.features.extrudeFeatures
                extrude_input = extrudes.createInput(
                    sketch.profiles.item(0),
                    adsk.fusion.FeatureOperations.NewBodyFeatureOperation
                )
                
                distance = adsk.core.ValueInput.createByReal(self.dowel_length / 10.0)
                extrude_input.setDistanceExtent(False, distance)
                
                dowel = extrudes.add(extrude_input)
                dowel.bodies.item(0).name = f"Spinotto_{i+1}"
                
                dowels.append(dowel.bodies.item(0))
        except:
            pass
        
        return dowels
