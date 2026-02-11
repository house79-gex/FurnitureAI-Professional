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

    # -------------------------------------------------------------------------
    # ENTRY POINT
    # -------------------------------------------------------------------------
    def create_cabinet(self, params):
        """
        Crea un mobile completo con parametri utente (tutti in mm).

        NOTA: height = altezza TOTALE da pavimento a top.
        """
        width = params.get("width", 800)
        height = params.get("height", 720)
        depth = params.get("depth", 580)
        thickness = params.get("material_thickness", 18)

        has_back = params.get("has_back", True)
        back_thickness = params.get("back_thickness", 3)
        back_mounting = params.get("back_mounting", self.DEFAULT_BACK_MOUNTING)
        rabbet_width = params.get("rabbet_width", self.DEFAULT_RABBET_WIDTH)
        rabbet_depth = params.get("rabbet_depth", back_thickness)
        groove_width = params.get("groove_width", back_thickness + self.DEFAULT_GROOVE_WIDTH_TOLERANCE)
        groove_depth = params.get("groove_depth", back_thickness)
        groove_offset = params.get("groove_offset_from_rear", self.DEFAULT_GROOVE_OFFSET_FROM_REAR)

        has_plinth = params.get("has_plinth", True)
        plinth_height = params.get("plinth_height", 100)

        shelves_count = params.get("shelves_count", 0)
        shelf_front_setback = params.get("shelf_front_setback", self.DEFAULT_SHELF_FRONT_SETBACK)
        shelf_bore_enabled = params.get("shelf_bore_enabled", self.DEFAULT_SHELF_BORE_ENABLED)
        divisions_count = params.get("divisions_count", 0)

        has_door = params.get("has_door", False)
        door_gap = params.get("door_gap", self.DEFAULT_DOOR_GAP)
        door_overlay_left = params.get("door_overlay_left", self.DEFAULT_DOOR_OVERLAY_LEFT)
        door_overlay_right = params.get("door_overlay_right", self.DEFAULT_DOOR_OVERLAY_RIGHT)
        door_overlay_top = params.get("door_overlay_top", self.DEFAULT_DOOR_OVERLAY_TOP)
        door_overlay_bottom = params.get("door_overlay_bottom", self.DEFAULT_DOOR_OVERLAY_BOTTOM)
        door_thickness = params.get("door_thickness", self.DEFAULT_DOOR_THICKNESS)

        # Parametri spinatura/foratura (placeholder, non usati ora)
        dowels_enabled = params.get("dowels_enabled", False)
        dowel_diameter = params.get("dowel_diameter", 8)
        dowel_edge_distance = params.get("dowel_edge_distance", 37)
        dowel_spacing = params.get("dowel_spacing", 32)

        self._params = params

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

        if has_door:
            self._create_door_panel(
                cabinet_comp,
                width,
                height,
                depth,
                thickness,
                has_plinth,
                plinth_height,
                door_gap,
                door_overlay_left,
                door_overlay_right,
                door_overlay_top,
                door_overlay_bottom,
                door_thickness,
                params,
            )

        return cabinet_comp

    # -------------------------------------------------------------------------
    # SUPPORTO PARAMETRI E UNITÀ
    # -------------------------------------------------------------------------
    def _calculate_back_inset(self, back_mounting, thickness, back_thickness, rabbet_width, groove_offset):
        if back_mounting == "flush_rabbet":
            return rabbet_width
        elif back_mounting == "groove":
            return groove_offset
        elif back_mounting == "surface":
            return 0
        else:
            if self.logger:
                self.logger.warning(
                    f"Unrecognized back_mounting type '{back_mounting}', defaulting to 'flush_rabbet'"
                )
            return rabbet_width

    def _mm_to_cm(self, value_mm):
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
            ("DoorGap", params.get("door_gap", self.DEFAULT_DOOR_GAP), "mm"),
            ("DoorOverlayLeft", params.get("door_overlay_left", self.DEFAULT_DOOR_OVERLAY_LEFT), "mm"),
            ("DoorOverlayRight", params.get("door_overlay_right", self.DEFAULT_DOOR_OVERLAY_RIGHT), "mm"),
            ("DoorOverlayTop", params.get("door_overlay_top", self.DEFAULT_DOOR_OVERLAY_TOP), "mm"),
            ("DoorOverlayBottom", params.get("door_overlay_bottom", self.DEFAULT_DOOR_OVERLAY_BOTTOM), "mm"),
            ("DoorThickness", params.get("door_thickness", self.DEFAULT_DOOR_THICKNESS), "mm"),
            ("CupDiameter", params.get("cup_diameter", self.DEFAULT_CUP_DIAMETER), "mm"),
            ("CupDepth", params.get("cup_depth", self.DEFAULT_CUP_DEPTH), "mm"),
            (
                "CupOffsetFromEdge",
                params.get("cup_center_offset_from_edge", self.DEFAULT_CUP_CENTER_OFFSET_FROM_EDGE),
                "mm",
            ),
            ("HingeOffsetTop", params.get("hinge_offset_top", self.DEFAULT_HINGE_OFFSET_TOP), "mm"),
            ("HingeOffsetBottom", params.get("hinge_offset_bottom", self.DEFAULT_HINGE_OFFSET_BOTTOM), "mm"),
            (
                "MountingPlateSystemLine",
                params.get("mounting_plate_system_line", self.DEFAULT_MOUNTING_PLATE_SYSTEM_LINE),
                "mm",
            ),
            (
                "MountingPlateHoleSpacing",
                params.get("mounting_plate_hole_spacing", self.DEFAULT_MOUNTING_PLATE_HOLE_SPACING),
                "mm",
            ),
            (
                "MountingPlateHoleDiameter",
                params.get("mounting_plate_hole_diameter", self.DEFAULT_MOUNTING_PLATE_HOLE_DIAMETER),
                "mm",
            ),
            ("RabbetWidth", params.get("rabbet_width", self.DEFAULT_RABBET_WIDTH), "mm"),
            ("GrooveOffsetFromRear", params.get("groove_offset_from_rear", self.DEFAULT_GROOVE_OFFSET_FROM_REAR), "mm"),
            ("ShelfFrontSetback", params.get("shelf_front_setback", self.DEFAULT_SHELF_FRONT_SETBACK), "mm"),
            ("ShelfBoreDiameter", params.get("shelf_bore_diameter", self.DEFAULT_SHELF_BORE_DIAMETER), "mm"),
            ("ShelfBoreFrontDistance", params.get("shelf_bore_front_distance", self.DEFAULT_SHELF_BORE_FRONT_DISTANCE), "mm"),
            ("ShelfBorePattern", params.get("shelf_bore_pattern", self.DEFAULT_SHELF_BORE_PATTERN), "mm"),
            ("DowelDiameter", params.get("dowel_diameter", self.DEFAULT_DOWEL_DIAMETER), "mm"),
            ("DowelEdgeDistance", params.get("dowel_edge_distance", self.DEFAULT_DOWEL_EDGE_DISTANCE), "mm"),
            ("DowelSpacing", params.get("dowel_spacing", self.DEFAULT_DOWEL_SPACING), "mm"),
        ]

        for name, value, unit in param_list:
            value_input = adsk.core.ValueInput.createByReal(value / MM_TO_CM)
            try:
                user_params.add(name, value_input, unit, "")
            except:
                pass

    # -------------------------------------------------------------------------
    # GEOMETRIA SCATOLA
    # -------------------------------------------------------------------------
    def _create_side_panels(self, component, width, height, depth, thickness, has_plinth, plinth_height):
        sketches = component.sketches
        extrudes = component.features.extrudeFeatures
        move_feats = component.features.moveFeatures

        yz_plane = component.yZConstructionPlane

        carcass_height = height - plinth_height  # mm
        z_start = plinth_height / MM_TO_CM  # cm

        # Fianco sinistro
        sketch_left = sketches.add(yz_plane)
        sketch_left.sketchCurves.sketchLines.addTwoPointRectangle(
            adsk.core.Point3D.create(0, z_start, 0),
            adsk.core.Point3D.create(depth / MM_TO_CM, z_start + carcass_height / MM_TO_CM, 0),
        )

        extrude_input_left = extrudes.createInput(
            sketch_left.profiles.item(0), adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        distance = adsk.core.ValueInput.createByReal(thickness / MM_TO_CM)
        extrude_input_left.setDistanceExtent(False, distance)
        extrude_left = extrudes.add(extrude_input_left)
        extrude_left.bodies.item(0).name = "Fianco_Sinistro"

        # Fianco destro
        sketch_right = sketches.add(yz_plane)
        sketch_right.sketchCurves.sketchLines.addTwoPointRectangle(
            adsk.core.Point3D.create(0, z_start, 0),
            adsk.core.Point3D.create(depth / MM_TO_CM, z_start + carcass_height / MM_TO_CM, 0),
        )

        transform_right = adsk.core.Matrix3D.create()
        transform_right.translation = adsk.core.Vector3D.create((width - thickness) / MM_TO_CM, 0, 0)

        extrude_input_right = extrudes.createInput(
            sketch_right.profiles.item(0), adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        extrude_input_right.setDistanceExtent(False, distance)
        extrude_right = extrudes.add(extrude_input_right)

        bodies_right = adsk.core.ObjectCollection.create()
        bodies_right.add(extrude_right.bodies.item(0))
        move_input_right = move_feats.createInput(bodies_right, transform_right)
        move_feats.add(move_input_right)

        extrude_right.bodies.item(0).name = "Fianco_Destro"

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
        Fondo e cielo con stessa profondità dei fianchi.
        """
        sketches = component.sketches
        extrudes = component.features.extrudeFeatures
        move_feats = component.features.moveFeatures

        yz_plane = component.yZConstructionPlane

        carcass_height = (height - plinth_height) if height is not None else None

        W_in_mm = width - 2 * thickness
        W_in = W_in_mm / MM_TO_CM  # cm

        depth_cm = depth / MM_TO_CM

        Z_bottom_mm = plinth_height
        Z_bottom = Z_bottom_mm / MM_TO_CM

        if carcass_height is not None:
            Z_top_mm = plinth_height + carcass_height - thickness
            Z_top = Z_top_mm / MM_TO_CM
        else:
            Z_top_mm = None
            Z_top = None

        # Fondo
        sketch_bottom = sketches.add(yz_plane)
        sketch_bottom.sketchCurves.sketchLines.addTwoPointRectangle(
            adsk.core.Point3D.create(0, Z_bottom, 0),
            adsk.core.Point3D.create(depth_cm, (Z_bottom_mm + thickness) / MM_TO_CM, 0),
        )
        extrude_input_bottom = extrudes.createInput(
            sketch_bottom.profiles.item(0), adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        extrude_input_bottom.setDistanceExtent(False, adsk.core.ValueInput.createByReal(W_in))
        extrude_bottom = extrudes.add(extrude_input_bottom)
        body_bottom = extrude_bottom.bodies.item(0)
        body_bottom.name = "Fondo"

        transform_bottom = adsk.core.Matrix3D.create()
        transform_bottom.translation = adsk.core.Vector3D.create(thickness / MM_TO_CM, 0, 0)
        col_bottom = adsk.core.ObjectCollection.create()
        col_bottom.add(body_bottom)
        move_input_bottom = move_feats.createInput(col_bottom, transform_bottom)
        move_feats.add(move_input_bottom)

        # Cielo
        if Z_top is not None:
            sketch_top = sketches.add(yz_plane)
            sketch_top.sketchCurves.sketchLines.addTwoPointRectangle(
                adsk.core.Point3D.create(0, Z_top, 0),
                adsk.core.Point3D.create(depth_cm, (Z_top_mm + thickness) / MM_TO_CM, 0),
            )
            extrude_input_top = extrudes.createInput(
                sketch_top.profiles.item(0), adsk.fusion.FeatureOperations.NewBodyFeatureOperation
            )
            extrude_input_top.setDistanceExtent(False, adsk.core.ValueInput.createByReal(W_in))
            extrude_top = extrudes.add(extrude_input_top)
            body_top = extrude_top.bodies.item(0)
            body_top.name = "Cielo"

            transform_top = adsk.core.Matrix3D.create()
            transform_top.translation = adsk.core.Vector3D.create(thickness / MM_TO_CM, 0, 0)
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
        Schienale interno appoggiato su fondo e sotto il cielo.
        """
        sketches = component.sketches
        extrudes = component.features.extrudeFeatures
        move_feats = component.features.moveFeatures

        yz_plane = component.yZConstructionPlane

        carcass_height = height - plinth_height  # mm

        panel_width_mm = width - 2 * thickness
        panel_height_mm = carcass_height - 2 * thickness

        z_base_mm = plinth_height + thickness
        z_base = z_base_mm / MM_TO_CM
        z_top = (z_base_mm + panel_height_mm) / MM_TO_CM

        if back_mounting == "flush_rabbet":
            y_position = (depth - rabbet_width) / MM_TO_CM
        elif back_mounting == "groove":
            y_position = (depth - groove_offset) / MM_TO_CM
        elif back_mounting == "surface":
            y_position = (depth - back_thickness) / MM_TO_CM
        else:
            y_position = (depth - rabbet_width) / MM_TO_CM

        sketch = sketches.add(yz_plane)
        sketch.sketchCurves.sketchLines.addTwoPointRectangle(
            adsk.core.Point3D.create(y_position, z_base, 0),
            adsk.core.Point3D.create(y_position + back_thickness / MM_TO_CM, z_top, 0),
        )

        extrude_input_back = extrudes.createInput(
            sketch.profiles.item(0), adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        distance = adsk.core.ValueInput.createByReal(panel_width_mm / MM_TO_CM)
        extrude_input_back.setDistanceExtent(False, distance)
        extrude_back = extrudes.add(extrude_input_back)
        back_body = extrude_back.bodies.item(0)
        back_body.name = "Retro"

        transform_back = adsk.core.Matrix3D.create()
        transform_back.translation = adsk.core.Vector3D.create(thickness / MM_TO_CM, 0, 0)
        bodies_back = adsk.core.ObjectCollection.create()
        bodies_back.add(back_body)
        move_input_back = move_feats.createInput(bodies_back, transform_back)
        move_feats.add(move_input_back)

    def _create_plinth(self, component, width, depth, thickness, plinth_height):
        sketches = component.sketches
        extrudes = component.features.extrudeFeatures

        xy_plane = component.xYConstructionPlane

        sketch = sketches.add(xy_plane)
        lines = sketch.sketchCurves.sketchLines

        p1 = adsk.core.Point3D.create(0, 0, 0)
        p2 = adsk.core.Point3D.create(width / MM_TO_CM, 0, 0)
        p3 = adsk.core.Point3D.create(width / MM_TO_CM, (thickness * 2) / MM_TO_CM, 0)
        p4 = adsk.core.Point3D.create(0, (thickness * 2) / MM_TO_CM, 0)

        lines.addByTwoPoints(p1, p2)
        lines.addByTwoPoints(p2, p3)
        lines.addByTwoPoints(p3, p4)
        lines.addByTwoPoints(p4, p1)

        extrude_input_plinth = extrudes.createInput(
            sketch.profiles.item(0), adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        distance = adsk.core.ValueInput.createByReal(plinth_height / MM_TO_CM)
        extrude_input_plinth.setDistanceExtent(False, distance)
        extrude_plinth = extrudes.add(extrude_input_plinth)
        extrude_plinth.bodies.item(0).name = "Zoccolo"

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
        if count <= 0:
            return

        sketches = component.sketches
        extrudes = component.features.extrudeFeatures
        move_feats = component.features.moveFeatures

        yz_plane = component.yZConstructionPlane

        W_in_mm = width - 2 * thickness
        W_in = W_in_mm / MM_TO_CM

        carcass_height = height - plinth_height  # mm

        shelf_depth_eff_mm = depth - back_inset - shelf_front_setback
        usable_height_mm = carcass_height - 2 * thickness
        if usable_height_mm <= 0:
            return

        spacing_mm = usable_height_mm / (count + 1)

        for i in range(count):
            Z_pos_mm = plinth_height + thickness + spacing_mm * (i + 1)
            Z_pos = Z_pos_mm / MM_TO_CM

            sketch = sketches.add(yz_plane)
            sketch.sketchCurves.sketchLines.addTwoPointRectangle(
                adsk.core.Point3D.create(shelf_front_setback / MM_TO_CM, Z_pos, 0),
                adsk.core.Point3D.create(
                    (shelf_front_setback + shelf_depth_eff_mm) / MM_TO_CM, (Z_pos_mm + thickness) / MM_TO_CM, 0
                ),
            )

            extrude_input_shelf = extrudes.createInput(
                sketch.profiles.item(0), adsk.fusion.FeatureOperations.NewBodyFeatureOperation
            )
            extrude_input_shelf.setDistanceExtent(False, adsk.core.ValueInput.createByReal(W_in))
            extrude_shelf = extrudes.add(extrude_input_shelf)
            shelf_body = extrude_shelf.bodies.item(0)
            shelf_body.name = f"Ripiano_{i+1}"

            transform_shelf = adsk.core.Matrix3D.create()
            transform_shelf.translation = adsk.core.Vector3D.create(thickness / MM_TO_CM, 0, 0)
            col_shelf = adsk.core.ObjectCollection.create()
            col_shelf.add(shelf_body)
            move_input_shelf = move_feats.createInput(col_shelf, transform_shelf)
            move_feats.add(move_input_shelf)

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

    def _create_divisions(self, component, width, height, depth, thickness, count, has_plinth, plinth_height):
        sketches = component.sketches
        extrudes = component.features.extrudeFeatures
        move_feats = component.features.moveFeatures

        yz_plane = component.yZConstructionPlane

        usable_width = width - 2 * thickness
        spacing = usable_width / (count + 1)

        effective_height = height - plinth_height if has_plinth else height
        panel_height = effective_height - 2 * thickness

        z_offset = (plinth_height + thickness) / MM_TO_CM if has_plinth else thickness / MM_TO_CM

        for i in range(count):
            x_position = thickness + spacing * (i + 1)

            sketch = sketches.add(yz_plane)
            sketch.sketchCurves.sketchLines.addTwoPointRectangle(
                adsk.core.Point3D.create(0, z_offset, 0),
                adsk.core.Point3D.create(depth / MM_TO_CM, z_offset + panel_height / MM_TO_CM, 0),
            )

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
    # ANTA E FERRAMENTA
    # -------------------------------------------------------------------------
    def _create_door_panel(
        self,
        component,
        width,
        height,
        depth,
        thickness,
        has_plinth,
        plinth_height,
        door_gap,
        door_overlay_left,
        door_overlay_right,
        door_overlay_top,
        door_overlay_bottom,
        door_thickness,
        params,
    ):
        """
        Anta a copertura carcassa, leggermente più piccola per i giochi:
        - X: [0,width] con gioco laterale
        - Z: [plinth_height,height] con gioco sopra e filo sotto
        """
        sketches = component.sketches
        extrudes = component.features.extrudeFeatures
        move_feats = component.features.moveFeatures

        side_gap_mm = 1.5
        top_gap_mm = 2.0
        bottom_gap_mm = 0.0

        carcass_x_min_mm = 0.0
        carcass_x_max_mm = width
        carcass_z_min_mm = plinth_height
        carcass_z_max_mm = height

        door_width_mm = (carcass_x_max_mm - carcass_x_min_mm) - 2 * side_gap_mm
        door_height_mm = (carcass_z_max_mm - carcass_z_min_mm) - top_gap_mm - bottom_gap_mm

        x_door_mm = carcass_x_min_mm + side_gap_mm
        z_door_mm = carcass_z_min_mm + bottom_gap_mm
        y_door_cm = depth / MM_TO_CM

        yz_plane = component.yZConstructionPlane
        sketch_door = sketches.add(yz_plane)

        sketch_door.sketchCurves.sketchLines.addTwoPointRectangle(
            adsk.core.Point3D.create(y_door_cm, z_door_mm / MM_TO_CM, 0),
            adsk.core.Point3D.create(
                y_door_cm + door_thickness / MM_TO_CM,
                (z_door_mm + door_height_mm) / MM_TO_CM,
                0,
            ),
        )

        extrude_input_door = extrudes.createInput(
            sketch_door.profiles.item(0),
            adsk.fusion.FeatureOperations.NewBodyFeatureOperation,
        )
        distance = adsk.core.ValueInput.createByReal(door_width_mm / MM_TO_CM)
        extrude_input_door.setDistanceExtent(False, distance)
        extrude_door = extrudes.add(extrude_input_door)
        door_body = extrude_door.bodies.item(0)
        door_body.name = "Anta"

        transform_door = adsk.core.Matrix3D.create()
        transform_door.translation = adsk.core.Vector3D.create(x_door_mm / MM_TO_CM, 0, 0)

        bodies_door = adsk.core.ObjectCollection.create()
        bodies_door.add(door_body)
        move_input_door = move_feats.createInput(bodies_door, transform_door)
        move_feats.add(move_input_door)

        try:
            fillet_feats = component.features.filletFeatures
            edge_collection = adsk.core.ObjectCollection.create()
            for edge in door_body.edges:
                edge_collection.add(edge)
            if edge_collection.count > 0:
                fillet_input = fillet_feats.createInput()
                radius_val = adsk.core.ValueInput.createByReal(2.0 / MM_TO_CM)
                fillet_input.addConstantRadiusEdgeSet(edge_collection, radius_val, True)
                fillet_feats.add(fillet_input)
        except:
            pass

        self._create_hinge_cup_holes(component, door_body, door_height_mm, door_thickness, params)

        for body in component.bRepBodies:
            if body.name == "Fianco_Sinistro":
                effective_height = height - plinth_height if has_plinth else height
                self._create_mounting_plate_holes(
                    component,
                    body,
                    effective_height,
                    depth,
                    thickness,
                    has_plinth,
                    plinth_height,
                    params,
                )
                break

    def _calculate_hinge_count(self, door_height):
        if door_height <= self.DEFAULT_HINGE_THRESHOLD_2:
            return 2
        elif door_height <= self.DEFAULT_HINGE_THRESHOLD_3:
            return 3
        else:
            return 4

    def _create_hinge_cup_holes(self, component, door_body, door_height, door_thickness, params):
        cup_diameter = params.get("cup_diameter", self.DEFAULT_CUP_DIAMETER)
        cup_depth = params.get("cup_depth", self.DEFAULT_CUP_DEPTH)
        cup_offset_k = params.get("cup_center_offset_from_edge", self.DEFAULT_CUP_CENTER_OFFSET_FROM_EDGE)
        hinge_offset_top = params.get("hinge_offset_top", self.DEFAULT_HINGE_OFFSET_TOP)
        hinge_offset_bottom = params.get("hinge_offset_bottom", self.DEFAULT_HINGE_OFFSET_BOTTOM)

        hinge_count = self._calculate_hinge_count(door_height)

        if hinge_count == 2:
            hinge_positions = [hinge_offset_top, door_height - hinge_offset_bottom]
        elif hinge_count == 3:
            middle = door_height / 2.0
            hinge_positions = [hinge_offset_top, middle, door_height - hinge_offset_bottom]
        else:
            spacing = (door_height - hinge_offset_top - hinge_offset_bottom) / 3.0
            hinge_positions = [
                hinge_offset_top,
                hinge_offset_top + spacing,
                hinge_offset_top + 2 * spacing,
                door_height - hinge_offset_bottom,
            ]

        self._hinge_positions = hinge_positions
        pass

    def _create_mounting_plate_holes(
        self, component, side_body, effective_height, depth, thickness, has_plinth, plinth_height, params
    ):
        system_line = params.get("mounting_plate_system_line", self.DEFAULT_MOUNTING_PLATE_SYSTEM_LINE)
        hole_spacing = params.get("mounting_plate_hole_spacing", self.DEFAULT_MOUNTING_PLATE_HOLE_SPACING)
        hole_diameter = params.get("mounting_plate_hole_diameter", self.DEFAULT_MOUNTING_PLATE_HOLE_DIAMETER)
        screw_depth = params.get("screw_depth", self.DEFAULT_SCREW_DEPTH)

        self._mounting_plate_system_line = system_line
        self._mounting_plate_hole_spacing = hole_spacing
        pass
