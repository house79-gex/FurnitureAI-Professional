"""
Cabinet Generator - Generatore professionale di carcasse mobili parametriche

Sistema completo per la creazione di carcasse mobili (scocca/struttura) con caratteristiche
professionali di falegnameria, incluse opzioni di montaggio schienale e sistemi di foratura.

RESPONSABILITÀ (versione 3.1 - FIX CRITICO Point3D):
- Creazione carcassa mobile (fianchi, top, fondo, schienale, zoccolo, ripiani, divisori)
- Sistema coordinate: X=larghezza, Y=altezza, Z=profondità (allineato con Fusion 360)
- FIX v3.1: Corretti parametri Point3D.create() su piani XZ e YZ
- Montaggio professionale schienale: flush_rabbet, groove, surface
- Sistema ripiani regolabili con forature System 32 (opzionale)
- Parametri utente nel componente per personalizzazione post-generazione

NON RESPONSABILE DI (delegato ad altri moduli):
- ❌ Generazione ante (vedi DoorGenerator + DoorDesigner)
- ❌ Generazione cassetti (vedi DrawerGenerator)
- ❌ Configurazione cerniere ante (vedi DoorGenerator.add_hinge_preparation)
- ❌ Logica business ante multiple (vedi DoorDesigner.compute_door_configs)

COORDINATE SYSTEM (allineato con Fusion 360):
- Origine: (0, 0, 0) = angolo inferiore sinistro posteriore del mobile
- X: Larghezza (0 = fianco sinistro, width = fianco destro)  
- Y: Altezza (0 = pavimento, height = top mobile)
- Z: Profondità (0 = retro/schienale, depth = fronte)
- Unità Fusion 360: cm (conversione automatica da mm input)

STRUTTURA CARCASSA (coordinate Y=altezza, Z=profondità):
- Zoccolo (plinth): da Y=0 a Y=plinth_height, Z da retro a fronte
- Fianchi (sides): da Y=plinth_height a Y=height (altezza = carcass_height)
- Fondo (bottom): a Y=plinth_height
- Cielo (top): a Y=height-thickness
- Schienale (back): secondo tipo montaggio, a Z=0 (retro) + offset
- Ripiani (shelves): spaziati uniformemente in altezza carcassa (Y)

MODIFICHE v3.1 (FIX CRITICO):
- Corretti parametri Point3D.create() in TUTTI i metodi con piani XZ/YZ
- _create_side_panels: da (y,0,0) a (0,y,z)
- _create_top_bottom_panels: da (x,z,0) a (x,0,z)
- _create_plinth: da (x,z,0) a (x,0,z)
- _create_shelves: da (x,z,0) a (x,0,z)
- _create_divisions: da (y,0,0) a (0,y,z)
"""

import adsk.core
import adsk.fusion
import math
from ..logging_utils import setup_logger

# Unit conversion constant: Fusion 360 uses cm internally
MM_TO_CM = 10.0


class CabinetGenerator:
    """Generatore parametrico di mobili con sistema di foratura e lavorazioni professionali"""

    # =========================================================================
    # DEPRECATED: Door and hinge defaults
    # =========================================================================
    DEFAULT_DOOR_GAP = 2.0  # mm - DEPRECATED
    DEFAULT_DOOR_OVERLAY_LEFT = 18.0  # mm - DEPRECATED
    DEFAULT_DOOR_OVERLAY_RIGHT = 18.0  # mm - DEPRECATED
    DEFAULT_DOOR_OVERLAY_TOP = 18.0  # mm - DEPRECATED
    DEFAULT_DOOR_OVERLAY_BOTTOM = 18.0  # mm - DEPRECATED
    DEFAULT_DOOR_THICKNESS = 18.0  # mm - DEPRECATED

    # Hinge preset: Blum Clip-top 110° - DEPRECATED
    DEFAULT_HINGE_TYPE = "clip_top_110"  # DEPRECATED
    DEFAULT_CUP_DIAMETER = 35.0  # mm - DEPRECATED
    DEFAULT_CUP_DEPTH = 12.5  # mm - DEPRECATED
    DEFAULT_CUP_CENTER_OFFSET_FROM_EDGE = 21.5  # mm (K dimension) - DEPRECATED
    DEFAULT_HINGE_OFFSET_TOP = 100.0  # mm from top edge to center - DEPRECATED
    DEFAULT_HINGE_OFFSET_BOTTOM = 100.0  # mm from bottom edge to center - DEPRECATED
    DEFAULT_MOUNTING_PLATE_SYSTEM_LINE = 37.0  # mm (System 32 standard) - DEPRECATED
    DEFAULT_MOUNTING_PLATE_HOLE_SPACING = 32.0  # mm (vertical interaxis) - DEPRECATED
    DEFAULT_MOUNTING_PLATE_HOLE_DIAMETER = 5.0  # mm - DEPRECATED
    DEFAULT_SCREW_DEPTH = 13.0  # mm for euro-screw 5×13 - DEPRECATED

    # Auto hinge count thresholds - DEPRECATED
    DEFAULT_HINGE_THRESHOLD_2 = 900.0  # mm - 2 hinges for height ≤ 900 - DEPRECATED
    DEFAULT_HINGE_THRESHOLD_3 = 1500.0  # mm - 3 hinges for 900-1500 - DEPRECATED
    # 4+ hinges for > 1500 mm - DEPRECATED

    # =========================================================================
    # ACTIVE: Back mounting defaults
    # =========================================================================
    DEFAULT_BACK_MOUNTING = "flush_rabbet"  # or "groove" or "surface"
    DEFAULT_RABBET_WIDTH = 12.0  # mm
    DEFAULT_GROOVE_WIDTH_TOLERANCE = 0.5  # mm (added to back_thickness)
    DEFAULT_GROOVE_OFFSET_FROM_REAR = 10.0  # mm

    # =========================================================================
    # ACTIVE: Shelves defaults
    # =========================================================================
    DEFAULT_SHELF_FRONT_SETBACK = 3.0  # mm
    DEFAULT_SHELF_BORE_ENABLED = False
    DEFAULT_SHELF_BORE_DIAMETER = 5.0  # mm
    DEFAULT_SHELF_BORE_FRONT_DISTANCE = 37.0  # mm
    DEFAULT_SHELF_BORE_PATTERN = 32.0  # mm

    # =========================================================================
    # ACTIVE: Dowel/Joinery defaults
    # =========================================================================
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
        self.logger = setup_logger('CabinetGenerator')

    # -------------------------------------------------------------------------
    # ENTRY POINT
    # -------------------------------------------------------------------------
    def create_cabinet(self, params):
        """
        Crea un mobile completo con parametri utente (tutti in mm).
        
        RESPONSABILITÀ: Genera SOLO la carcassa del mobile (sides, top, bottom, back,
        plinth, shelves, dividers). NON genera ante o cassetti.
        
        NOTA: height = altezza TOTALE da pavimento a top.
        """
        # Parametri base cabinet
        width = params.get("width", 800)
        height = params.get("height", 720)
        depth = params.get("depth", 580)
        thickness = params.get("material_thickness", 18)

        # Schienale
        has_back = params.get("has_back", True)
        back_thickness = params.get("back_thickness", 3)
        back_mounting = params.get("back_mounting", self.DEFAULT_BACK_MOUNTING)
        rabbet_width = params.get("rabbet_width", self.DEFAULT_RABBET_WIDTH)
        rabbet_depth = params.get("rabbet_depth", back_thickness)
        groove_width = params.get("groove_width", back_thickness + self.DEFAULT_GROOVE_WIDTH_TOLERANCE)
        groove_depth = params.get("groove_depth", back_thickness)
        groove_offset = params.get("groove_offset_from_rear", self.DEFAULT_GROOVE_OFFSET_FROM_REAR)

        # Zoccolo
        has_plinth = params.get("has_plinth", True)
        plinth_height = params.get("plinth_height", 100)

        # Ripiani e divisori
        shelves_count = params.get("shelves_count", 0)
        shelf_front_setback = params.get("shelf_front_setback", self.DEFAULT_SHELF_FRONT_SETBACK)
        shelf_bore_enabled = params.get("shelf_bore_enabled", self.DEFAULT_SHELF_BORE_ENABLED)
        divisions_count = params.get("divisions_count", 0)

        # Parametri spinatura (non usati ora)
        dowels_enabled = params.get("dowels_enabled", False)
        dowel_diameter = params.get("dowel_diameter", 8)
        dowel_edge_distance = params.get("dowel_edge_distance", 37)
        dowel_spacing = params.get("dowel_spacing", 32)

        self._params = params
        
        # Log parametri principali
        self.logger.info("═" * 60)
        self.logger.info("🏗️ CabinetGenerator.create_cabinet() chiamato")
        self.logger.info(f"📐 Dimensioni: {width}x{height}x{depth} mm")
        self.logger.info(f"📦 Spessore: {thickness}mm, Schienale: {back_thickness}mm")
        self.logger.info(f"🔧 Zoccolo: {plinth_height}mm" if has_plinth else "🔧 Senza zoccolo")
        self.logger.info(f"📚 Ripiani: {shelves_count}, Divisori: {divisions_count}")
        self.logger.info(f"🔨 Back mounting: {back_mounting}")
        carcass_height = height - plinth_height if has_plinth else height
        self.logger.info(f"📏 Altezza carcassa (sopra zoccolo): {carcass_height}mm")
        self.logger.info("─" * 60)

        occurrence = self.root_comp.occurrences.addNewComponent(adsk.core.Matrix3D.create())
        cabinet_comp = occurrence.component
        cabinet_comp.name = f"Mobile_{int(width)}x{int(height)}x{int(depth)}"

        self._create_user_parameters(cabinet_comp, params)

        back_inset = self._calculate_back_inset(
            back_mounting, thickness, back_thickness, rabbet_width, groove_offset
        )

        self._create_side_panels(cabinet_comp, width, height, depth, thickness, has_plinth, plinth_height)
        self._create_top_bottom_panels(
            cabinet_comp,
            width,
            depth,
            thickness,
            height=height,
            has_plinth=has_plinth,
            plinth_height=plinth_height,
            back_inset=back_inset,
            back_mounting=back_mounting,
        )

        if has_back:
            self._create_back_panel(
                cabinet_comp,
                width,
                height,
                thickness,
                back_thickness,
                has_plinth,
                plinth_height,
                back_mounting,
                rabbet_width,
                rabbet_depth,
                groove_width,
                groove_depth,
                groove_offset,
                depth,
            )

        if has_plinth:
            self._create_plinth(cabinet_comp, width, depth, thickness, plinth_height)

        if shelves_count > 0:
            self._create_shelves(
                cabinet_comp,
                width,
                depth,
                thickness,
                height,
                shelves_count,
                has_plinth,
                plinth_height,
                shelf_front_setback,
                back_inset,
                back_mounting,
            )

        if divisions_count > 0:
            self._create_divisions(
                cabinet_comp, width, height, depth, thickness, divisions_count, has_plinth, plinth_height
            )

        self.logger.info(f"✅ Cabinet carcass creato: {cabinet_comp.name}")
        self.logger.info("═" * 60)
        
        return cabinet_comp

    # -------------------------------------------------------------------------
    # SUPPORTO PARAMETRI E UNITÀ
    # -------------------------------------------------------------------------
    def _calculate_back_inset(self, back_mounting, thickness, back_thickness, rabbet_width, groove_offset):
        """
        Calcola l'arretramento (inset) dello schienale dalla faccia posteriore dei fianchi.
        """
        if back_mounting == "flush_rabbet":
            return rabbet_width
        elif back_mounting == "groove":
            return groove_offset
        elif back_mounting == "surface":
            return 0
        else:
            if self.logger:
                self.logger.warning(
                    f"Tipo back_mounting non riconosciuto '{back_mounting}', uso 'flush_rabbet' di default"
                )
            return rabbet_width

    def _mm_to_cm(self, value_mm):
        """Converte millimetri in centimetri per Fusion 360."""
        return value_mm / MM_TO_CM

    def _create_user_parameters(self, component, params):
        user_params = component.parentDesign.userParameters

        param_list = [
            ("Larghezza", params.get("width", 800), "mm"),
            ("Altezza", params.get("height", 720), "mm"),
            ("Profondita", params.get("depth", 580), "mm"),
            ("Spessore", params.get("material_thickness", 18), "mm"),
            ("SpessoreRetro", params.get("back_thickness", 3), "mm"),
            ("AltezzaZoccolo", params.get("plinth_height", 100), "mm"),
        ]

        for name, value, unit in param_list:
            value_input = adsk.core.ValueInput.createByReal(value / MM_TO_CM)
            try:
                user_params.add(name, value_input, unit, "")
            except:
                pass

    # -------------------------------------------------------------------------
    # GEOMETRIA SCATOLA (BOX CARCASS) - FIX v3.1
    # -------------------------------------------------------------------------
    def _create_side_panels(self, component, width, height, depth, thickness, has_plinth, plinth_height):
        """
        Crea i pannelli laterali (fianchi sinistro e destro) della carcassa.
        
        Sistema coordinate CORRETTO (v3.1 - FIX CRITICO):
        - Sketch su yZConstructionPlane (piano dove X=0)
        - Point3D.create() SEMPRE in coordinate WORLD: (X=0, Y=y_world, Z=z_world)
        - Rettangolo: da (0, plinth_height, 0) a (0, height, depth)
        - Estrusione in direzione +X per spessore fianco
        
        FIX v3.1: Corretti parametri Point3D da (y,z,0) → (0,y,z)
        
        Risultato atteso bbox fianco sinistro (600×720×580, plinth=100):
        - X: (0, 1.8) cm = spessore 18mm
        - Y: (10, 72) cm = da top zoccolo a top mobile
        - Z: (0, 58) cm = da retro a fronte
        """
        sketches = component.sketches
        extrudes = component.features.extrudeFeatures
        move_feats = component.features.moveFeatures

        yz_plane = component.yZConstructionPlane

        carcass_height = height - plinth_height  # mm
        y_start_cm = plinth_height / MM_TO_CM    # cm (base carcassa in Y)
        y_end_cm = height / MM_TO_CM             # cm (top carcassa in Y)
        depth_cm = depth / MM_TO_CM              # cm

        # --- FIANCO SINISTRO ---
        # FIX v3.1: Su yZPlane (X=0), Point3D.create() usa (0, Y, Z) non (Y, Z, 0)!
        sketch_left = sketches.add(yz_plane)
        lines_left = sketch_left.sketchCurves.sketchLines
        
        # Punti in coordinate WORLD 3D (tutti con X=0 perché siamo su piano yZ)
        p1 = adsk.core.Point3D.create(0, y_start_cm, 0)           # retro basso
        p2 = adsk.core.Point3D.create(0, y_end_cm, 0)            # retro alto
        p3 = adsk.core.Point3D.create(0, y_end_cm, depth_cm)     # fronte alto
        p4 = adsk.core.Point3D.create(0, y_start_cm, depth_cm)   # fronte basso
        
        lines_left.addByTwoPoints(p1, p2)
        lines_left.addByTwoPoints(p2, p3)
        lines_left.addByTwoPoints(p3, p4)
        lines_left.addByTwoPoints(p4, p1)

        extrude_input_left = extrudes.createInput(
            sketch_left.profiles.item(0), 
            adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        distance = adsk.core.ValueInput.createByReal(thickness / MM_TO_CM)
        extrude_input_left.setDistanceExtent(False, distance)
        extrude_left = extrudes.add(extrude_input_left)
        left_body = extrude_left.bodies.item(0)
        left_body.name = "Fianco_Sinistro"
       
        # DEBUG bbox
        try:
            bbox = left_body.boundingBox
            app = adsk.core.Application.get()
            ui = app.userInterface
            ui.messageBox(
                f"DEBUG FIANCO SINISTRO BBOX (v3.1 FIXED):\n"
                f"x=({bbox.minPoint.x:.2f}, {bbox.maxPoint.x:.2f}) cm\n"
                f"y=({bbox.minPoint.y:.2f}, {bbox.maxPoint.y:.2f}) cm\n"
                f"z=({bbox.minPoint.z:.2f}, {bbox.maxPoint.z:.2f}) cm"
            )
        except:
            pass

        # --- FIANCO DESTRO ---
        sketch_right = sketches.add(yz_plane)
        lines_right = sketch_right.sketchCurves.sketchLines
        
        p1 = adsk.core.Point3D.create(0, y_start_cm, 0)
        p2 = adsk.core.Point3D.create(0, y_end_cm, 0)
        p3 = adsk.core.Point3D.create(0, y_end_cm, depth_cm)
        p4 = adsk.core.Point3D.create(0, y_start_cm, depth_cm)
        
        lines_right.addByTwoPoints(p1, p2)
        lines_right.addByTwoPoints(p2, p3)
        lines_right.addByTwoPoints(p3, p4)
        lines_right.addByTwoPoints(p4, p1)

        extrude_input_right = extrudes.createInput(
            sketch_right.profiles.item(0),
            adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        extrude_input_right.setDistanceExtent(False, distance)
        extrude_right = extrudes.add(extrude_input_right)
        right_body = extrude_right.bodies.item(0)
        right_body.name = "Fianco_Destro"

        # Sposta fianco destro a X = width - thickness
        transform_right = adsk.core.Matrix3D.create()
        transform_right.translation = adsk.core.Vector3D.create(
            (width - thickness) / MM_TO_CM, 0, 0
        )
        bodies_right = adsk.core.ObjectCollection.create()
        bodies_right.add(right_body)
        move_input_right = move_feats.createInput(bodies_right, transform_right)
        move_feats.add(move_input_right)

    def _create_top_bottom_panels(
        self,
        component,
        width,
        depth,
        thickness,
        height=None,
        has_plinth=False,
        plinth_height=0,
        back_inset=0,
        back_mounting="flush_rabbet",
    ):
        """
        Fondo e cielo: pannelli orizzontali larghezza × profondità.
        
        Sistema coordinate CORRETTO (v3.1 - FIX CRITICO):
        - Sketch su xZConstructionPlane (piano orizzontale Y=costante)
        - Point3D.create() SEMPRE in coordinate WORLD: (X=x_world, Y=0, Z=z_world)
        - Rettangolo: da (thickness, 0, 0) a (width-thickness, 0, depth)
        - Estrusione in +Y per spessore pannello
        
        FIX v3.1: Corretti parametri Point3D da (x,z,0) → (x,0,z)
        
        Fondo: piano XZ a Y=plinth_height, estruso +Y per thickness
        Cielo: piano XZ a Y=height-thickness, estruso +Y per thickness
        """
        sketches = component.sketches
        extrudes = component.features.extrudeFeatures
        move_feats = component.features.moveFeatures

        xz_plane = component.xZConstructionPlane

        carcass_height = (height - plinth_height) if height is not None else None

        X_in_mm = width - 2 * thickness
        X_in = X_in_mm / MM_TO_CM
        depth_cm = depth / MM_TO_CM

        # Posizioni Y
        Y_bottom_mm = plinth_height
        Y_bottom = Y_bottom_mm / MM_TO_CM

        if carcass_height is not None:
            Y_top_mm = plinth_height + carcass_height - thickness
            Y_top = Y_top_mm / MM_TO_CM
        else:
            Y_top_mm = None
            Y_top = None

        # --- FONDO ---
        # FIX v3.1: Su xZPlane (Y=0), Point3D.create() usa (X, 0, Z) non (X, Z, 0)!
        sketch_bottom = sketches.add(xz_plane)
        lines_bottom = sketch_bottom.sketchCurves.sketchLines
        
        thickness_cm = thickness / MM_TO_CM
        width_end_cm = (thickness + X_in_mm) / MM_TO_CM
        
        p1 = adsk.core.Point3D.create(thickness_cm, 0, 0)          # retro sinistro
        p2 = adsk.core.Point3D.create(width_end_cm, 0, 0)          # retro destro
        p3 = adsk.core.Point3D.create(width_end_cm, 0, depth_cm)   # fronte destro
        p4 = adsk.core.Point3D.create(thickness_cm, 0, depth_cm)   # fronte sinistro
        
        lines_bottom.addByTwoPoints(p1, p2)
        lines_bottom.addByTwoPoints(p2, p3)
        lines_bottom.addByTwoPoints(p3, p4)
        lines_bottom.addByTwoPoints(p4, p1)

        extrude_input_bottom = extrudes.createInput(
            sketch_bottom.profiles.item(0), adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        extrude_input_bottom.setDistanceExtent(False, adsk.core.ValueInput.createByReal(thickness / MM_TO_CM))
        extrude_bottom = extrudes.add(extrude_input_bottom)
        body_bottom = extrude_bottom.bodies.item(0)
        body_bottom.name = "Fondo"

        # Posiziona fondo a Y = plinth_height
        transform_bottom = adsk.core.Matrix3D.create()
        transform_bottom.translation = adsk.core.Vector3D.create(0, Y_bottom, 0)
        bodies_bottom = adsk.core.ObjectCollection.create()
        bodies_bottom.add(body_bottom)
        move_input_bottom = move_feats.createInput(bodies_bottom, transform_bottom)
        move_feats.add(move_input_bottom)

        # --- CIELO (TOP) ---
        if Y_top is not None:
            sketch_top = sketches.add(xz_plane)
            lines_top = sketch_top.sketchCurves.sketchLines
            
            p1 = adsk.core.Point3D.create(thickness_cm, 0, 0)
            p2 = adsk.core.Point3D.create(width_end_cm, 0, 0)
            p3 = adsk.core.Point3D.create(width_end_cm, 0, depth_cm)
            p4 = adsk.core.Point3D.create(thickness_cm, 0, depth_cm)
            
            lines_top.addByTwoPoints(p1, p2)
            lines_top.addByTwoPoints(p2, p3)
            lines_top.addByTwoPoints(p3, p4)
            lines_top.addByTwoPoints(p4, p1)

            extrude_input_top = extrudes.createInput(
                sketch_top.profiles.item(0), adsk.fusion.FeatureOperations.NewBodyFeatureOperation
            )
            extrude_input_top.setDistanceExtent(False, adsk.core.ValueInput.createByReal(thickness / MM_TO_CM))
            extrude_top = extrudes.add(extrude_input_top)
            body_top = extrude_top.bodies.item(0)
            body_top.name = "Cielo"

            # Posiziona cielo a Y = height - thickness
            transform_top = adsk.core.Matrix3D.create()
            transform_top.translation = adsk.core.Vector3D.create(0, Y_top, 0)
            col_top = adsk.core.ObjectCollection.create()
            col_top.add(body_top)
            move_input_top = move_feats.createInput(col_top, transform_top)
            move_feats.add(move_input_top)

    def _create_back_panel(
        self,
        component,
        width,
        height,
        thickness,
        back_thickness,
        has_plinth,
        plinth_height,
        back_mounting="flush_rabbet",
        rabbet_width=12,
        rabbet_depth=3,
        groove_width=3.5,
        groove_depth=3,
        groove_offset=10,
        depth=580,
    ):
        """
        Schienale: pannello verticale larghezza × altezza sul retro.
        
        Sistema coordinate (CORRETTO v3.0, confermato v3.1):
        - Sketch su xYConstructionPlane (piano verticale Z=costante)
        - Primo parametro → X mondo (larghezza)
        - Secondo parametro → Y mondo (altezza)
        - Estrusione in +Z per spessore schienale
        
        Schienale: piano XY tra i fianchi, da fondo a cielo, a Z=back_inset
        """
        sketches = component.sketches
        extrudes = component.features.extrudeFeatures
        move_feats = component.features.moveFeatures

        xy_plane = component.xYConstructionPlane

        carcass_height = height - plinth_height  # mm

        panel_width_mm = width - 2 * thickness
        panel_height_mm = carcass_height - 2 * thickness

        x_left = thickness / MM_TO_CM
        x_right = (thickness + panel_width_mm) / MM_TO_CM

        y_base_mm = plinth_height + thickness
        y_base = y_base_mm / MM_TO_CM
        y_top = (y_base_mm + panel_height_mm) / MM_TO_CM

        if back_mounting == "flush_rabbet":
            z_position = rabbet_width / MM_TO_CM
        elif back_mounting == "groove":
            z_position = groove_offset / MM_TO_CM
        elif back_mounting == "surface":
            z_position = 0
        else:
            z_position = rabbet_width / MM_TO_CM

        sketch = sketches.add(xy_plane)
        sketch.sketchCurves.sketchLines.addTwoPointRectangle(
            adsk.core.Point3D.create(x_left, y_base, 0),
            adsk.core.Point3D.create(x_right, y_top, 0),
        )

        extrude_input_back = extrudes.createInput(
            sketch.profiles.item(0), adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        distance = adsk.core.ValueInput.createByReal(back_thickness / MM_TO_CM)
        extrude_input_back.setDistanceExtent(False, distance)
        extrude_back = extrudes.add(extrude_input_back)
        back_body = extrude_back.bodies.item(0)
        back_body.name = "Retro"

        transform_back = adsk.core.Matrix3D.create()
        transform_back.translation = adsk.core.Vector3D.create(0, 0, z_position)
        bodies_back = adsk.core.ObjectCollection.create()
        bodies_back.add(back_body)
        move_input_back = move_feats.createInput(bodies_back, transform_back)
        move_feats.add(move_input_back)
        
    def _create_plinth(self, component, width, depth, thickness, plinth_height):
        """
        Crea lo zoccolo sotto la carcassa.

        Sistema coordinate CORRETTO (v3.1 - FIX CRITICO):
        - Origine: angolo inferiore sinistro posteriore
        - X = larghezza (0 → width)
        - Y = altezza (0 = pavimento → plinth_height)
        - Z = profondità (0 = retro → depth)
        
        Metodo:
        - Sketch su xZConstructionPlane (piano Y=0, pavimento)
        - Point3D.create() SEMPRE in coordinate WORLD: (X=x_world, Y=0, Z=z_world)
        - Disegna rettangolo X × Z (larghezza × profondità)
        - Estrude in direzione +Y per plinth_height (verso l'alto)
        
        FIX v3.1: Corretti parametri Point3D da (x,z,0) → (x,0,z)
        
        Risultato atteso bbox zoccolo (600×720×580, plinth=100):
        - X: (0, 60) cm = larghezza
        - Y: (0, 10) cm = altezza zoccolo
        - Z: (0, 58) cm = profondità
        """
        sketches = component.sketches
        extrudes = component.features.extrudeFeatures

        xz_plane = component.xZConstructionPlane

        width_cm = width / MM_TO_CM
        depth_cm = depth / MM_TO_CM
        
        # FIX v3.1: Su xZPlane (Y=0), Point3D.create() usa (X, 0, Z) non (X, Z, 0)!
        sketch = sketches.add(xz_plane)
        lines = sketch.sketchCurves.sketchLines
        
        # Disegna rettangolo: punti in coordinate WORLD (X, Y=0, Z)
        p1 = adsk.core.Point3D.create(0, 0, 0)              # retro sinistro
        p2 = adsk.core.Point3D.create(width_cm, 0, 0)       # retro destro
        p3 = adsk.core.Point3D.create(width_cm, 0, depth_cm)  # fronte destro
        p4 = adsk.core.Point3D.create(0, 0, depth_cm)       # fronte sinistro
       
        lines.addByTwoPoints(p1, p2)
        lines.addByTwoPoints(p2, p3)
        lines.addByTwoPoints(p3, p4)
        lines.addByTwoPoints(p4, p1)

        # Estrusione in direzione +Y (verso l'alto) per altezza zoccolo
        extrude_input_plinth = extrudes.createInput(
            sketch.profiles.item(0), adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        distance = adsk.core.ValueInput.createByReal(plinth_height / MM_TO_CM)
        extrude_input_plinth.setDistanceExtent(False, distance)
        extrude_plinth = extrudes.add(extrude_input_plinth)
        plinth_body = extrude_plinth.bodies.item(0)
        plinth_body.name = "Zoccolo"
        
        # Log bbox per verifica
        try:
            bbox = plinth_body.boundingBox
            self.logger.info(
                f"   Zoccolo creato (v3.1) - bbox: "
                f"X=[{bbox.minPoint.x:.2f}, {bbox.maxPoint.x:.2f}] "
                f"Y=[{bbox.minPoint.y:.2f}, {bbox.maxPoint.y:.2f}] "
                f"Z=[{bbox.minPoint.z:.2f}, {bbox.maxPoint.z:.2f}] cm"
            )
        except Exception as e:
            self.logger.warning(f"   Impossibile ottenere bbox zoccolo: {e}")
    
    def _create_shelves(
        self,
        component,
        width,
        depth,
        thickness,
        height,
        count,
        has_plinth,
        plinth_height,
        shelf_front_setback,
        back_inset,
        back_mounting,
    ):
        """
        Crea ripiani interni regolabili: pannelli orizzontali larghezza × profondità.
        
        Sistema coordinate CORRETTO (v3.1 - FIX CRITICO):
        - Sketch su xZConstructionPlane (piano orizzontale Y=costante)
        - Point3D.create() SEMPRE in coordinate WORLD: (X=x_world, Y=0, Z=z_world)
        - Rettangolo: da (thickness, 0, back_inset) a (width-thickness, 0, depth-setback)
        - Estrusione in +Y per spessore ripiano
        
        FIX v3.1: Corretti parametri Point3D da (x,z,0) → (x,0,z)
        
        Ripiani: piani XZ a varie Y (altezze), distribuiti uniformemente tra fondo e cielo
        """
        if count <= 0:
            return

        sketches = component.sketches
        extrudes = component.features.extrudeFeatures
        move_feats = component.features.moveFeatures

        xz_plane = component.xZConstructionPlane

        X_in_mm = width - 2 * thickness
        X_in = X_in_mm / MM_TO_CM

        carcass_height = height - plinth_height  # mm

        Z_start_mm = back_inset
        Z_end_mm = depth - shelf_front_setback
        Z_start = Z_start_mm / MM_TO_CM
        Z_end = Z_end_mm / MM_TO_CM
        
        usable_height_mm = carcass_height - 2 * thickness
        if usable_height_mm <= 0:
            return

        spacing_mm = usable_height_mm / (count + 1)

        thickness_cm = thickness / MM_TO_CM
        width_end_cm = (thickness + X_in_mm) / MM_TO_CM

        for i in range(count):
            Y_pos_mm = plinth_height + thickness + spacing_mm * (i + 1)
            Y_pos = Y_pos_mm / MM_TO_CM
            
            # FIX v3.1: Su xZPlane (Y=0), Point3D.create() usa (X, 0, Z) non (X, Z, 0)!
            sketch = sketches.add(xz_plane)
            lines = sketch.sketchCurves.sketchLines
            
            p1 = adsk.core.Point3D.create(thickness_cm, 0, Z_start)
            p2 = adsk.core.Point3D.create(width_end_cm, 0, Z_start)
            p3 = adsk.core.Point3D.create(width_end_cm, 0, Z_end)
            p4 = adsk.core.Point3D.create(thickness_cm, 0, Z_end)
            
            lines.addByTwoPoints(p1, p2)
            lines.addByTwoPoints(p2, p3)
            lines.addByTwoPoints(p3, p4)
            lines.addByTwoPoints(p4, p1)

            extrude_input_shelf = extrudes.createInput(
                sketch.profiles.item(0), adsk.fusion.FeatureOperations.NewBodyFeatureOperation
            )
            extrude_input_shelf.setDistanceExtent(False, adsk.core.ValueInput.createByReal(thickness / MM_TO_CM))
            extrude_shelf = extrudes.add(extrude_input_shelf)
            shelf_body = extrude_shelf.bodies.item(0)
            shelf_body.name = f"Ripiano_{i+1}"

            transform_shelf = adsk.core.Matrix3D.create()
            transform_shelf.translation = adsk.core.Vector3D.create(0, Y_pos, 0)
            col_shelf = adsk.core.ObjectCollection.create()
            col_shelf.add(shelf_body)
            move_input_shelf = move_feats.createInput(col_shelf, transform_shelf)
            move_feats.add(move_input_shelf)

    def _create_divisions(self, component, width, height, depth, thickness, count, has_plinth, plinth_height):
        """
        Crea divisori verticali interni.
        
        Sistema coordinate CORRETTO (v3.1 - FIX CRITICO):
        - Sketch su yZConstructionPlane (piano X=0)
        - Point3D.create() SEMPRE in coordinate WORLD: (X=0, Y=y_world, Z=z_world)
        - Rettangolo: da (0, plinth+thickness, 0) a (0, height-thickness, depth)
        - Estrusione in +X per spessore divisorio
        
        FIX v3.1: Corretti parametri Point3D da (y,z,0) → (0,y,z)
        
        Divisori: distribuiti uniformemente in X (larghezza),
                  con altezza da (plinth+thickness) a (height-thickness)
        """
        sketches = component.sketches
        extrudes = component.features.extrudeFeatures
        move_feats = component.features.moveFeatures

        yz_plane = component.yZConstructionPlane

        usable_width = width - 2 * thickness
        spacing = usable_width / (count + 1)

        effective_height = height - plinth_height if has_plinth else height
        panel_height = effective_height - 2 * thickness

        y_offset = (plinth_height + thickness) / MM_TO_CM if has_plinth else thickness / MM_TO_CM
        y_end = y_offset + panel_height / MM_TO_CM
        depth_cm = depth / MM_TO_CM

        for i in range(count):
            x_position = thickness + spacing * (i + 1)

            # FIX v3.1: Su yZPlane (X=0), Point3D.create() usa (0, Y, Z) non (Y, Z, 0)!
            sketch = sketches.add(yz_plane)
            lines = sketch.sketchCurves.sketchLines
            
            p1 = adsk.core.Point3D.create(0, y_offset, 0)
            p2 = adsk.core.Point3D.create(0, y_end, 0)
            p3 = adsk.core.Point3D.create(0, y_end, depth_cm)
            p4 = adsk.core.Point3D.create(0, y_offset, depth_cm)
            
            lines.addByTwoPoints(p1, p2)
            lines.addByTwoPoints(p2, p3)
            lines.addByTwoPoints(p3, p4)
            lines.addByTwoPoints(p4, p1)

            extrude_input_div = extrudes.createInput(
                sketch.profiles.item(0), adsk.fusion.FeatureOperations.NewBodyFeatureOperation
            )
            distance = adsk.core.ValueInput.createByReal(thickness / MM_TO_CM)
            extrude_input_div.setDistanceExtent(False, distance)
            extrude_div = extrudes.add(extrude_input_div)
            extrude_div.bodies.item(0).name = f"Divisorio_{i+1}"

            transform_div = adsk.core.Matrix3D.create()
            transform_div.translation = adsk.core.Vector3D.create(x_position / MM_TO_CM, 0, 0)

            bodies_div = adsk.core.ObjectCollection.create()
            bodies_div.add(extrude_div.bodies.item(0))
            move_input_div = move_feats.createInput(bodies_div, transform_div)
            move_feats.add(move_input_div)

    # -------------------------------------------------------------------------
    # PLACEHOLDER LAVORAZIONI
    # -------------------------------------------------------------------------
    def _create_rabbet_cuts(
        self,
        component,
        width,
        height,
        depth,
        thickness,
        back_thickness,
        has_plinth,
        plinth_height,
        rabbet_width,
        rabbet_depth,
    ):
        pass

    def _create_groove_cuts(
        self,
        component,
        width,
        height,
        depth,
        thickness,
        back_thickness,
        has_plinth,
        plinth_height,
        groove_width,
        groove_depth,
        groove_offset_from_rear,
    ):
        pass

    def _create_dowel_holes(
        self,
        component,
        width,
        height,
        depth,
        thickness,
        has_plinth,
        plinth_height,
        dowel_diameter,
        dowel_edge_distance,
        dowel_spacing,
    ):
        pass
