"""
Cabinet Generator - Professional furniture carcass creation with parametric design

Complete system for creating parametric cabinets with professional machining features
including door/hinge parameters, back mounting options, and adjustable shelf systems.
"""

import adsk.core
import adsk.fusion
import math

# Unit conversion constant: Fusion 360 uses cm internally
MM_TO_CM = 10.0

class CabinetGenerator:
    """Generatore parametrico di mobili con sistema di foratura e lavorazioni professionali"""
    
    # Door and hinge defaults (Blum Clip-top 110° with spring)
    DEFAULT_DOOR_GAP = 2.0  # mm
    DEFAULT_DOOR_OVERLAY_LEFT = 18.0  # mm
    DEFAULT_DOOR_OVERLAY_RIGHT = 18.0  # mm
    DEFAULT_DOOR_OVERLAY_TOP = 18.0  # mm
    DEFAULT_DOOR_OVERLAY_BOTTOM = 18.0  # mm
    DEFAULT_DOOR_THICKNESS = 18.0  # mm
    
    # Hinge preset: Blum Clip-top 110°
    DEFAULT_HINGE_TYPE = "clip_top_110"
    DEFAULT_CUP_DIAMETER = 35.0  # mm
    DEFAULT_CUP_DEPTH = 12.5  # mm
    DEFAULT_CUP_CENTER_OFFSET_FROM_EDGE = 21.5  # mm (K dimension)
    DEFAULT_HINGE_OFFSET_TOP = 100.0  # mm from top edge to center
    DEFAULT_HINGE_OFFSET_BOTTOM = 100.0  # mm from bottom edge to center
    DEFAULT_MOUNTING_PLATE_SYSTEM_LINE = 37.0  # mm (System 32 standard)
    DEFAULT_MOUNTING_PLATE_HOLE_SPACING = 32.0  # mm (vertical interaxis)
    DEFAULT_MOUNTING_PLATE_HOLE_DIAMETER = 5.0  # mm
    DEFAULT_SCREW_DEPTH = 13.0  # mm for euro-screw 5×13
    
    # Auto hinge count thresholds
    DEFAULT_HINGE_THRESHOLD_2 = 900.0  # mm - 2 hinges for height ≤ 900
    DEFAULT_HINGE_THRESHOLD_3 = 1500.0  # mm - 3 hinges for 900-1500
    # 4+ hinges for > 1500 mm
    
    # Back mounting defaults
    DEFAULT_BACK_MOUNTING = "flush_rabbet"  # or "groove" or "surface"
    DEFAULT_RABBET_WIDTH = 12.0  # mm
    DEFAULT_GROOVE_WIDTH_TOLERANCE = 0.5  # mm (added to back_thickness)
    DEFAULT_GROOVE_OFFSET_FROM_REAR = 10.0  # mm
    
    # Shelves defaults
    DEFAULT_SHELF_FRONT_SETBACK = 3.0  # mm
    DEFAULT_SHELF_BORE_ENABLED = False
    DEFAULT_SHELF_BORE_DIAMETER = 5.0  # mm
    DEFAULT_SHELF_BORE_FRONT_DISTANCE = 37.0  # mm
    DEFAULT_SHELF_BORE_PATTERN = 32.0  # mm
    
    # Dowel/Joinery defaults
    DEFAULT_DOWELS_ENABLED = False
    DEFAULT_DOWEL_DIAMETER = 8.0  # mm
    DEFAULT_DOWEL_EDGE_DISTANCE = 35.0  # mm
    DEFAULT_DOWEL_SPACING = 64.0  # mm (multiple of 32mm)
    
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
                - back_mounting: Tipo montaggio retro ('flush_rabbet', 'groove', 'surface', default 'flush_rabbet')
                - rabbet_width: Larghezza scasso (mm, default 12)
                - rabbet_depth: Profondità scasso (mm, default = back_thickness)
                - groove_width: Larghezza cava (mm, default = back_thickness + 0.5)
                - groove_depth: Profondità cava (mm, default = back_thickness)
                - groove_offset_from_rear: Distanza dalla faccia posteriore (mm, default 10)
                - has_plinth: Include zoccolo (bool, default True)
                - plinth_height: Altezza zoccolo (mm, default 100)
                - shelves_count: Numero ripiani (int, default 0)
                - shelf_front_setback: Rientro ripiani dal fronte (mm, default 3)
                - shelf_bore_enabled: Abilita fori per ripiani regolabili (bool, default False)
                - shelf_bore_diameter: Diametro fori ripiani (mm, default 5)
                - shelf_bore_front_distance: Distanza fori dal fronte (mm, default 37)
                - shelf_bore_pattern: Passo fori ripiani (mm, default 32)
                - divisions_count: Numero divisori verticali (int, default 0)
                - has_door: Include anta (bool, default False)
                - door_gap: Spazio tra ante (mm, default 2)
                - door_overlay_left: Sovrapposizione sinistra (mm, default 18)
                - door_overlay_right: Sovrapposizione destra (mm, default 18)
                - door_overlay_top: Sovrapposizione superiore (mm, default 18)
                - door_overlay_bottom: Sovrapposizione inferiore (mm, default 18)
                - door_thickness: Spessore anta (mm, default 18)
                - hinge_type: Tipo cerniera (default 'clip_top_110')
                - cup_diameter: Diametro tazza cerniera (mm, default 35)
                - cup_depth: Profondità tazza (mm, default 12.5)
                - cup_center_offset_from_edge: Offset K tazza dal bordo (mm, default 21.5)
                - hinge_offset_top: Distanza prima cerniera dal top (mm, default 100)
                - hinge_offset_bottom: Distanza ultima cerniera dal bottom (mm, default 100)
                - mounting_plate_system_line: Linea sistema piastra (mm, default 37)
                - mounting_plate_hole_spacing: Passo fori piastra (mm, default 32)
                - mounting_plate_hole_diameter: Diametro fori piastra (mm, default 5)
                - dowels_enabled: Abilita spinotti (bool, default False)
                - dowel_diameter: Diametro spinotto (mm, default 8)
                - dowel_edge_distance: Distanza spinotto dal bordo (mm, default 35)
                - dowel_spacing: Passo spinotti (mm, default 64)
        
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
        back_mounting = params.get('back_mounting', self.DEFAULT_BACK_MOUNTING)
        rabbet_width = params.get('rabbet_width', self.DEFAULT_RABBET_WIDTH)
        rabbet_depth = params.get('rabbet_depth', back_thickness)
        groove_width = params.get('groove_width', back_thickness + self.DEFAULT_GROOVE_WIDTH_TOLERANCE)
        groove_depth = params.get('groove_depth', back_thickness)
        groove_offset = params.get('groove_offset_from_rear', self.DEFAULT_GROOVE_OFFSET_FROM_REAR)
        has_plinth = params.get('has_plinth', True)
        plinth_height = params.get('plinth_height', 100)
        shelves_count = params.get('shelves_count', 0)
        shelf_front_setback = params.get('shelf_front_setback', self.DEFAULT_SHELF_FRONT_SETBACK)
        shelf_bore_enabled = params.get('shelf_bore_enabled', self.DEFAULT_SHELF_BORE_ENABLED)
        divisions_count = params.get('divisions_count', 0)
        has_door = params.get('has_door', False)
        door_gap = params.get('door_gap', self.DEFAULT_DOOR_GAP)
        door_overlay_left = params.get('door_overlay_left', self.DEFAULT_DOOR_OVERLAY_LEFT)
        door_overlay_right = params.get('door_overlay_right', self.DEFAULT_DOOR_OVERLAY_RIGHT)
        door_overlay_top = params.get('door_overlay_top', self.DEFAULT_DOOR_OVERLAY_TOP)
        door_overlay_bottom = params.get('door_overlay_bottom', self.DEFAULT_DOOR_OVERLAY_BOTTOM)
        door_thickness = params.get('door_thickness', self.DEFAULT_DOOR_THICKNESS)
        
        # Store params for later use
        self._params = params
        
        # Nuovi parametri professionali - raggruppati per chiarezza
        back_mounting = params.get('back_mounting', 'flush_rabbet')
        rabbet_width = params.get('rabbet_width', 12)
        rabbet_depth = params.get('rabbet_depth', back_thickness)
        groove_width = params.get('groove_width', back_thickness + 0.5)
        groove_depth = params.get('groove_depth', back_thickness)
        groove_offset_from_rear = params.get('groove_offset_from_rear', 10)
        shelf_front_setback = params.get('shelf_front_setback', 3)
        
        # Parametri spinatura/foratura
        dowels_enabled = params.get('dowels_enabled', False)
        dowel_diameter = params.get('dowel_diameter', 8)
        dowel_edge_distance = params.get('dowel_edge_distance', 37)
        dowel_spacing = params.get('dowel_spacing', 32)
        
        # Parametri ante (placeholders per uso futuro)
        door_overlay_left = params.get('door_overlay_left', 0)
        door_overlay_right = params.get('door_overlay_right', 0)
        door_overlay_top = params.get('door_overlay_top', 0)
        door_overlay_bottom = params.get('door_overlay_bottom', 0)
        door_gap = params.get('door_gap', 2)
        
        # Crea il componente principale
        occurrence = self.root_comp.occurrences.addNewComponent(
            adsk.core.Matrix3D.create()
        )
        cabinet_comp = occurrence.component
        cabinet_comp.name = f"Mobile_{int(width)}x{int(height)}x{int(depth)}"
        
        # Crea i parametri utente
        self._create_user_parameters(cabinet_comp, params)
        
        # Calculate back panel inset for shelf depth calculation
        back_inset = self._calculate_back_inset(back_mounting, thickness, back_thickness, 
                                                  rabbet_width, groove_offset)
        
        # Crea i pannelli principali
        self._create_side_panels(cabinet_comp, width, height, depth, thickness, has_plinth, plinth_height)
        self._create_top_bottom_panels(cabinet_comp, width, depth, thickness, height, has_plinth, plinth_height, 
                                       back_inset, back_mounting)
        
        # Aggiungi pannello posteriore se richiesto
        if has_back:
            self._create_back_panel(cabinet_comp, width, height, thickness, back_thickness, has_plinth, 
                                    plinth_height, back_mounting, rabbet_width, rabbet_depth, 
                                    groove_width, groove_depth, groove_offset, depth)
        
        # Aggiungi zoccolo se richiesto
        if has_plinth:
            self._create_plinth(cabinet_comp, width, depth, thickness, plinth_height)
        
        # Aggiungi ripiani
        if shelves_count > 0:
            self._create_shelves(cabinet_comp, width, depth, thickness, height, shelves_count, has_plinth, 
                                plinth_height, shelf_front_setback, back_inset, back_mounting)
        
        # Aggiungi divisori verticali
        if divisions_count > 0:
            self._create_divisions(cabinet_comp, width, height, depth, thickness, divisions_count, has_plinth, plinth_height)
        
        # Aggiungi anta se richiesta
        if has_door:
            self._create_door_panel(cabinet_comp, width, height, depth, thickness, has_plinth, plinth_height,
                                   door_gap, door_overlay_left, door_overlay_right, door_overlay_top,
                                   door_overlay_bottom, door_thickness, params)
        
        return cabinet_comp
    
    def _calculate_back_inset(self, back_mounting, thickness, back_thickness, rabbet_width, groove_offset):
        """
        Calcola quanto il retro è rientrato rispetto alla profondità totale
        
        Args:
            back_mounting: Tipo di montaggio ('flush_rabbet', 'groove', 'surface')
            thickness: Spessore pannelli laterali (mm)
            back_thickness: Spessore retro (mm)
            rabbet_width: Larghezza scasso (mm)
            groove_offset: Distanza cava dal retro (mm)
        
        Returns:
            float: Rientro retro in mm
        
        Raises:
            ValueError: If back_mounting type is not recognized
        """
        if back_mounting == 'flush_rabbet':
            # Retro a filo con scasso: rientra di rabbet_width
            return rabbet_width
        elif back_mounting == 'groove':
            # Retro in cava: rientra di groove_offset
            return groove_offset
        elif back_mounting == 'surface':
            # Retro in superficie: a filo con il retro
            return 0
        else:
            # Unrecognized back_mounting type
            if self.logger:
                self.logger.warning(f"Unrecognized back_mounting type '{back_mounting}', defaulting to 'flush_rabbet'")
            # Default to flush_rabbet for backward compatibility
            return rabbet_width
    
    def _create_user_parameters(self, component, params):
        """
        Crea parametri utente per il mobile
        
        Args:
            component: Componente Fusion
            params: Dizionario parametri
        """
        user_params = component.parentDesign.userParameters
        
        # Parametri dimensionali base
        param_list = [
            ('Larghezza', params.get('width', 800), 'mm'),
            ('Altezza', params.get('height', 720), 'mm'),
            ('Profondita', params.get('depth', 580), 'mm'),
            ('Spessore', params.get('material_thickness', 18), 'mm'),
            ('SpessoreRetro', params.get('back_thickness', 3), 'mm'),
            ('AltezzaZoccolo', params.get('plinth_height', 100), 'mm'),
            # Door parameters
            ('DoorGap', params.get('door_gap', self.DEFAULT_DOOR_GAP), 'mm'),
            ('DoorOverlayLeft', params.get('door_overlay_left', self.DEFAULT_DOOR_OVERLAY_LEFT), 'mm'),
            ('DoorOverlayRight', params.get('door_overlay_right', self.DEFAULT_DOOR_OVERLAY_RIGHT), 'mm'),
            ('DoorOverlayTop', params.get('door_overlay_top', self.DEFAULT_DOOR_OVERLAY_TOP), 'mm'),
            ('DoorOverlayBottom', params.get('door_overlay_bottom', self.DEFAULT_DOOR_OVERLAY_BOTTOM), 'mm'),
            ('DoorThickness', params.get('door_thickness', self.DEFAULT_DOOR_THICKNESS), 'mm'),
            # Hinge parameters
            ('CupDiameter', params.get('cup_diameter', self.DEFAULT_CUP_DIAMETER), 'mm'),
            ('CupDepth', params.get('cup_depth', self.DEFAULT_CUP_DEPTH), 'mm'),
            ('CupOffsetFromEdge', params.get('cup_center_offset_from_edge', self.DEFAULT_CUP_CENTER_OFFSET_FROM_EDGE), 'mm'),
            ('HingeOffsetTop', params.get('hinge_offset_top', self.DEFAULT_HINGE_OFFSET_TOP), 'mm'),
            ('HingeOffsetBottom', params.get('hinge_offset_bottom', self.DEFAULT_HINGE_OFFSET_BOTTOM), 'mm'),
            ('MountingPlateSystemLine', params.get('mounting_plate_system_line', self.DEFAULT_MOUNTING_PLATE_SYSTEM_LINE), 'mm'),
            ('MountingPlateHoleSpacing', params.get('mounting_plate_hole_spacing', self.DEFAULT_MOUNTING_PLATE_HOLE_SPACING), 'mm'),
            ('MountingPlateHoleDiameter', params.get('mounting_plate_hole_diameter', self.DEFAULT_MOUNTING_PLATE_HOLE_DIAMETER), 'mm'),
            # Back mounting parameters
            ('RabbetWidth', params.get('rabbet_width', self.DEFAULT_RABBET_WIDTH), 'mm'),
            ('GrooveOffsetFromRear', params.get('groove_offset_from_rear', self.DEFAULT_GROOVE_OFFSET_FROM_REAR), 'mm'),
            # Shelf parameters
            ('ShelfFrontSetback', params.get('shelf_front_setback', self.DEFAULT_SHELF_FRONT_SETBACK), 'mm'),
            ('ShelfBoreDiameter', params.get('shelf_bore_diameter', self.DEFAULT_SHELF_BORE_DIAMETER), 'mm'),
            ('ShelfBoreFrontDistance', params.get('shelf_bore_front_distance', self.DEFAULT_SHELF_BORE_FRONT_DISTANCE), 'mm'),
            ('ShelfBorePattern', params.get('shelf_bore_pattern', self.DEFAULT_SHELF_BORE_PATTERN), 'mm'),
            # Dowel parameters
            ('DowelDiameter', params.get('dowel_diameter', self.DEFAULT_DOWEL_DIAMETER), 'mm'),
            ('DowelEdgeDistance', params.get('dowel_edge_distance', self.DEFAULT_DOWEL_EDGE_DISTANCE), 'mm'),
            ('DowelSpacing', params.get('dowel_spacing', self.DEFAULT_DOWEL_SPACING), 'mm'),
        ]
        
        for name, value, unit in param_list:
            value_input = adsk.core.ValueInput.createByReal(value / MM_TO_CM)  # Converti mm in cm
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
        # Convert to cm for Fusion 360 internal units
        z_start = plinth_height / MM_TO_CM if has_plinth else 0  # cm
        
        # Pannello sinistro
        sketch_left = sketches.add(yz_plane)
        rect_left = sketch_left.sketchCurves.sketchLines.addTwoPointRectangle(
            adsk.core.Point3D.create(0, z_start, 0),  # z_start is in cm
            adsk.core.Point3D.create(depth / MM_TO_CM, z_start + effective_height / MM_TO_CM, 0)  # All in cm
        )
        
        extrude_input = extrudes.createInput(
            sketch_left.profiles.item(0),
            adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        distance = adsk.core.ValueInput.createByReal(thickness / MM_TO_CM)
        extrude_input.setDistanceExtent(False, distance)
        extrude_left = extrudes.add(extrude_input)
        extrude_left.bodies.item(0).name = "Fianco_Sinistro"
        
        # Pannello destro (offset in X)
        sketch_right = sketches.add(yz_plane)
        rect_right = sketch_right.sketchCurves.sketchLines.addTwoPointRectangle(
            adsk.core.Point3D.create(0, z_start, 0),
            adsk.core.Point3D.create(depth / MM_TO_CM, z_start + effective_height / MM_TO_CM, 0)
        )
        
        # Transform per posizionare a destra
        transform_right = adsk.core.Matrix3D.create()
        transform_right.translation = adsk.core.Vector3D.create((width - thickness) / MM_TO_CM, 0, 0)
        
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
    """
    Crea i pannelli superiore (Cielo) e inferiore (Fondo) allineati ai fianchi:
    - Sketch su YZ
    - Estrusione lungo X pari alla larghezza interna (W_in)
    """
    sketches = component.sketches
    extrudes = component.features.extrudeFeatures

    yz_plane = component.yZConstructionPlane

    # Larghezza interna (X)
    W_in = width - 2 * thickness

    # Quote Z
    Z_bottom = plinth_height  # mm
    Z_bottom_cm = Z_bottom / 10.0
    if height is not None:
        H_eff = height - plinth_height  # mm
        Z_top = plinth_height + H_eff - thickness  # mm
        Z_top_cm = Z_top / 10.0

    # Fondo: profilo depth × thickness su YZ, a Z = plinth_height
    sketch_bottom = sketches.add(yz_plane)
    rect_bottom = sketch_bottom.sketchCurves.sketchLines.addTwoPointRectangle(
        adsk.core.Point3D.create(0, Z_bottom_cm, 0),
        adsk.core.Point3D.create(depth / 10.0, (Z_bottom + thickness) / 10.0, 0)
    )
    extrude_input_bottom = extrudes.createInput(
        sketch_bottom.profiles.item(0),
        adsk.fusion.FeatureOperations.NewBodyFeatureOperation
    )
    extrude_input_bottom.setDistanceExtent(
        False,
        adsk.core.ValueInput.createByReal(W_in / 10.0)
    )
    extrude_bottom = extrudes.add(extrude_input_bottom)
    body_bottom = extrude_bottom.bodies.item(0)
    body_bottom.name = "Fondo"

    # Cielo: profilo depth × thickness su YZ, a Z = plinth_height + H_eff - thickness
    if height is not None:
        sketch_top = sketches.add(yz_plane)
        rect_top = sketch_top.sketchCurves.sketchLines.addTwoPointRectangle(
            adsk.core.Point3D.create(0, Z_top_cm, 0),
            adsk.core.Point3D.create(depth / 10.0, (Z_top + thickness) / 10.0, 0)
        )
        extrude_input_top = extrudes.createInput(
            sketch_top.profiles.item(0),
            adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        extrude_input_top.setDistanceExtent(
            False,
            adsk.core.ValueInput.createByReal(W_in / 10.0)
        )
        extrude_top = extrudes.add(extrude_input_top)
        body_top = extrude_top.bodies.item(0)
        body_top.name = "Cielo""
    
    def _create_back_panel(self, component, width, height, thickness, back_thickness, has_plinth, 
                          plinth_height, back_mounting='flush_rabbet', rabbet_width=12, rabbet_depth=3,
                          groove_width=3.5, groove_depth=3, groove_offset=10, depth=580):
        """
        Crea il pannello posteriore con supporto per diversi tipi di montaggio
        
        Args:
            back_mounting: 'flush_rabbet' (scasso a filo), 'groove' (cava), 'surface' (superficie)
            depth: Profondità mobile (mm) - necessario per calcolo posizione Y
        """
        sketches = component.sketches
        extrudes = component.features.extrudeFeatures
        move_feats = component.features.moveFeatures
        
        # Piano YZ per pannello posteriore - consistente con altri pannelli
        yz_plane = component.yZConstructionPlane
        
        # Calcola dimensioni
        effective_height = height - plinth_height if has_plinth else height
        panel_width = width - 2 * thickness
        panel_height = effective_height - 2 * thickness
        
        # BUG FIX: Calculate Z offset for back panel
        z_offset = (plinth_height + thickness) / MM_TO_CM if has_plinth else thickness / MM_TO_CM
        
        # Calculate Y position based on mounting type
        if back_mounting == 'flush_rabbet':
            # Retro a filo: posizionato a depth - rabbet_width
            y_position = (depth - rabbet_width) / MM_TO_CM
        elif back_mounting == 'groove':
            # Retro in cava: posizionato a depth - groove_offset
            y_position = (depth - groove_offset) / MM_TO_CM
        elif back_mounting == 'surface':
            # Retro in superficie: a filo con il retro
            y_position = (depth - back_thickness) / MM_TO_CM
        else:
            # Default: flush_rabbet
            y_position = (depth - rabbet_width) / MM_TO_CM
        
        sketch = sketches.add(yz_plane)
        rect = sketch.sketchCurves.sketchLines.addTwoPointRectangle(
            adsk.core.Point3D.create(y_position, z_offset, 0),
            adsk.core.Point3D.create(y_position + back_thickness / MM_TO_CM, 
                                    z_offset + panel_height / MM_TO_CM, 0)
        )
        
        # Estrudi lungo X per la larghezza tra i fianchi
        extrude_input = extrudes.createInput(
            sketch.profiles.item(0),
            adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        distance = adsk.core.ValueInput.createByReal(panel_width / MM_TO_CM)
        extrude_input.setDistanceExtent(False, distance)
        extrude_back = extrudes.add(extrude_input)
        extrude_back.bodies.item(0).name = "Retro"
        
        # Move to correct X position (after side panel thickness)
        transform_back = adsk.core.Matrix3D.create()
        transform_back.translation = adsk.core.Vector3D.create(thickness / MM_TO_CM, 0, 0)
        
        bodies_back = adsk.core.ObjectCollection.create()
        bodies_back.add(extrude_back.bodies.item(0))
        move_input_back = move_feats.createInput(bodies_back, transform_back)
        move_feats.add(move_input_back)
        
        # TODO: Implementare lavorazioni per scassi/cave sui pannelli laterali/top/bottom
        # Placeholder per feature di machining (rabbet/groove cuts)
        if back_mounting == 'flush_rabbet':
            # Crea scasso sui pannelli laterali, top e bottom
            self._create_rabbet_cuts(component, width, height, depth, thickness, has_plinth, 
                                    plinth_height, rabbet_width, rabbet_depth)
        elif back_mounting == 'groove':
            # Crea cava sui pannelli laterali
            self._create_groove_cuts(component, width, height, depth, thickness, has_plinth,
                                    plinth_height, groove_width, groove_depth, groove_offset)
    
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
        p2 = adsk.core.Point3D.create(width / MM_TO_CM, 0, 0)
        p3 = adsk.core.Point3D.create(width / MM_TO_CM, (thickness * 2) / MM_TO_CM, 0)
        p4 = adsk.core.Point3D.create(0, (thickness * 2) / MM_TO_CM, 0)
        
        lines.addByTwoPoints(p1, p2)
        lines.addByTwoPoints(p2, p3)
        lines.addByTwoPoints(p3, p4)
        lines.addByTwoPoints(p4, p1)
        
        extrude_input = extrudes.createInput(
            sketch.profiles.item(0),
            adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        distance = adsk.core.ValueInput.createByReal(plinth_height / MM_TO_CM)
        extrude_input.setDistanceExtent(False, distance)
        extrude_plinth = extrudes.add(extrude_input)
        extrude_plinth.bodies.item(0).name = "Zoccolo"
    
    def _create_shelves(self, component, width, depth, thickness, height, count, has_plinth, plinth_height, params=None):
    """
    Crea ripiani su YZ con estrusione lungo X = W_in.
    Considera rientro frontale e arretramento dovuto allo schienale.
    """
    sketches = component.sketches
    extrudes = component.features.extrudeFeatures

    yz_plane = component.yZConstructionPlane

    W_in = width - 2 * thickness
    H_eff = height - plinth_height

    # Parametri
    shelf_front_setback = (params or {}).get('shelf_front_setback', 3)  # mm default
    back_mounting = (params or {}).get('back_mounting', 'flush_rabbet')
    back_thickness = (params or {}).get('back_thickness', thickness)
    groove_offset = (params or {}).get('groove_offset_from_rear', 10)  # mm

    # arretramento posteriore del fronte utile
    if back_mounting == 'flush_rabbet':
        back_inset = 0
    elif back_mounting == 'groove':
        back_inset = groove_offset
    else:
        # surface (applicata in superficie dietro i fianchi): arretra di spessore schiena
        back_inset = back_thickness

    shelf_depth_eff = depth - back_inset - shelf_front_setback

    usable_height = H_eff - 2 * thickness
    spacing = usable_height / (count + 1)

    for i in range(count):
        Z_pos_mm = plinth_height + thickness + spacing * (i + 1)
        Z_pos_cm = Z_pos_mm / 10.0

        # Profilo ripiano su YZ
        sketch = sketches.add(yz_plane)
        rect = sketch.sketchCurves.sketchLines.addTwoPointRectangle(
            adsk.core.Point3D.create(shelf_front_setback / 10.0, Z_pos_cm, 0),
            adsk.core.Point3D.create((shelf_front_setback + shelf_depth_eff) / 10.0, (Z_pos_mm + thickness) / 10.0, 0)
        )

        extrude_input_shelf = extrudes.createInput(
            sketch.profiles.item(0),
            adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        extrude_input_shelf.setDistanceExtent(
            False,
            adsk.core.ValueInput.createByReal(W_in / 10.0)
        )
        extrude_shelf = extrudes.add(extrude_input_shelf)
        shelf_body = extrude_shelf.bodies.item(0)
        shelf_body.name = f"Ripiano_{i+1}"
    
    def _create_rabbet_cuts(self, component, width, height, depth, thickness, back_thickness,
                           has_plinth, plinth_height, rabbet_width, rabbet_depth):
        """
        Crea tagli per battuta (rabbet) sui bordi posteriori interni dei fianchi
        
        Placeholder per lavorazioni 3D future
        La battuta è un taglio rettangolare sul bordo posteriore interno per alloggiare il retro
        """
        # TODO: Implementare tagli extrude-cut sui fianchi
        # Battuta larghezza=rabbet_width, profondità=rabbet_depth
        # Posizione: bordo posteriore interno dei pannelli laterali
        pass
    
    def _create_groove_cuts(self, component, width, height, depth, thickness, back_thickness,
                           has_plinth, plinth_height, groove_width, groove_depth, groove_offset_from_rear):
        """
        Crea tagli per canale (groove) sulle facce interne dei fianchi
        
        Placeholder per lavorazioni 3D future
        Il canale è una tasca fresata sulla faccia interna per alloggiare il retro
        """
        # TODO: Implementare tagli pocket (fresata) sui fianchi
        # Canale larghezza=groove_width, profondità=groove_depth
        # Offset da bordo posteriore=groove_offset_from_rear
        pass
    
    def _create_dowel_holes(self, component, width, height, depth, thickness, has_plinth, plinth_height,
                           dowel_diameter, dowel_edge_distance, dowel_spacing):
        """
        Crea forature per spinatura (dowel holes) tra fondo/cielo e fianchi
        
        Placeholder per lavorazioni 3D future con sistema 32mm
        
        Args:
            dowel_diameter: Diametro tassello (mm, tipicamente 8)
            dowel_edge_distance: Distanza dal bordo (mm, tipicamente 37)
            dowel_spacing: Spaziatura tra fori (mm, tipicamente 32 per sistema 32mm)
        """
        # TODO: Implementare fori extrude-cut per spinatura
        # Pattern: sistema 32mm standard
        # Posizioni: fondo e cielo nei fianchi
        # Può essere integrato con fusion_addin/lib/joinery in futuro
        pass
    
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
        z_offset = (plinth_height + thickness) / MM_TO_CM if has_plinth else thickness / MM_TO_CM
        
        for i in range(count):
            x_position = thickness + spacing * (i + 1)
            
            sketch = sketches.add(yz_plane)
            rect = sketch.sketchCurves.sketchLines.addTwoPointRectangle(
                adsk.core.Point3D.create(0, z_offset, 0),
                adsk.core.Point3D.create(depth / MM_TO_CM, z_offset + panel_height / MM_TO_CM, 0)
            )
            
            extrude_input = extrudes.createInput(
                sketch.profiles.item(0),
                adsk.fusion.FeatureOperations.NewBodyFeatureOperation
            )
            distance = adsk.core.ValueInput.createByReal(thickness / MM_TO_CM)
            extrude_input.setDistanceExtent(False, distance)
            extrude_div = extrudes.add(extrude_input)
            extrude_div.bodies.item(0).name = f"Divisorio_{i+1}"
            
            # Move divider to correct X position
            transform_div = adsk.core.Matrix3D.create()
            transform_div.translation = adsk.core.Vector3D.create(x_position / MM_TO_CM, 0, 0)
            
            bodies_div = adsk.core.ObjectCollection.create()
            bodies_div.add(extrude_div.bodies.item(0))
            move_input_div = move_feats.createInput(bodies_div, transform_div)
            move_feats.add(move_input_div)
    
    def _create_door_panel(self, component, width, height, depth, thickness, has_plinth, plinth_height,
                          door_gap, door_overlay_left, door_overlay_right, door_overlay_top,
                          door_overlay_bottom, door_thickness, params):
        """
        Crea pannello anta con overlay e gap
        
        Args:
            component: Componente mobile
            width: Larghezza totale mobile (mm)
            height: Altezza totale mobile (mm)
            depth: Profondità mobile (mm)
            thickness: Spessore pannelli laterali (mm)
            has_plinth: Se ha zoccolo
            plinth_height: Altezza zoccolo (mm)
            door_gap: Spazio tra ante (mm)
            door_overlay_*: Sovrapposizioni (mm)
            door_thickness: Spessore anta (mm)
            params: Parametri originali per hinge machining
        """
        sketches = component.sketches
        extrudes = component.features.extrudeFeatures
        move_feats = component.features.moveFeatures
        
        # Calculate carcass opening dimensions
        effective_height = height - plinth_height if has_plinth else height
        internal_width = width - 2 * thickness
        
        # Calculate door dimensions from opening with overlay
        door_width = internal_width + door_overlay_left + door_overlay_right
        door_height = effective_height + door_overlay_top + door_overlay_bottom
        
        # Calculate door position
        # X: starts at left edge minus overlay
        x_door = -door_overlay_left / MM_TO_CM
        # Y: at front of cabinet (depth), extending forward by door_thickness
        y_door = depth / MM_TO_CM
        # Z: starts at plinth minus overlay
        z_door = (plinth_height - door_overlay_bottom) / MM_TO_CM if has_plinth else -door_overlay_bottom / MM_TO_CM
        
        # Create door on YZ plane
        yz_plane = component.yZConstructionPlane
        sketch_door = sketches.add(yz_plane)
        rect_door = sketch_door.sketchCurves.sketchLines.addTwoPointRectangle(
            adsk.core.Point3D.create(y_door, z_door, 0),
            adsk.core.Point3D.create(y_door + door_thickness / MM_TO_CM, 
                                    z_door + door_height / MM_TO_CM, 0)
        )
        
        extrude_input = extrudes.createInput(
            sketch_door.profiles.item(0),
            adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        distance = adsk.core.ValueInput.createByReal(door_width / MM_TO_CM)
        extrude_input.setDistanceExtent(False, distance)
        extrude_door = extrudes.add(extrude_input)
        extrude_door.bodies.item(0).name = "Anta"
        
        # Move door to correct X position
        transform_door = adsk.core.Matrix3D.create()
        transform_door.translation = adsk.core.Vector3D.create(x_door, 0, 0)
        
        bodies_door = adsk.core.ObjectCollection.create()
        bodies_door.add(extrude_door.bodies.item(0))
        move_input_door = move_feats.createInput(bodies_door, transform_door)
        move_feats.add(move_input_door)
        
        # Add hinge cup holes to door
        door_body = extrude_door.bodies.item(0)
        self._create_hinge_cup_holes(component, door_body, door_height, door_thickness, params)
        
        # Add mounting plate holes to side panels
        # Find left side panel body
        for body in component.bRepBodies:
            if body.name == "Fianco_Sinistro":
                self._create_mounting_plate_holes(component, body, effective_height, depth, thickness, 
                                                  has_plinth, plinth_height, params)
                break
    
    def _calculate_hinge_count(self, door_height):
        """
        Calcola numero automatico di cerniere in base all'altezza anta
        
        Args:
            door_height: Altezza anta (mm)
        
        Returns:
            int: Numero di cerniere
        """
        if door_height <= self.DEFAULT_HINGE_THRESHOLD_2:
            return 2
        elif door_height <= self.DEFAULT_HINGE_THRESHOLD_3:
            return 3
        else:
            return 4
    
    def _create_hinge_cup_holes(self, component, door_body, door_height, door_thickness, params):
        """
        Crea fori tazza cerniera sull'anta
        
        Args:
            component: Componente mobile
            door_body: Body dell'anta
            door_height: Altezza anta (mm)
            door_thickness: Spessore anta (mm)
            params: Parametri configurazione cerniera
        
        Note:
            This is a placeholder method. Actual hole drilling will be implemented
            in a future update using Fusion 360's holeFeatures API. The method
            calculates positions for future use.
        
        TODO: Implement actual hole drilling using component.features.holeFeatures
              Each hole should be: diameter = cup_diameter, depth = cup_depth,
              centerline at K offset from edge
        """
        # Get hinge parameters
        cup_diameter = params.get('cup_diameter', self.DEFAULT_CUP_DIAMETER)
        cup_depth = params.get('cup_depth', self.DEFAULT_CUP_DEPTH)
        cup_offset_k = params.get('cup_center_offset_from_edge', self.DEFAULT_CUP_CENTER_OFFSET_FROM_EDGE)
        hinge_offset_top = params.get('hinge_offset_top', self.DEFAULT_HINGE_OFFSET_TOP)
        hinge_offset_bottom = params.get('hinge_offset_bottom', self.DEFAULT_HINGE_OFFSET_BOTTOM)
        
        # Calculate hinge count
        hinge_count = self._calculate_hinge_count(door_height)
        
        # Calculate hinge positions along door height
        hinge_positions = []
        if hinge_count == 2:
            hinge_positions = [hinge_offset_top, door_height - hinge_offset_bottom]
        elif hinge_count == 3:
            middle = door_height / 2.0
            hinge_positions = [hinge_offset_top, middle, door_height - hinge_offset_bottom]
        elif hinge_count == 4:
            spacing = (door_height - hinge_offset_top - hinge_offset_bottom) / 3.0
            hinge_positions = [
                hinge_offset_top,
                hinge_offset_top + spacing,
                hinge_offset_top + 2 * spacing,
                door_height - hinge_offset_bottom
            ]
        
        # Store calculated positions for future implementation
        # When implemented, create cup holes at each position:
        # - Diameter: cup_diameter (35mm)
        # - Depth: cup_depth (12.5mm) 
        # - Centerline: cup_offset_k (21.5mm) from door edge
        self._hinge_positions = hinge_positions
        
        # Placeholder - actual implementation will use Fusion API to create holes
        pass
    
    def _create_mounting_plate_holes(self, component, side_body, effective_height, depth, thickness,
                                    has_plinth, plinth_height, params):
        """
        Crea fori per piastra di montaggio sul pannello laterale
        
        Args:
            component: Componente mobile
            side_body: Body del pannello laterale
            effective_height: Altezza effettiva carcassa (mm)
            depth: Profondità mobile (mm)
            thickness: Spessore pannello (mm)
            has_plinth: Se ha zoccolo
            plinth_height: Altezza zoccolo (mm)
            params: Parametri configurazione
        
        Note:
            This is a placeholder method. Actual hole drilling will be implemented
            in a future update using Fusion 360's holeFeatures API.
            
        Hole Pattern:
            - Vertical line at system_line distance (37mm) from front edge
            - Holes spaced vertically at 32mm intervals (System 32 standard)
            - Holes aligned with hinge positions on door
            - Diameter: 5mm, Depth: 13mm (for euro-screw 5×13)
        
        TODO: Implement actual hole drilling using component.features.holeFeatures
        """
        # Get mounting plate parameters
        system_line = params.get('mounting_plate_system_line', self.DEFAULT_MOUNTING_PLATE_SYSTEM_LINE)
        hole_spacing = params.get('mounting_plate_hole_spacing', self.DEFAULT_MOUNTING_PLATE_HOLE_SPACING)
        hole_diameter = params.get('mounting_plate_hole_diameter', self.DEFAULT_MOUNTING_PLATE_HOLE_DIAMETER)
        screw_depth = params.get('screw_depth', self.DEFAULT_SCREW_DEPTH)
        
        # Calculate hole positions
        # System line is at 37mm from front edge
        # Holes spaced vertically at 32mm intervals
        # Aligned with hinge positions on door
        
        # Store calculated pattern for future implementation
        # When implemented, create holes at:
        # - Y position: system_line (37mm from front)
        # - Z positions: aligned with hinge positions, plus additional holes in 32mm grid
        # - X position: on side panel face
        # - Diameter: hole_diameter (5mm)
        # - Depth: screw_depth (13mm)
        self._mounting_plate_system_line = system_line
        self._mounting_plate_hole_spacing = hole_spacing
        
        # Placeholder - actual implementation will use Fusion API to create holes
        pass
    
    def _create_rabbet_cuts(self, component, width, height, depth, thickness, has_plinth,
                           plinth_height, rabbet_width, rabbet_depth):
        """
        Crea scassi per montaggio retro a filo (flush_rabbet)
        
        Args:
            component: Componente mobile
            Placeholder per implementazione futura con extrude cuts
        """
        # TODO: Implement rabbet cuts on side panels, top and bottom
        # Use extrude cuts to create grooves for back panel insertion
        pass
    
    def _create_groove_cuts(self, component, width, height, depth, thickness, has_plinth,
                           plinth_height, groove_width, groove_depth, groove_offset):
        """
        Crea cave per montaggio retro in scanalatura (groove)
        
        Args:
            component: Componente mobile
            Placeholder per implementazione futura con extrude cuts
        """
        # TODO: Implement groove cuts on side panels
        # Use extrude cuts to create grooves at specified offset from back
        pass
