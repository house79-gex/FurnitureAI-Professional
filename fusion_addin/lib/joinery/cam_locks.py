"""
Connettori a camma (cam locks) tipo Rafix/Minifix
Sistema di connessione rapida per mobili smontabili
"""

import adsk.core
import adsk.fusion

class CamLocks:
    """Generatore di preparazioni per connettori a camma"""
    
    def __init__(self, component):
        """
        Inizializza il generatore
        
        Args:
            component: Componente Fusion
        """
        self.component = component
        
        # Specifiche Rafix (standard Hafele)
        self.rafix_cam_diameter = 15.0      # Diametro camma (mm)
        self.rafix_cam_depth = 11.5         # Profondità camma (mm)
        self.rafix_pin_diameter = 5.0       # Diametro spina (mm)
        self.rafix_pin_depth = 34.0         # Profondità spina (mm)
        
        # Specifiche Minifix (standard Hafele)
        self.minifix_housing_diameter = 10.0  # Diametro alloggiamento (mm)
        self.minifix_housing_depth = 12.5     # Profondità alloggiamento (mm)
        self.minifix_pin_diameter = 5.0       # Diametro spina (mm)
        self.minifix_pin_depth = 13.0         # Profondità spina (mm)
    
    def add_rafix_connection(self, body_with_cam, body_with_pin, params):
        """
        Crea una connessione Rafix completa
        
        Args:
            body_with_cam: Corpo che riceverà la camma
            body_with_pin: Corpo che riceverà la spina
            params: Dizionario parametri
                - position: Posizione connettore (mm)
                - orientation: Orientamento ('horizontal', 'vertical')
        
        Returns:
            dict: Informazioni connessione
        """
        position = params.get('position', {'x': 50, 'y': 0, 'z': 50})
        orientation = params.get('orientation', 'horizontal')
        
        connection_info = {
            'type': 'rafix',
            'position': position,
            'cam_hole': None,
            'pin_hole': None
        }
        
        # Crea foro per camma
        cam_hole = self._create_rafix_cam_hole(body_with_cam, position, orientation)
        connection_info['cam_hole'] = cam_hole
        
        # Crea foro per spina
        pin_hole = self._create_rafix_pin_hole(body_with_pin, position, orientation)
        connection_info['pin_hole'] = pin_hole
        
        return connection_info
    
    def add_minifix_connection(self, body_with_housing, body_with_pin, params):
        """
        Crea una connessione Minifix completa
        
        Args:
            body_with_housing: Corpo che riceverà l'alloggiamento
            body_with_pin: Corpo che riceverà la spina
            params: Dizionario parametri
                - position: Posizione connettore (mm)
                - orientation: Orientamento
        
        Returns:
            dict: Informazioni connessione
        """
        position = params.get('position', {'x': 50, 'y': 0, 'z': 50})
        orientation = params.get('orientation', 'horizontal')
        
        connection_info = {
            'type': 'minifix',
            'position': position,
            'housing_hole': None,
            'pin_hole': None
        }
        
        # Crea foro per alloggiamento
        housing_hole = self._create_minifix_housing_hole(body_with_housing, position, orientation)
        connection_info['housing_hole'] = housing_hole
        
        # Crea foro per spina
        pin_hole = self._create_minifix_pin_hole(body_with_pin, position, orientation)
        connection_info['pin_hole'] = pin_hole
        
        return connection_info
    
    def add_rafix_pattern(self, body_cam, body_pin, params):
        """
        Aggiunge un pattern di connettori Rafix
        
        Args:
            body_cam: Corpo per camme
            body_pin: Corpo per spine
            params: Dizionario parametri
                - count: Numero connettori
                - spacing: Spaziatura (mm)
                - start_position: Posizione iniziale (mm)
                - orientation: Orientamento
        
        Returns:
            list: Lista di connessioni create
        """
        count = params.get('count', 2)
        spacing = params.get('spacing', 100)
        start_position = params.get('start_position', {'x': 50, 'y': 0, 'z': 50})
        orientation = params.get('orientation', 'horizontal')
        
        connections = []
        
        for i in range(count):
            # Calcola posizione
            if orientation == 'horizontal':
                position = {
                    'x': start_position['x'] + (i * spacing),
                    'y': start_position['y'],
                    'z': start_position['z']
                }
            else:  # vertical
                position = {
                    'x': start_position['x'],
                    'y': start_position['y'],
                    'z': start_position['z'] + (i * spacing)
                }
            
            # Crea connessione
            connection = self.add_rafix_connection(
                body_cam,
                body_pin,
                {'position': position, 'orientation': orientation}
            )
            connections.append(connection)
        
        return connections
    
    def _create_rafix_cam_hole(self, body, position, orientation):
        """
        Crea foro per camma Rafix
        
        Args:
            body: BRepBody
            position: Dizionario posizione
            orientation: Orientamento
        
        Returns:
            Feature o None
        """
        try:
            holes = self.component.features.holeFeatures
            
            # Crea punto
            point = adsk.core.Point3D.create(
                position['x'] / 10.0,
                position['y'] / 10.0,
                position['z'] / 10.0
            )
            
            # Determina direzione
            if orientation == 'horizontal':
                direction = adsk.core.Vector3D.create(1, 0, 0)
            else:
                direction = adsk.core.Vector3D.create(0, 0, 1)
            
            # Crea foro
            hole_input = holes.createSimpleInput(
                adsk.core.ValueInput.createByReal(self.rafix_cam_diameter / 20.0)
            )
            hole_input.setPositionByPoint(point)
            hole_input.setDistanceExtent(
                adsk.core.ValueInput.createByReal(self.rafix_cam_depth / 10.0)
            )
            hole_input.setDirection(direction)
            
            hole = holes.add(hole_input)
            return hole
        except:
            return None
    
    def _create_rafix_pin_hole(self, body, position, orientation):
        """
        Crea foro per spina Rafix
        
        Args:
            body: BRepBody
            position: Dizionario posizione
            orientation: Orientamento
        
        Returns:
            Feature o None
        """
        try:
            holes = self.component.features.holeFeatures
            
            # Crea punto
            point = adsk.core.Point3D.create(
                position['x'] / 10.0,
                position['y'] / 10.0,
                position['z'] / 10.0
            )
            
            # Determina direzione (opposta alla camma)
            if orientation == 'horizontal':
                direction = adsk.core.Vector3D.create(-1, 0, 0)
            else:
                direction = adsk.core.Vector3D.create(0, 0, -1)
            
            # Crea foro
            hole_input = holes.createSimpleInput(
                adsk.core.ValueInput.createByReal(self.rafix_pin_diameter / 20.0)
            )
            hole_input.setPositionByPoint(point)
            hole_input.setDistanceExtent(
                adsk.core.ValueInput.createByReal(self.rafix_pin_depth / 10.0)
            )
            hole_input.setDirection(direction)
            
            hole = holes.add(hole_input)
            return hole
        except:
            return None
    
    def _create_minifix_housing_hole(self, body, position, orientation):
        """
        Crea foro alloggiamento Minifix
        
        Args:
            body: BRepBody
            position: Dizionario posizione
            orientation: Orientamento
        
        Returns:
            Feature o None
        """
        try:
            holes = self.component.features.holeFeatures
            
            point = adsk.core.Point3D.create(
                position['x'] / 10.0,
                position['y'] / 10.0,
                position['z'] / 10.0
            )
            
            if orientation == 'horizontal':
                direction = adsk.core.Vector3D.create(1, 0, 0)
            else:
                direction = adsk.core.Vector3D.create(0, 0, 1)
            
            hole_input = holes.createSimpleInput(
                adsk.core.ValueInput.createByReal(self.minifix_housing_diameter / 20.0)
            )
            hole_input.setPositionByPoint(point)
            hole_input.setDistanceExtent(
                adsk.core.ValueInput.createByReal(self.minifix_housing_depth / 10.0)
            )
            hole_input.setDirection(direction)
            
            hole = holes.add(hole_input)
            return hole
        except:
            return None
    
    def _create_minifix_pin_hole(self, body, position, orientation):
        """
        Crea foro spina Minifix
        
        Args:
            body: BRepBody
            position: Dizionario posizione
            orientation: Orientamento
        
        Returns:
            Feature o None
        """
        try:
            holes = self.component.features.holeFeatures
            
            point = adsk.core.Point3D.create(
                position['x'] / 10.0,
                position['y'] / 10.0,
                position['z'] / 10.0
            )
            
            if orientation == 'horizontal':
                direction = adsk.core.Vector3D.create(-1, 0, 0)
            else:
                direction = adsk.core.Vector3D.create(0, 0, -1)
            
            hole_input = holes.createSimpleInput(
                adsk.core.ValueInput.createByReal(self.minifix_pin_diameter / 20.0)
            )
            hole_input.setPositionByPoint(point)
            hole_input.setDistanceExtent(
                adsk.core.ValueInput.createByReal(self.minifix_pin_depth / 10.0)
            )
            hole_input.setDirection(direction)
            
            hole = holes.add(hole_input)
            return hole
        except:
            return None
    
    def get_connector_specs(self, connector_type):
        """
        Ottieni le specifiche tecniche di un connettore
        
        Args:
            connector_type: Tipo ('rafix', 'minifix')
        
        Returns:
            dict: Specifiche tecniche
        """
        if connector_type == 'rafix':
            return {
                'name': 'Rafix',
                'manufacturer': 'Hafele',
                'cam_diameter': self.rafix_cam_diameter,
                'cam_depth': self.rafix_cam_depth,
                'pin_diameter': self.rafix_pin_diameter,
                'pin_depth': self.rafix_pin_depth,
                'material_thickness_min': 15,
                'material_thickness_max': 25,
                'load_capacity_kg': 50
            }
        elif connector_type == 'minifix':
            return {
                'name': 'Minifix',
                'manufacturer': 'Hafele',
                'housing_diameter': self.minifix_housing_diameter,
                'housing_depth': self.minifix_housing_depth,
                'pin_diameter': self.minifix_pin_diameter,
                'pin_depth': self.minifix_pin_depth,
                'material_thickness_min': 15,
                'material_thickness_max': 19,
                'load_capacity_kg': 35
            }
        else:
            return {}
