"""
Generatore di mobili base (carcasse) con parametri utente
Sistema completo per la creazione di mobili parametrici
"""

import adsk.core
import adsk.fusion
import math

class CabinetGenerator:
    """Generatore parametrico di mobili con sistema di foratura"""
    
    def __init__(self, design):
        """
        Inizializza il generatore
        
        Args:
            design: Istanza di adsk.fusion.Design
        """
        self.design = design
        self.root_comp = design.rootComponent
        self.logger = None
    
    def create_cabinet(self, params):
        """
        Crea un mobile completo con parametri utente
        
        Args:
            params: Dizionario con parametri del mobile
                - width: Larghezza totale (mm)
                - height: Altezza totale (mm)
                - depth: Profondità totale (mm)
                - material_thickness: Spessore pannello (mm, default 18)
                - has_back: Include pannello posteriore (bool, default True)
                - back_thickness: Spessore pannello post. (mm, default 3)
                - has_plinth: Include zoccolo (bool, default True)
                - plinth_height: Altezza zoccolo (mm, default 100)
                - shelves_count: Numero ripiani (int, default 0)
                - divisions_count: Numero divisori verticali (int, default 0)
        
        Returns:
            adsk.fusion.Component: Componente del mobile creato
        """
        # Estrai parametri con valori default
        width = params.get('width', 800)
        height = params.get('height', 720)
        depth = params.get('depth', 580)
        thickness = params.get('material_thickness', 18)
        has_back = params.get('has_back', True)
        back_thickness = params.get('back_thickness', 3)
        has_plinth = params.get('has_plinth', True)
        plinth_height = params.get('plinth_height', 100)
        shelves_count = params.get('shelves_count', 0)
        divisions_count = params.get('divisions_count', 0)
        
        # Crea il componente principale
        occurrence = self.root_comp.occurrences.addNewComponent(
            adsk.core.Matrix3D.create()
        )
        cabinet_comp = occurrence.component
        cabinet_comp.name = f"Mobile_{int(width)}x{int(height)}x{int(depth)}"
        
        # Crea i parametri utente
        self._create_user_parameters(cabinet_comp, params)
        
        # Crea i pannelli principali
        self._create_side_panels(cabinet_comp, width, height, depth, thickness, has_plinth, plinth_height)
        self._create_top_bottom_panels(cabinet_comp, width, depth, thickness, height, has_plinth, plinth_height)
        
        # Aggiungi pannello posteriore se richiesto
        if has_back:
            self._create_back_panel(cabinet_comp, width, height, thickness, back_thickness, has_plinth, plinth_height)
        
        # Aggiungi zoccolo se richiesto
        if has_plinth:
            self._create_plinth(cabinet_comp, width, depth, thickness, plinth_height)
        
        # Aggiungi ripiani
        if shelves_count > 0:
            self._create_shelves(cabinet_comp, width, depth, thickness, height, shelves_count, has_plinth, plinth_height)
        
        # Aggiungi divisori verticali
        if divisions_count > 0:
            self._create_divisions(cabinet_comp, width, height, depth, thickness, divisions_count, has_plinth, plinth_height)
        
        return cabinet_comp
    
    def _create_user_parameters(self, component, params):
        """
        Crea parametri utente per il mobile
        
        Args:
            component: Componente Fusion
            params: Dizionario parametri
        """
        user_params = component.parentDesign.userParameters
        
        # Parametri dimensionali
        param_list = [
            ('Larghezza', params.get('width', 800), 'mm'),
            ('Altezza', params.get('height', 720), 'mm'),
            ('Profondita', params.get('depth', 580), 'mm'),
            ('Spessore', params.get('material_thickness', 18), 'mm'),
            ('SpessoreRetro', params.get('back_thickness', 3), 'mm'),
            ('AltezzaZoccolo', params.get('plinth_height', 100), 'mm')
        ]
        
        for name, value, unit in param_list:
            value_input = adsk.core.ValueInput.createByReal(value / 10.0)  # Converti mm in cm
            try:
                user_params.add(name, value_input, unit, '')
            except:
                # Il parametro esiste già
                pass
    
    def _create_side_panels(self, component, width, height, depth, thickness, has_plinth, plinth_height):
        """Crea i pannelli laterali"""
        sketches = component.sketches
        extrudes = component.features.extrudeFeatures
        move_feats = component.features.moveFeatures
        
        # Piano YZ per pannello sinistro
        yz_plane = component.yZConstructionPlane
        
        # Calcola altezza effettiva (considera lo zoccolo)
        effective_height = height - plinth_height if has_plinth else height
        
        # BUG FIX: Start side panels at plinth_height when plinth exists
        z_start = plinth_height / 10.0 if has_plinth else 0
        
        # Pannello sinistro
        sketch_left = sketches.add(yz_plane)
        rect_left = sketch_left.sketchCurves.sketchLines.addTwoPointRectangle(
            adsk.core.Point3D.create(0, z_start, 0),
            adsk.core.Point3D.create(depth / 10.0, z_start + effective_height / 10.0, 0)  # mm to cm
        )
        
        extrude_input = extrudes.createInput(
            sketch_left.profiles.item(0),
            adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        distance = adsk.core.ValueInput.createByReal(thickness / 10.0)
        extrude_input.setDistanceExtent(False, distance)
        extrude_left = extrudes.add(extrude_input)
        extrude_left.bodies.item(0).name = "Fianco_Sinistro"
        
        # Pannello destro (offset in X)
        sketch_right = sketches.add(yz_plane)
        rect_right = sketch_right.sketchCurves.sketchLines.addTwoPointRectangle(
            adsk.core.Point3D.create(0, z_start, 0),
            adsk.core.Point3D.create(depth / 10.0, z_start + effective_height / 10.0, 0)
        )
        
        # Transform per posizionare a destra
        transform_right = adsk.core.Matrix3D.create()
        transform_right.translation = adsk.core.Vector3D.create((width - thickness) / 10.0, 0, 0)
        
        extrude_input_right = extrudes.createInput(
            sketch_right.profiles.item(0),
            adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        extrude_input_right.setDistanceExtent(False, distance)
        extrude_right = extrudes.add(extrude_input_right)
        
        # Sposta il corpo
        bodies_right = adsk.core.ObjectCollection.create()
        bodies_right.add(extrude_right.bodies.item(0))
        move_input_right = move_feats.createInput(bodies_right, transform_right)
        move_feats.add(move_input_right)
        
        extrude_right.bodies.item(0).name = "Fianco_Destro"
    
    def _create_top_bottom_panels(self, component, width, depth, thickness, height=None, has_plinth=False, plinth_height=0):
        """Crea i pannelli superiore e inferiore"""
        sketches = component.sketches
        extrudes = component.features.extrudeFeatures
        move_feats = component.features.moveFeatures
        
        xy_plane = component.xYConstructionPlane
        
        # BUG FIX: Calculate Z positions for bottom and top panels
        z_bottom = plinth_height / 10.0 if has_plinth else 0
        
        # Pannello inferiore
        sketch_bottom = sketches.add(xy_plane)
        rect_bottom = sketch_bottom.sketchCurves.sketchLines.addTwoPointRectangle(
            adsk.core.Point3D.create(0, 0, 0),
            adsk.core.Point3D.create(width / 10.0, depth / 10.0, 0)
        )
        
        extrude_input = extrudes.createInput(
            sketch_bottom.profiles.item(0),
            adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        distance = adsk.core.ValueInput.createByReal(thickness / 10.0)
        extrude_input.setDistanceExtent(False, distance)
        extrude_bottom = extrudes.add(extrude_input)
        extrude_bottom.bodies.item(0).name = "Fondo"
        
        # BUG FIX: Move bottom panel to plinth_height if plinth exists
        if has_plinth and plinth_height > 0:
            transform_bottom = adsk.core.Matrix3D.create()
            transform_bottom.translation = adsk.core.Vector3D.create(0, 0, z_bottom)
            
            bodies_bottom = adsk.core.ObjectCollection.create()
            bodies_bottom.add(extrude_bottom.bodies.item(0))
            move_input_bottom = move_feats.createInput(bodies_bottom, transform_bottom)
            move_feats.add(move_input_bottom)
        
        # Pannello superiore (copia e sposta)
        sketch_top = sketches.add(xy_plane)
        rect_top = sketch_top.sketchCurves.sketchLines.addTwoPointRectangle(
            adsk.core.Point3D.create(0, 0, 0),
            adsk.core.Point3D.create(width / 10.0, depth / 10.0, 0)
        )
        
        extrude_input_top = extrudes.createInput(
            sketch_top.profiles.item(0),
            adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        extrude_input_top.setDistanceExtent(False, distance)
        extrude_top = extrudes.add(extrude_input_top)
        extrude_top.bodies.item(0).name = "Cielo"
        
        # BUG FIX: Move top panel to correct Z position
        if height is not None:
            effective_height = height - plinth_height if has_plinth else height
            z_top = (plinth_height + effective_height - thickness) / 10.0
            
            transform_top = adsk.core.Matrix3D.create()
            transform_top.translation = adsk.core.Vector3D.create(0, 0, z_top)
            
            bodies_top = adsk.core.ObjectCollection.create()
            bodies_top.add(extrude_top.bodies.item(0))
            move_input_top = move_feats.createInput(bodies_top, transform_top)
            move_feats.add(move_input_top)
    
    def _create_back_panel(self, component, width, height, thickness, back_thickness, has_plinth, plinth_height):
        """Crea il pannello posteriore con scasso"""
        sketches = component.sketches
        extrudes = component.features.extrudeFeatures
        move_feats = component.features.moveFeatures
        
        # Piano XZ per pannello posteriore
        xz_plane = component.xZConstructionPlane
        
        # Calcola dimensioni
        effective_height = height - plinth_height if has_plinth else height
        panel_width = width - 2 * thickness
        panel_height = effective_height - 2 * thickness
        
        # BUG FIX: Calculate Z offset for back panel
        z_offset = (plinth_height + thickness) / 10.0 if has_plinth else thickness / 10.0
        
        sketch = sketches.add(xz_plane)
        rect = sketch.sketchCurves.sketchLines.addTwoPointRectangle(
            adsk.core.Point3D.create(thickness / 10.0, z_offset, 0),
            adsk.core.Point3D.create((thickness + panel_width) / 10.0, z_offset + panel_height / 10.0, 0)
        )
        
        extrude_input = extrudes.createInput(
            sketch.profiles.item(0),
            adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        distance = adsk.core.ValueInput.createByReal(back_thickness / 10.0)
        # BUG FIX: Extrude toward rear (positive direction from XZ plane means toward front, so we keep it positive)
        extrude_input.setDistanceExtent(False, distance)
        extrude_back = extrudes.add(extrude_input)
        extrude_back.bodies.item(0).name = "Retro"
    
    def _create_plinth(self, component, width, depth, thickness, plinth_height):
        """Crea lo zoccolo"""
        sketches = component.sketches
        extrudes = component.features.extrudeFeatures
        
        # Piano XY per zoccolo
        xy_plane = component.xYConstructionPlane
        
        # Profilo a U dello zoccolo
        sketch = sketches.add(xy_plane)
        lines = sketch.sketchCurves.sketchLines
        
        # Crea profilo U (fronte + 2 lati)
        # Fronte
        p1 = adsk.core.Point3D.create(0, 0, 0)
        p2 = adsk.core.Point3D.create(width / 10.0, 0, 0)
        p3 = adsk.core.Point3D.create(width / 10.0, (thickness * 2) / 10.0, 0)
        p4 = adsk.core.Point3D.create(0, (thickness * 2) / 10.0, 0)
        
        lines.addByTwoPoints(p1, p2)
        lines.addByTwoPoints(p2, p3)
        lines.addByTwoPoints(p3, p4)
        lines.addByTwoPoints(p4, p1)
        
        extrude_input = extrudes.createInput(
            sketch.profiles.item(0),
            adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        distance = adsk.core.ValueInput.createByReal(plinth_height / 10.0)
        extrude_input.setDistanceExtent(False, distance)
        extrude_plinth = extrudes.add(extrude_input)
        extrude_plinth.bodies.item(0).name = "Zoccolo"
    
    def _create_shelves(self, component, width, depth, thickness, height, count, has_plinth, plinth_height):
        """Crea ripiani intermedi"""
        sketches = component.sketches
        extrudes = component.features.extrudeFeatures
        move_feats = component.features.moveFeatures
        
        xy_plane = component.xYConstructionPlane
        
        # Calcola spaziatura ripiani
        effective_height = height - plinth_height if has_plinth else height
        usable_height = effective_height - 2 * thickness
        spacing = usable_height / (count + 1)
        
        panel_width = width - 2 * thickness
        
        for i in range(count):
            z_position = (plinth_height if has_plinth else 0) + thickness + spacing * (i + 1)
            
            sketch = sketches.add(xy_plane)
            rect = sketch.sketchCurves.sketchLines.addTwoPointRectangle(
                adsk.core.Point3D.create(thickness / 10.0, 0, 0),
                adsk.core.Point3D.create((thickness + panel_width) / 10.0, depth / 10.0, 0)
            )
            
            extrude_input = extrudes.createInput(
                sketch.profiles.item(0),
                adsk.fusion.FeatureOperations.NewBodyFeatureOperation
            )
            distance = adsk.core.ValueInput.createByReal(thickness / 10.0)
            extrude_input.setDistanceExtent(False, distance)
            extrude_shelf = extrudes.add(extrude_input)
            extrude_shelf.bodies.item(0).name = f"Ripiano_{i+1}"
            
            # BUG FIX: Move shelf to correct Z position
            transform_shelf = adsk.core.Matrix3D.create()
            transform_shelf.translation = adsk.core.Vector3D.create(0, 0, z_position / 10.0)
            
            bodies_shelf = adsk.core.ObjectCollection.create()
            bodies_shelf.add(extrude_shelf.bodies.item(0))
            move_input_shelf = move_feats.createInput(bodies_shelf, transform_shelf)
            move_feats.add(move_input_shelf)
    
    def _create_divisions(self, component, width, height, depth, thickness, count, has_plinth, plinth_height):
        """Crea divisori verticali"""
        sketches = component.sketches
        extrudes = component.features.extrudeFeatures
        move_feats = component.features.moveFeatures
        
        yz_plane = component.yZConstructionPlane
        
        # Calcola spaziatura divisori
        usable_width = width - 2 * thickness
        spacing = usable_width / (count + 1)
        
        effective_height = height - plinth_height if has_plinth else height
        panel_height = effective_height - 2 * thickness
        
        # BUG FIX: Calculate Z offset for dividers
        z_offset = (plinth_height + thickness) / 10.0 if has_plinth else thickness / 10.0
        
        for i in range(count):
            x_position = thickness + spacing * (i + 1)
            
            sketch = sketches.add(yz_plane)
            rect = sketch.sketchCurves.sketchLines.addTwoPointRectangle(
                adsk.core.Point3D.create(0, z_offset, 0),
                adsk.core.Point3D.create(depth / 10.0, z_offset + panel_height / 10.0, 0)
            )
            
            extrude_input = extrudes.createInput(
                sketch.profiles.item(0),
                adsk.fusion.FeatureOperations.NewBodyFeatureOperation
            )
            distance = adsk.core.ValueInput.createByReal(thickness / 10.0)
            extrude_input.setDistanceExtent(False, distance)
            extrude_div = extrudes.add(extrude_input)
            extrude_div.bodies.item(0).name = f"Divisorio_{i+1}"
            
            # BUG FIX: Move divider to correct X position
            transform_div = adsk.core.Matrix3D.create()
            transform_div.translation = adsk.core.Vector3D.create(x_position / 10.0, 0, 0)
            
            bodies_div = adsk.core.ObjectCollection.create()
            bodies_div.add(extrude_div.bodies.item(0))
            move_input_div = move_feats.createInput(bodies_div, transform_div)
            move_feats.add(move_input_div)
