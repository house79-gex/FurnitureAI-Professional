"""
Generatore di cassetti con guide scorrevoli
Sistema completo per cassetti con parametri di montaggio
"""

import adsk.core
import adsk.fusion

class DrawerGenerator:
    """Generatore di cassetti parametrici"""
    
    def __init__(self, design):
        """
        Inizializza il generatore
        
        Args:
            design: Istanza di adsk.fusion.Design
        """
        self.design = design
        self.root_comp = design.rootComponent
    
    def create_drawer(self, params):
        """
        Crea un cassetto completo
        
        Args:
            params: Dizionario con parametri
                - width: Larghezza cassetto (mm)
                - depth: Profondità cassetto (mm)
                - height: Altezza cassetto (mm)
                - thickness: Spessore pannelli (mm, default 18)
                - bottom_thickness: Spessore fondo (mm, default 3)
                - front_height: Altezza frontale (mm, default = height)
                - drawer_type: Tipo ('standard', 'inner', default 'standard')
                - parent_component: Componente genitore (cabinet) - opzionale
                - posizione_da_top: Posizione Z dalla cima del mobile (mm) - per posizionamento
        
        Returns:
            adsk.fusion.Component: Componente cassetto
        """
        width = params.get('width', 400)
        depth = params.get('depth', 500)
        height = params.get('height', 150)
        thickness = params.get('thickness', 18)
        bottom_thickness = params.get('bottom_thickness', 3)
        front_height = params.get('front_height', height)
        drawer_type = params.get('drawer_type', 'standard')
        parent_component = params.get('parent_component', None)
        posizione_da_top = params.get('posizione_da_top', None)
        
        # BUG FIX: Create drawer inside parent component if provided
        target_comp = parent_component if parent_component else self.root_comp
        
        # BUG FIX: Calculate position transform if posizione_da_top specified
        transform = adsk.core.Matrix3D.create()
        if posizione_da_top is not None:
            # Z position: measured from top, so it's negative offset from cabinet top
            z_position = posizione_da_top / 10.0
            transform.translation = adsk.core.Vector3D.create(0, 0, z_position)
        
        # Crea componente cassetto
        occurrence = target_comp.occurrences.addNewComponent(transform)
        drawer_comp = occurrence.component
        drawer_comp.name = f"Cassetto_{int(width)}x{int(depth)}x{int(height)}"
        
        # Crea i componenti del cassetto
        self._create_drawer_sides(drawer_comp, width, depth, height, thickness)
        self._create_drawer_front_back(drawer_comp, width, height, thickness, depth)
        self._create_drawer_bottom(drawer_comp, width, depth, bottom_thickness, thickness)
        
        if drawer_type == 'standard':
            self._create_drawer_face(drawer_comp, width, front_height, thickness)
        
        return drawer_comp
    
    def create_drawer_stack(self, params):
        """
        Crea una pila di cassetti
        
        Args:
            params: Dizionario con parametri
                - width: Larghezza (mm)
                - depth: Profondità (mm)
                - total_height: Altezza totale disponibile (mm)
                - drawer_count: Numero cassetti
                - thickness: Spessore pannelli (mm)
                - gap: Spazio tra cassetti (mm, default 2)
        
        Returns:
            list: Lista di componenti cassetti
        """
        width = params.get('width', 400)
        depth = params.get('depth', 500)
        total_height = params.get('total_height', 600)
        drawer_count = params.get('drawer_count', 3)
        thickness = params.get('thickness', 18)
        gap = params.get('gap', 2)
        
        # Calcola altezza singolo cassetto
        available_height = total_height - (gap * (drawer_count - 1))
        drawer_height = available_height / drawer_count
        
        drawers = []
        current_z = 0
        
        for i in range(drawer_count):
            drawer_params = {
                'width': width,
                'depth': depth,
                'height': drawer_height,
                'thickness': thickness,
                'drawer_type': 'standard'
            }
            
            drawer = self.create_drawer(drawer_params)
            drawers.append(drawer)
            
            # Posiziona il cassetto
            if i > 0:
                transform = adsk.core.Matrix3D.create()
                transform.translation = adsk.core.Vector3D.create(0, 0, current_z / 10.0)
                
                for occ in self.root_comp.occurrences:
                    if occ.component == drawer:
                        occ.transform = transform
                        break
            
            current_z += drawer_height + gap
        
        return drawers
    
    def _create_drawer_sides(self, component, width, depth, height, thickness):
        """Crea i fianchi del cassetto"""
        sketches = component.sketches
        extrudes = component.features.extrudeFeatures
        
        yz_plane = component.yZConstructionPlane
        
        # Fianco sinistro
        sketch_left = sketches.add(yz_plane)
        rect_left = sketch_left.sketchCurves.sketchLines.addTwoPointRectangle(
            adsk.core.Point3D.create(0, 0, 0),
            adsk.core.Point3D.create(depth / 10.0, height / 10.0, 0)
        )
        
        extrude_input = extrudes.createInput(
            sketch_left.profiles.item(0),
            adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        distance = adsk.core.ValueInput.createByReal(thickness / 10.0)
        extrude_input.setDistanceExtent(False, distance)
        extrude_left = extrudes.add(extrude_input)
        extrude_left.bodies.item(0).name = "Fianco_Sinistro"
        
        # Fianco destro
        sketch_right = sketches.add(yz_plane)
        rect_right = sketch_right.sketchCurves.sketchLines.addTwoPointRectangle(
            adsk.core.Point3D.create(0, 0, 0),
            adsk.core.Point3D.create(depth / 10.0, height / 10.0, 0)
        )
        
        extrude_input_right = extrudes.createInput(
            sketch_right.profiles.item(0),
            adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        extrude_input_right.setDistanceExtent(False, distance)
        extrude_right = extrudes.add(extrude_input_right)
        
        # Sposta a destra
        transform = adsk.core.Matrix3D.create()
        transform.translation = adsk.core.Vector3D.create((width - thickness) / 10.0, 0, 0)
        
        move_feats = component.features.moveFeatures
        bodies = adsk.core.ObjectCollection.create()
        bodies.add(extrude_right.bodies.item(0))
        move_input = move_feats.createInput(bodies, transform)
        move_feats.add(move_input)
        
        extrude_right.bodies.item(0).name = "Fianco_Destro"
    
    def _create_drawer_front_back(self, component, width, height, thickness, depth=None):
        """
        Crea fronte e retro del cassetto.
        
        SISTEMA COORDINATE (allineato con Fusion 360):
        - X = larghezza (width)
        - Y = altezza (height)  
        - Z = profondità (depth)
        
        Fronte e retro si sviluppano nel piano XY (larghezza × altezza),
        estrusi in direzione Z (profondità).
        """
        sketches = component.sketches
        extrudes = component.features.extrudeFeatures
        move_feats = component.features.moveFeatures
        
        xy_plane = component.xYConstructionPlane
        
        # Calcola larghezza interna
        internal_width = width - 2 * thickness
        
        # Fronte interno (a Z=0, fronte cassetto)
        sketch_front = sketches.add(xy_plane)
        rect_front = sketch_front.sketchCurves.sketchLines.addTwoPointRectangle(
            adsk.core.Point3D.create(thickness / 10.0, 0, 0),
            adsk.core.Point3D.create((thickness + internal_width) / 10.0, height / 10.0, 0)
        )
        
        extrude_input = extrudes.createInput(
            sketch_front.profiles.item(0),
            adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        distance = adsk.core.ValueInput.createByReal(thickness / 10.0)
        extrude_input.setDistanceExtent(False, distance)
        extrude_front = extrudes.add(extrude_input)
        extrude_front.bodies.item(0).name = "Fronte_Interno"
        
        # Retro (più basso per permettere scorrimento del fondo)
        back_height = height - 10  # 10mm più basso
        
        sketch_back = sketches.add(xy_plane)
        rect_back = sketch_back.sketchCurves.sketchLines.addTwoPointRectangle(
            adsk.core.Point3D.create(thickness / 10.0, 0, 0),
            adsk.core.Point3D.create((thickness + internal_width) / 10.0, back_height / 10.0, 0)
        )
        
        extrude_input_back = extrudes.createInput(
            sketch_back.profiles.item(0),
            adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        extrude_input_back.setDistanceExtent(False, distance)
        extrude_back = extrudes.add(extrude_input_back)
        extrude_back.bodies.item(0).name = "Retro"
        
        # Posiziona il pannello retro alla profondità corretta (Z = depth - thickness)
        if depth is not None:
            transform_back = adsk.core.Matrix3D.create()
            # Position back at Z = depth - thickness (depth is along Z axis)
            z_back = (depth - thickness) / 10.0
            transform_back.translation = adsk.core.Vector3D.create(0, 0, z_back)
            
            bodies_back = adsk.core.ObjectCollection.create()
            bodies_back.add(extrude_back.bodies.item(0))
            move_input_back = move_feats.createInput(bodies_back, transform_back)
            move_feats.add(move_input_back)
    
    def _create_drawer_bottom(self, component, width, depth, bottom_thickness, side_thickness):
        """
        Crea il fondo del cassetto.
        
        SISTEMA COORDINATE (allineato con Fusion 360):
        - X = larghezza (width)
        - Y = altezza (height)
        - Z = profondità (depth)
        
        Il fondo si sviluppa nel piano XZ (larghezza × profondità),
        estruso in direzione +Y (verso l'alto) per lo spessore.
        """
        sketches = component.sketches
        extrudes = component.features.extrudeFeatures
        move_feats = component.features.moveFeatures
        
        xz_plane = component.xZConstructionPlane
        
        # Dimensioni fondo (dentro ai fianchi)
        bottom_width = width - 2 * side_thickness
        
        sketch = sketches.add(xz_plane)
        rect = sketch.sketchCurves.sketchLines.addTwoPointRectangle(
            adsk.core.Point3D.create(side_thickness / 10.0, 0, 0),
            adsk.core.Point3D.create((side_thickness + bottom_width) / 10.0, depth / 10.0, 0)
        )
        
        extrude_input = extrudes.createInput(
            sketch.profiles.item(0),
            adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        distance = adsk.core.ValueInput.createByReal(bottom_thickness / 10.0)
        extrude_input.setDistanceExtent(False, distance)
        extrude_bottom = extrudes.add(extrude_input)
        extrude_bottom.bodies.item(0).name = "Fondo"
        
        # Il fondo scorre in scanalature nei fianchi, fronte e retro
        # Tipicamente posizionato a 10mm dal fondo per permettere la scanalatura
        y_bottom_groove_offset = 1.0  # 10mm convertiti in cm
        transform_bottom = adsk.core.Matrix3D.create()
        transform_bottom.translation = adsk.core.Vector3D.create(0, y_bottom_groove_offset, 0)
        
        bodies_bottom = adsk.core.ObjectCollection.create()
        bodies_bottom.add(extrude_bottom.bodies.item(0))
        move_input_bottom = move_feats.createInput(bodies_bottom, transform_bottom)
        move_feats.add(move_input_bottom)
    
    def _create_drawer_face(self, component, width, height, thickness):
        """
        Crea il frontale del cassetto (parte visibile).
        
        SISTEMA COORDINATE (allineato con Fusion 360):
        - X = larghezza (width)
        - Y = altezza (height)
        - Z = profondità (depth)
        
        Il frontale si sviluppa nel piano XY (larghezza × altezza),
        estruso in direzione -Z (verso il fronte, verso l'esterno).
        """
        sketches = component.sketches
        extrudes = component.features.extrudeFeatures
        
        xy_plane = component.xYConstructionPlane
        
        sketch = sketches.add(xy_plane)
        rect = sketch.sketchCurves.sketchLines.addTwoPointRectangle(
            adsk.core.Point3D.create(0, 0, 0),
            adsk.core.Point3D.create(width / 10.0, height / 10.0, 0)
        )
        
        extrude_input = extrudes.createInput(
            sketch.profiles.item(0),
            adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        distance = adsk.core.ValueInput.createByReal(thickness / 10.0)
        extrude_input.setDistanceExtent(False, distance)
        extrude_face = extrudes.add(extrude_input)
        extrude_face.bodies.item(0).name = "Frontale"
    
    def add_slide_preparation(self, drawer_comp, slide_type='quadro', cabinet_depth=580):
        """
        Aggiunge preparazioni per guide scorrevoli
        
        Args:
            drawer_comp: Componente cassetto
            slide_type: Tipo guida ('quadro', 'tandem', 'standard')
            cabinet_depth: Profondità mobile (mm)
        
        Returns:
            dict: Informazioni di montaggio
        """
        # Ottieni dimensioni cassetto
        bbox = drawer_comp.bRepBodies.item(0).boundingBox
        drawer_width = (bbox.maxPoint.x - bbox.minPoint.x) * 10  # cm to mm
        drawer_height = (bbox.maxPoint.z - bbox.minPoint.z) * 10
        
        mounting_info = {
            'slide_type': slide_type,
            'cabinet_depth': cabinet_depth,
            'drawer_width': drawer_width,
            'drawer_height': drawer_height,
            'mounting_holes': []
        }
        
        # Per guide Quadro V6 (Hettich):
        # - Fori su fianchi a metà altezza
        # - Distanza tra fori: 32mm (compatibile System 32)
        if slide_type == 'quadro':
            hole_positions = self._calculate_slide_holes(drawer_height, 'quadro')
            mounting_info['mounting_holes'] = hole_positions
        
        return mounting_info
    
    def _calculate_slide_holes(self, drawer_height, slide_type):
        """
        Calcola posizioni fori per guide
        
        Args:
            drawer_height: Altezza cassetto (mm)
            slide_type: Tipo guida
        
        Returns:
            list: Lista di posizioni fori (mm dall'origine)
        """
        if slide_type == 'quadro':
            # Fori a metà altezza, sistema 32mm
            center_height = drawer_height / 2.0
            
            # Arrotonda al multiplo di 32 più vicino
            base_position = round(center_height / 32) * 32
            
            return [
                {'z': base_position, 'type': 'mounting'},
                {'z': base_position + 32, 'type': 'adjustment'}
            ]
        
        return []
