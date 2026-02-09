"""
Generatore di ante (porte) singole e doppie per mobili
Supporta diverse tipologie di apertura e montaggio
"""

import adsk.core
import adsk.fusion
import math

class DoorGenerator:
    """Generatore di ante per mobili"""
    
    def __init__(self, design):
        """
        Inizializza il generatore di ante
        
        Args:
            design: Istanza di adsk.fusion.Design
        """
        self.design = design
        self.root_comp = design.rootComponent
    
    def create_door(self, params):
        """
        Crea un'anta singola
        
        Args:
            params: Dizionario con parametri
                - width: Larghezza anta (mm)
                - height: Altezza anta (mm)
                - thickness: Spessore anta (mm, default 18)
                - door_type: Tipo ('flat', 'frame', default 'flat')
                - position: Posizione montaggio ('left', 'right', 'top', 'bottom')
                - parent_component: Componente genitore (cabinet) - opzionale
                - cabinet_depth: Profondità mobile per posizionamento (mm)
                - cabinet_plinth_height: Altezza zoccolo per posizionamento Z (mm)
                - x_offset: Offset X per posizionamento (mm, default 0)
                - mounting_type: Tipo montaggio ('copertura_totale', 'filo', 'semicopertura')
        
        Returns:
            adsk.fusion.Component: Componente anta
        """
        width = params.get('width', 400)
        height = params.get('height', 700)
        thickness = params.get('thickness', 18)
        door_type = params.get('door_type', 'flat')
        position = params.get('position', 'left')
        parent_component = params.get('parent_component', None)
        cabinet_depth = params.get('cabinet_depth', 0)
        cabinet_plinth_height = params.get('cabinet_plinth_height', 0)
        x_offset = params.get('x_offset', 0)
        mounting_type = params.get('mounting_type', 'copertura_totale')
        
        # BUG FIX: Create door inside parent component if provided
        target_comp = parent_component if parent_component else self.root_comp
        
        # BUG FIX: Calculate position transform
        transform = adsk.core.Matrix3D.create()
        
        # Y position: at cabinet front (depth)
        # For copertura_totale, door extends beyond cabinet front
        # For filo, door is flush with cabinet front (same calculation for now)
        # For semicopertura, door partially covers
        y_position = 0
        if cabinet_depth > 0:
            if mounting_type == 'copertura_totale':
                y_position = (cabinet_depth - thickness) / 10.0
            elif mounting_type == 'filo':
                # Filo means flush - in this simplified model, same as copertura_totale
                # In real implementation, would need cabinet panel thickness offsets
                y_position = (cabinet_depth - thickness) / 10.0
            else:  # semicopertura
                y_position = (cabinet_depth - thickness / 2.0) / 10.0
        
        # Z position: starts at plinth height
        z_position = cabinet_plinth_height / 10.0
        
        # X position: based on x_offset
        x_position = x_offset / 10.0
        
        transform.translation = adsk.core.Vector3D.create(x_position, y_position, z_position)
        
        # Crea componente anta
        occurrence = target_comp.occurrences.addNewComponent(transform)
        door_comp = occurrence.component
        door_comp.name = f"Anta_{position.capitalize()}_{int(width)}x{int(height)}"
        
        if door_type == 'flat':
            self._create_flat_door(door_comp, width, height, thickness)
        elif door_type == 'frame':
            self._create_frame_door(door_comp, width, height, thickness)
        
        return door_comp
    
    def create_double_door(self, params):
        """
        Crea una coppia di ante doppie
        
        Args:
            params: Dizionario con parametri
                - total_width: Larghezza totale (mm)
                - height: Altezza (mm)
                - thickness: Spessore (mm, default 18)
                - gap: Distanza tra le ante (mm, default 3)
                - door_type: Tipo anta
                - parent_component: Componente genitore (cabinet) - opzionale
                - cabinet_depth: Profondità mobile per posizionamento (mm)
                - cabinet_plinth_height: Altezza zoccolo per posizionamento Z (mm)
                - x_offset: Offset X iniziale per posizionamento (mm, default 0)
                - mounting_type: Tipo montaggio ('copertura_totale', 'filo', 'semicopertura')
        
        Returns:
            tuple: (componente_sinistra, componente_destra)
        """
        total_width = params.get('total_width', 800)
        height = params.get('height', 700)
        thickness = params.get('thickness', 18)
        gap = params.get('gap', 3)
        door_type = params.get('door_type', 'flat')
        parent_component = params.get('parent_component', None)
        cabinet_depth = params.get('cabinet_depth', 0)
        cabinet_plinth_height = params.get('cabinet_plinth_height', 0)
        x_offset = params.get('x_offset', 0)
        mounting_type = params.get('mounting_type', 'copertura_totale')
        
        # Calcola larghezza singola anta
        single_width = (total_width - gap) / 2.0
        
        # Crea anta sinistra
        left_params = {
            'width': single_width,
            'height': height,
            'thickness': thickness,
            'door_type': door_type,
            'position': 'left',
            'parent_component': parent_component,
            'cabinet_depth': cabinet_depth,
            'cabinet_plinth_height': cabinet_plinth_height,
            'x_offset': x_offset,
            'mounting_type': mounting_type
        }
        left_door = self.create_door(left_params)
        
        # Crea anta destra
        right_params = {
            'width': single_width,
            'height': height,
            'thickness': thickness,
            'door_type': door_type,
            'position': 'right',
            'parent_component': parent_component,
            'cabinet_depth': cabinet_depth,
            'cabinet_plinth_height': cabinet_plinth_height,
            'x_offset': x_offset + single_width + gap,
            'mounting_type': mounting_type
        }
        right_door = self.create_door(right_params)
        
        return left_door, right_door
    
    def _create_flat_door(self, component, width, height, thickness):
        """
        Crea anta piatta (pannello singolo)
        
        Args:
            component: Componente destinazione
            width, height, thickness: Dimensioni in mm
        """
        sketches = component.sketches
        extrudes = component.features.extrudeFeatures
        
        xy_plane = component.xYConstructionPlane
        
        # Crea rettangolo
        sketch = sketches.add(xy_plane)
        rect = sketch.sketchCurves.sketchLines.addTwoPointRectangle(
            adsk.core.Point3D.create(0, 0, 0),
            adsk.core.Point3D.create(width / 10.0, height / 10.0, 0)
        )
        
        # Estrudi
        extrude_input = extrudes.createInput(
            sketch.profiles.item(0),
            adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        distance = adsk.core.ValueInput.createByReal(thickness / 10.0)
        extrude_input.setDistanceExtent(False, distance)
        extrude = extrudes.add(extrude_input)
        extrude.bodies.item(0).name = "Pannello_Anta"
    
    def _create_frame_door(self, component, width, height, thickness):
        """
        Crea anta con telaio (stile shaker semplificato)
        
        Args:
            component: Componente destinazione
            width, height, thickness: Dimensioni in mm
        """
        frame_width = 60  # Larghezza telaio
        
        sketches = component.sketches
        extrudes = component.features.extrudeFeatures
        
        xy_plane = component.xYConstructionPlane
        
        # Crea profilo telaio con rettangolo interno vuoto
        sketch = sketches.add(xy_plane)
        lines = sketch.sketchCurves.sketchLines
        
        # Rettangolo esterno
        outer_rect = lines.addTwoPointRectangle(
            adsk.core.Point3D.create(0, 0, 0),
            adsk.core.Point3D.create(width / 10.0, height / 10.0, 0)
        )
        
        # Rettangolo interno (vuoto)
        inner_rect = lines.addTwoPointRectangle(
            adsk.core.Point3D.create(frame_width / 10.0, frame_width / 10.0, 0),
            adsk.core.Point3D.create((width - frame_width) / 10.0, (height - frame_width) / 10.0, 0)
        )
        
        # Estrudi il profilo (dovrebbe creare automaticamente il telaio)
        extrude_input = extrudes.createInput(
            sketch.profiles.item(0),
            adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        distance = adsk.core.ValueInput.createByReal(thickness / 10.0)
        extrude_input.setDistanceExtent(False, distance)
        extrude_frame = extrudes.add(extrude_input)
        extrude_frame.bodies.item(0).name = "Telaio_Anta"
        
        # Crea pannello centrale (più sottile)
        panel_thickness = thickness - 4  # Pannello ribassato
        
        sketch_panel = sketches.add(xy_plane)
        rect_panel = sketch_panel.sketchCurves.sketchLines.addTwoPointRectangle(
            adsk.core.Point3D.create((frame_width + 5) / 10.0, (frame_width + 5) / 10.0, 0),
            adsk.core.Point3D.create((width - frame_width - 5) / 10.0, (height - frame_width - 5) / 10.0, 0)
        )
        
        extrude_input_panel = extrudes.createInput(
            sketch_panel.profiles.item(0),
            adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        distance_panel = adsk.core.ValueInput.createByReal(panel_thickness / 10.0)
        extrude_input_panel.setDistanceExtent(False, distance_panel)
        extrude_panel = extrudes.add(extrude_input_panel)
        extrude_panel.bodies.item(0).name = "Pannello_Centrale"
    
    def add_hinge_preparation(self, door_comp, hinge_type='clip_top', hinge_count=2):
        """
        Aggiunge le preparazioni per le cerniere
        
        Args:
            door_comp: Componente anta
            hinge_type: Tipo cerniera ('clip_top', 'standard')
            hinge_count: Numero di cerniere
        
        Returns:
            list: Lista di feature create
        """
        features = []
        
        # Ottieni dimensioni anta
        bbox = door_comp.bRepBodies.item(0).boundingBox
        height = (bbox.maxPoint.z - bbox.minPoint.z) * 10  # cm to mm
        
        # Calcola posizioni cerniere
        if hinge_count == 2:
            positions = [height * 0.15, height * 0.85]  # 15% e 85% dell'altezza
        elif hinge_count == 3:
            positions = [height * 0.1, height * 0.5, height * 0.9]
        else:
            # Spaziatura uniforme
            spacing = height / (hinge_count + 1)
            positions = [spacing * (i + 1) for i in range(hinge_count)]
        
        # Per cerniere Clip Top (Blum): foro diametro 35mm, profondità 12mm
        if hinge_type == 'clip_top':
            hole_diameter = 35
            hole_depth = 12
            
            for pos in positions:
                feature = self._create_hinge_hole(
                    door_comp,
                    pos,
                    hole_diameter,
                    hole_depth
                )
                if feature:
                    features.append(feature)
        
        return features
    
    def _create_hinge_hole(self, component, z_position, diameter, depth):
        """
        Crea un foro per cerniera
        
        Args:
            component: Componente destinazione
            z_position: Posizione Z del foro (mm)
            diameter: Diametro foro (mm)
            depth: Profondità foro (mm)
        
        Returns:
            Feature creata o None
        """
        try:
            sketches = component.sketches
            extrudes = component.features.extrudeFeatures
            
            # Crea piano di costruzione alla posizione Z
            yz_plane = component.yZConstructionPlane
            
            # Crea sketch con cerchio
            sketch = sketches.add(yz_plane)
            
            # Centro foro a metà larghezza anta
            bbox = component.bRepBodies.item(0).boundingBox
            y_center = (bbox.maxPoint.y - bbox.minPoint.y) / 2.0
            
            center_point = adsk.core.Point3D.create(0, y_center, z_position / 10.0)
            circle = sketch.sketchCurves.sketchCircles.addByCenterRadius(
                center_point,
                diameter / 20.0  # mm to cm, e poi raggio
            )
            
            # Estrudi come taglio
            extrude_input = extrudes.createInput(
                sketch.profiles.item(0),
                adsk.fusion.FeatureOperations.CutFeatureOperation
            )
            distance = adsk.core.ValueInput.createByReal(depth / 10.0)
            extrude_input.setDistanceExtent(False, distance)
            extrude = extrudes.add(extrude_input)
            
            return extrude
        except:
            return None
