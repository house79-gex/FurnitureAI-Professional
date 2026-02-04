"""
Inseritore ferramenta nel modello Fusion 360
Posiziona fisicamente i componenti hardware nel design
"""

import adsk.core
import adsk.fusion

class HardwareInserter:
    """Inserisce componenti hardware nel modello Fusion"""
    
    def __init__(self, component):
        """
        Inizializza l'inseritore
        
        Args:
            component: Componente Fusion destinazione
        """
        self.component = component
        self.design = component.parentDesign
    
    def insert_hinge(self, hinge_data, position, side='left'):
        """
        Inserisce una cerniera nel modello
        
        Args:
            hinge_data: Dati cerniera dal catalogo
            position: Posizione Z (mm)
            side: Lato montaggio ('left', 'right')
        
        Returns:
            dict: Informazioni inserimento
        """
        cup_diameter = hinge_data.get('cup_diameter', 35)
        cup_depth = hinge_data.get('cup_depth', 12)
        
        # Crea componente per cerniera (semplificato come cilindro)
        occurrence = self.component.occurrences.addNewComponent(
            adsk.core.Matrix3D.create()
        )
        hinge_comp = occurrence.component
        hinge_comp.name = f"Cerniera_{side}_{int(position)}"
        
        # Crea rappresentazione semplificata cerniera
        sketches = hinge_comp.sketches
        xy_plane = hinge_comp.xYConstructionPlane
        
        sketch = sketches.add(xy_plane)
        circle = sketch.sketchCurves.sketchCircles.addByCenterRadius(
            adsk.core.Point3D.create(0, 0, 0),
            cup_diameter / 20.0  # mm to cm, poi raggio
        )
        
        # Estrudi
        extrudes = hinge_comp.features.extrudeFeatures
        extrude_input = extrudes.createInput(
            sketch.profiles.item(0),
            adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        
        distance = adsk.core.ValueInput.createByReal(cup_depth / 10.0)
        extrude_input.setDistanceExtent(False, distance)
        
        hinge_body = extrudes.add(extrude_input)
        hinge_body.bodies.item(0).name = "Corpo_Cerniera"
        
        # Posiziona alla posizione corretta
        transform = adsk.core.Matrix3D.create()
        x_offset = 0 if side == 'left' else 40  # Semplificazione
        transform.translation = adsk.core.Vector3D.create(
            x_offset / 10.0,
            0,
            position / 10.0
        )
        occurrence.transform = transform
        
        return {
            'success': True,
            'component': hinge_comp,
            'position': position,
            'side': side
        }
    
    def insert_slide_pair(self, slide_data, drawer_position):
        """
        Inserisce una coppia di guide scorrevoli
        
        Args:
            slide_data: Dati guida dal catalogo
            drawer_position: Posizione cassetto (x, y, z)
        
        Returns:
            dict: Informazioni inserimento
        """
        slide_length = slide_data.get('length', 500)
        mounting_height = slide_data.get('technical_specs', {}).get('mounting_height', 90)
        
        # Crea componenti guide (semplificati come barre)
        # Guida sinistra
        left_guide = self._create_slide_component(slide_length, 'sinistra')
        
        # Guida destra
        right_guide = self._create_slide_component(slide_length, 'destra')
        
        # Posiziona le guide
        # (semplificazione: posizionamento approssimato)
        
        return {
            'success': True,
            'left_guide': left_guide,
            'right_guide': right_guide,
            'slide_length': slide_length
        }
    
    def insert_handle(self, handle_data, door_component, position='center'):
        """
        Inserisce una maniglia su anta/cassetto
        
        Args:
            handle_data: Dati maniglia dal catalogo
            door_component: Componente anta/frontale
            position: Posizione ('center', 'top', 'bottom')
        
        Returns:
            dict: Informazioni inserimento
        """
        handle_type = handle_data.get('type', 'bar')
        
        if handle_type == 'bar':
            return self._insert_bar_handle(handle_data, door_component, position)
        elif handle_type == 'knob':
            return self._insert_knob_handle(handle_data, door_component, position)
        elif handle_type == 'recessed':
            return self._insert_recessed_handle(handle_data, door_component)
        else:
            return {'success': False, 'message': 'Tipo maniglia non supportato'}
    
    def insert_shelf_supports(self, body, positions):
        """
        Inserisce supporti ripiano
        
        Args:
            body: Corpo fianco mobile
            positions: Lista di posizioni Z (mm)
        
        Returns:
            list: Lista supporti inseriti
        """
        supports = []
        
        for pos in positions:
            # Crea pin di supporto (cilindro piccolo)
            support_comp = self._create_shelf_support_component(pos)
            supports.append(support_comp)
        
        return supports
    
    def _create_slide_component(self, length, side):
        """Crea componente guida scorrevole semplificato"""
        occurrence = self.component.occurrences.addNewComponent(
            adsk.core.Matrix3D.create()
        )
        slide_comp = occurrence.component
        slide_comp.name = f"Guida_{side}_{int(length)}"
        
        # Crea barra rettangolare semplificata
        sketches = slide_comp.sketches
        xy_plane = slide_comp.xYConstructionPlane
        
        sketch = sketches.add(xy_plane)
        rect = sketch.sketchCurves.sketchLines.addTwoPointRectangle(
            adsk.core.Point3D.create(0, 0, 0),
            adsk.core.Point3D.create(length / 10.0, 0.5, 0)  # 5mm altezza
        )
        
        # Estrudi
        extrudes = slide_comp.features.extrudeFeatures
        extrude_input = extrudes.createInput(
            sketch.profiles.item(0),
            adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        
        distance = adsk.core.ValueInput.createByReal(1.2)  # 12mm spessore
        extrude_input.setDistanceExtent(False, distance)
        
        slide_body = extrudes.add(extrude_input)
        slide_body.bodies.item(0).name = f"Corpo_Guida_{side}"
        
        return slide_comp
    
    def _insert_bar_handle(self, handle_data, door_component, position):
        """Inserisce maniglia a barra"""
        interaxis = handle_data.get('interaxis', 320)
        diameter = handle_data.get('diameter', 12)
        
        # Ottieni dimensioni anta
        bbox = door_component.bRepBodies.item(0).boundingBox
        door_width = (bbox.maxPoint.x - bbox.minPoint.x) * 10  # cm to mm
        door_height = (bbox.maxPoint.z - bbox.minPoint.z) * 10
        
        # Calcola posizione
        if position == 'center':
            x_pos = door_width / 2
            z_pos = door_height / 2
        elif position == 'top':
            x_pos = door_width / 2
            z_pos = door_height - 50  # 50mm dal top
        else:  # bottom
            x_pos = door_width / 2
            z_pos = 50  # 50mm dal bottom
        
        # Crea fori per viti (semplificazione)
        hole_positions = [
            (x_pos - interaxis / 2, z_pos),
            (x_pos + interaxis / 2, z_pos)
        ]
        
        # Crea componente maniglia (cilindro orizzontale)
        occurrence = door_component.occurrences.addNewComponent(
            adsk.core.Matrix3D.create()
        )
        handle_comp = occurrence.component
        handle_comp.name = "Maniglia_Barra"
        
        return {
            'success': True,
            'component': handle_comp,
            'hole_positions': hole_positions
        }
    
    def _insert_knob_handle(self, handle_data, door_component, position):
        """Inserisce pomello"""
        diameter = handle_data.get('diameter', 30)
        projection = handle_data.get('projection', 25)
        
        # Calcola posizione (simile a barra)
        bbox = door_component.bRepBodies.item(0).boundingBox
        door_width = (bbox.maxPoint.x - bbox.minPoint.x) * 10
        door_height = (bbox.maxPoint.z - bbox.minPoint.z) * 10
        
        x_pos = door_width / 2
        z_pos = door_height / 2 if position == 'center' else door_height - 50
        
        # Crea componente pomello (sfera/cilindro)
        occurrence = door_component.occurrences.addNewComponent(
            adsk.core.Matrix3D.create()
        )
        knob_comp = occurrence.component
        knob_comp.name = "Pomello"
        
        return {
            'success': True,
            'component': knob_comp,
            'position': (x_pos, z_pos)
        }
    
    def _insert_recessed_handle(self, handle_data, door_component):
        """Inserisce maniglia a gola"""
        groove_depth = handle_data.get('mounting', {}).get('groove_depth', 13)
        groove_height = handle_data.get('mounting', {}).get('groove_height', 19)
        
        # Crea scasso per gola (semplificazione)
        # In realtà richiederebbe un taglio sul bordo superiore dell'anta
        
        return {
            'success': True,
            'message': 'Maniglia a gola richiede scasso sul bordo superiore',
            'groove_specs': {
                'depth': groove_depth,
                'height': groove_height
            }
        }
    
    def _create_shelf_support_component(self, z_position):
        """Crea componente supporto ripiano"""
        occurrence = self.component.occurrences.addNewComponent(
            adsk.core.Matrix3D.create()
        )
        support_comp = occurrence.component
        support_comp.name = f"Supporto_Ripiano_{int(z_position)}"
        
        # Crea pin (cilindro piccolo)
        sketches = support_comp.sketches
        xy_plane = support_comp.xYConstructionPlane
        
        sketch = sketches.add(xy_plane)
        circle = sketch.sketchCurves.sketchCircles.addByCenterRadius(
            adsk.core.Point3D.create(0, 0, 0),
            0.25  # 5mm diametro
        )
        
        # Estrudi
        extrudes = support_comp.features.extrudeFeatures
        extrude_input = extrudes.createInput(
            sketch.profiles.item(0),
            adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        
        distance = adsk.core.ValueInput.createByReal(1.6)  # 16mm lunghezza
        extrude_input.setDistanceExtent(False, distance)
        
        support_body = extrudes.add(extrude_input)
        support_body.bodies.item(0).name = "Pin_Supporto"
        
        return support_comp
