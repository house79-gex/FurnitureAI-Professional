"""
Generatore di ante (porte) singole e doppie per mobili
Supporta diverse tipologie di apertura e montaggio

RESPONSABILITÀ:
- Crea geometria ante (flat o frame)
- Posiziona ante nello spazio 3D relativo alla carcassa
- Applica giochi (gap) standard per funzionamento cerniere
- Gestisce montaggio copertura totale, filo, semicopertura

NON RESPONSABILE DI:
- Calcolo numero ante (vedi DoorDesigner)
- Calcolo larghezze ante (vedi DoorDesigner)
- Calcolo offset X (vedi DoorDesigner)
- Logica di business configurazione ante (vedi DoorDesigner)
"""

import adsk.core
import adsk.fusion
import math
from ..logging_utils import setup_logger


class DoorGenerator:
    """
    Generatore di ante per mobili
    
    Genera la geometria fisica delle ante e le posiziona correttamente
    rispetto alla carcassa del mobile. Riceve configurazioni complete
    da DoorDesigner e crea i componenti 3D corrispondenti.
    """

    def __init__(self, design):
        """
        Inizializza il generatore di ante

        Args:
            design: Istanza di adsk.fusion.Design
        """
        self.design = design
        self.root_comp = design.rootComponent
        self.logger = setup_logger("DoorGenerator")

    # -------------------------------------------------------------------------
    # ANTA SINGOLA (con riallineamento via bounding box)
    # -------------------------------------------------------------------------
    def create_door(self, params):
        """
        Crea un'anta singola con geometria e posizionamento.

        NOTA IMPORTANTE:
        - Il CabinetGenerator corrente usa Y come asse di ALTEZZA
          e Z come PROFONDITÀ.
        - Questo metodo crea l'anta nel suo componente locale
          (altezza su Y, spessore su Z) e poi la riallinea al cabinet
          usando i bounding box di cabinet e anta.
        """

        # --- INPUT PARAMETRI ---
        nominal_width_mm = params.get("width", 400)
        carcass_height_mm = params.get("height", 700)  # altezza carcassa sopra zoccolo
        thickness = params.get("thickness", 18)
        door_type = params.get("door_type", "flat")
        position = params.get("position", "left")
        parent_component = params.get("parent_component", None)
        cabinet_depth = params.get("cabinet_depth", 0)
        cabinet_plinth_height = params.get("cabinet_plinth_height", 0)
        x_offset_mm = params.get("x_offset", 0)
        mounting_type = params.get("mounting_type", "copertura_totale")

        # DEBUG popup parametri in ingresso
        try:
            app = adsk.core.Application.get()
            ui = app.userInterface
            ui.messageBox(
                f"DEBUG DOOR:\n"
                f"width={nominal_width_mm}\n"
                f"height={carcass_height_mm}\n"
                f"depth={cabinet_depth}\n"
                f"plinth={cabinet_plinth_height}\n"
                f"x_offset={x_offset_mm}"
            )
        except:
            pass

        self.logger.info("=" * 70)
        self.logger.info(f"🚪 Creazione anta singola: {position}")
        self.logger.info(f"   Larghezza nominale: {nominal_width_mm}mm")
        self.logger.info(f"   Altezza carcassa: {carcass_height_mm}mm")
        self.logger.info(f"   Spessore: {thickness}mm")
        self.logger.info(f"   Tipo: {door_type}, Montaggio: {mounting_type}")
        self.logger.info(f"   Plinth height: {cabinet_plinth_height}mm")
        self.logger.info(f"   X offset: {x_offset_mm}mm")

        # --- GIOCHI ---
        side_gap_mm = 1.5
        top_gap_mm = 2.0
        bottom_gap_mm = 0.0

        door_width_mm = max(0.0, nominal_width_mm - 2 * side_gap_mm)
        door_height_mm = max(0.0, carcass_height_mm - top_gap_mm - bottom_gap_mm)

        self.logger.info(
            f"   Gap: laterale={side_gap_mm}mm, alto={top_gap_mm}mm, basso={bottom_gap_mm}mm"
        )
        self.logger.info(
            f"   Dimensioni reali anta: {door_width_mm}mm × {door_height_mm}mm × {thickness}mm"
        )

        # --- COMPONENTE TARGET ---
        target_comp = parent_component if parent_component else self.root_comp

        # --- TRASFORMAZIONE INIZIALE ---
        transform = adsk.core.Matrix3D.create()

        # X: offset laterale calcolato da DoorDesigner
        x_position_cm = (x_offset_mm + side_gap_mm) / 10.0

        # Y/Z: inizialmente 0, poi correggiamo via bounding box
        y_position_cm = 0.0
        z_position_cm = 0.0

        transform.translation = adsk.core.Vector3D.create(
            x_position_cm, y_position_cm, z_position_cm
        )

        self.logger.info(
            f"   Posizionamento iniziale anta: "
            f"X={x_position_cm:.2f}cm, Y={y_position_cm:.2f}cm, Z={z_position_cm:.2f}cm "
            f"(correzione via bbox successiva)"
        )

        # --- CREA COMPONENTE ANTA ---
        occurrence = target_comp.occurrences.addNewComponent(transform)
        door_comp = occurrence.component
        door_comp.name = f"Anta_{position.capitalize()}_{int(door_width_mm)}x{int(door_height_mm)}"

        self.logger.info(f"   Componente creato: {door_comp.name}")

        # --- GEOMETRIA INTERNA (locale: altezza su Y, spessore su Z) ---
        if door_type == "flat":
            self._create_flat_door(door_comp, door_width_mm, door_height_mm, thickness)
            self.logger.info("   Geometria: anta piatta (flat)")
        elif door_type == "frame":
            self._create_frame_door(door_comp, door_width_mm, door_height_mm, thickness)
            self.logger.info("   Geometria: anta a telaio (frame)")

        # --- RIALLINEAMENTO VIA BOUNDING BOX ---
        try:
            app = adsk.core.Application.get()
            ui = app.userInterface

            # 1) bounding box anta
            if door_comp.bRepBodies.count == 0:
                self.logger.warning("DEBUG ANTA: nessun body, skip riallineamento")
                self.logger.info("✅ Anta completata (senza riallineamento)")
                self.logger.info("=" * 70)
                return door_comp

            door_body = door_comp.bRepBodies.item(0)
            door_bbox = door_body.boundingBox

            ui.messageBox(
                f"DEBUG ANTA BBOX:\n"
                f"x=({door_bbox.minPoint.x:.2f}, {door_bbox.maxPoint.x:.2f}) cm\n"
                f"y=({door_bbox.minPoint.y:.2f}, {door_bbox.maxPoint.y:.2f}) cm\n"
                f"z=({door_bbox.minPoint.z:.2f}, {door_bbox.maxPoint.z:.2f}) cm"
            )

            # 2) bounding box cabinet (prendiamo il primo body del parent_component)
            if target_comp.bRepBodies.count == 0:
                self.logger.warning("DEBUG CABINET: nessun body nel parent_component")
                self.logger.info("✅ Anta completata (senza riallineamento)")
                self.logger.info("=" * 70)
                return door_comp

            cab_body = target_comp.bRepBodies.item(0)
            cab_bbox = cab_body.boundingBox

            ui.messageBox(
                f"DEBUG CABINET BBOX:\n"
                f"x=({cab_bbox.minPoint.x:.2f}, {cab_bbox.maxPoint.x:.2f}) cm\n"
                f"y=({cab_bbox.minPoint.y:.2f}, {cab_bbox.maxPoint.y:.2f}) cm\n"
                f"z=({cab_bbox.minPoint.z:.2f}, {cab_bbox.maxPoint.z:.2f}) cm"
            )

            # Nel cabinet attuale:
            # - Y è ALTEZZA (es. 10→72 cm),
            # - Z è PROFONDITÀ (-58→0, fronte a 0).
            #
            # Nell'anta:
            # - Y è ALTEZZA (0→~61.6),
            # - Z è SPESSORE (0→~1.8 verso +Z).
            #
            # Obiettivo:
            # - base anta alla base carcassa: Y_min_anta = Y_min_carcassa
            # - faccia posteriore anta sul fronte carcassa: Z_max_anta = Z_max_carcassa

            desired_door_y_min = cab_bbox.minPoint.y         # base carcassa (include zoccolo)
            desired_door_z_max = cab_bbox.maxPoint.z         # fronte carcassa (tipicamente 0)

            current_door_y_min = door_bbox.minPoint.y
            current_door_z_max = door_bbox.maxPoint.z

            delta_y = desired_door_y_min - current_door_y_min
            delta_z = desired_door_z_max - current_door_z_max

            self.logger.info(
                f"   Riallineamento via bbox: delta_y={delta_y:.2f}cm, delta_z={delta_z:.2f}cm"
            )

            # Traslazione di correzione su tutti i corpi dell'anta
            move_feats = door_comp.features.moveFeatures
            bodies = adsk.core.ObjectCollection.create()
            for body in door_comp.bRepBodies:
                bodies.add(body)

            fix_transform = adsk.core.Matrix3D.create()
            fix_transform.translation = adsk.core.Vector3D.create(0, delta_y, delta_z)

            move_input = move_feats.createInput(bodies, fix_transform)
            move_feats.add(move_input)

        except:
            # se qualcosa fallisce nel riallineamento, lasciamo l'anta dov'è
            pass

        self.logger.info(f"✅ Anta {position} completata")
        self.logger.info("=" * 70)

        return door_comp

    # -------------------------------------------------------------------------
    # ANTE DOPPIE
    # -------------------------------------------------------------------------
    def create_double_door(self, params):
        """
        Crea una coppia di ante doppie (destra e sinistra).
        """
        total_width = params.get("total_width", 800)
        carcass_height_mm = params.get("height", 700)
        thickness = params.get("thickness", 18)
        gap = params.get("gap", 3)
        door_type = params.get("door_type", "flat")
        parent_component = params.get("parent_component", None)
        cabinet_depth = params.get("cabinet_depth", 0)
        cabinet_plinth_height = params.get("cabinet_plinth_height", 0)
        x_offset = params.get("x_offset", 0)
        mounting_type = params.get("mounting_type", "copertura_totale")

        self.logger.info("=" * 70)
        self.logger.info("🚪🚪 Creazione coppia ante doppie")
        self.logger.info(f"   Larghezza totale: {total_width}mm, Gap centrale: {gap}mm")

        single_width = (total_width - gap) / 2.0
        self.logger.info(f"   Larghezza singola anta: {single_width}mm")

        left_params = {
            "width": single_width,
            "height": carcass_height_mm,
            "thickness": thickness,
            "door_type": door_type,
            "position": "left",
            "parent_component": parent_component,
            "cabinet_depth": cabinet_depth,
            "cabinet_plinth_height": cabinet_plinth_height,
            "x_offset": x_offset,
            "mounting_type": mounting_type,
        }
        left_door = self.create_door(left_params)

        right_params = {
            "width": single_width,
            "height": carcass_height_mm,
            "thickness": thickness,
            "door_type": door_type,
            "position": "right",
            "parent_component": parent_component,
            "cabinet_depth": cabinet_depth,
            "cabinet_plinth_height": cabinet_plinth_height,
            "x_offset": x_offset + single_width + gap,
            "mounting_type": mounting_type,
        }
        right_door = self.create_door(right_params)

        self.logger.info("✅ Coppia ante doppie completata")
        self.logger.info("=" * 70)

        return left_door, right_door

    # -------------------------------------------------------------------------
    # GEOMETRIA ANTE
    # -------------------------------------------------------------------------
    def _create_flat_door(self, component, width, height, thickness):
        """
        Crea geometria anta piatta (pannello singolo).
        """
        sketches = component.sketches
        extrudes = component.features.extrudeFeatures

        xy_plane = component.xYConstructionPlane

        sketch = sketches.add(xy_plane)
        sketch.sketchCurves.sketchLines.addTwoPointRectangle(
            adsk.core.Point3D.create(0, 0, 0),
            adsk.core.Point3D.create(width / 10.0, height / 10.0, 0),
        )

        extrude_input = extrudes.createInput(
            sketch.profiles.item(0), adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        distance = adsk.core.ValueInput.createByReal(thickness / 10.0)
        extrude_input.setDistanceExtent(False, distance)
        extrude = extrudes.add(extrude_input)
        body = extrude.bodies.item(0)
        body.name = "Pannello_Anta"

        # Smusso R=2mm
        try:
            fillet_feats = component.features.filletFeatures
            edge_collection = adsk.core.ObjectCollection.create()
            for edge in body.edges:
                edge_collection.add(edge)
            if edge_collection.count > 0:
                fillet_input = fillet_feats.createInput()
                radius_val = adsk.core.ValueInput.createByReal(2.0 / 10.0)
                fillet_input.addConstantRadiusEdgeSet(edge_collection, radius_val, True)
                fillet_feats.add(fillet_input)
        except:
            pass

    def _create_frame_door(self, component, width, height, thickness):
        """
        Crea geometria anta a telaio (stile shaker semplificato).
        """
        frame_width = 60  # mm

        sketches = component.sketches
        extrudes = component.features.extrudeFeatures

        xy_plane = component.xYConstructionPlane

        sketch = sketches.add(xy_plane)
        lines = sketch.sketchCurves.sketchLines

        lines.addTwoPointRectangle(
            adsk.core.Point3D.create(0, 0, 0),
            adsk.core.Point3D.create(width / 10.0, height / 10.0, 0),
        )

        lines.addTwoPointRectangle(
            adsk.core.Point3D.create(frame_width / 10.0, frame_width / 10.0, 0),
            adsk.core.Point3D.create((width - frame_width) / 10.0, (height - frame_width) / 10.0, 0),
        )

        extrude_input = extrudes.createInput(
            sketch.profiles.item(0), adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        distance = adsk.core.ValueInput.createByReal(thickness / 10.0)
        extrude_input.setDistanceExtent(False, distance)
        extrude_frame = extrudes.add(extrude_input)
        extrude_frame.bodies.item(0).name = "Telaio_Anta"

        panel_thickness = thickness - 4  # mm

        sketch_panel = sketches.add(xy_plane)
        sketch_panel.sketchCurves.sketchLines.addTwoPointRectangle(
            adsk.core.Point3D.create((frame_width + 5) / 10.0, (frame_width + 5) / 10.0, 0),
            adsk.core.Point3D.create((width - frame_width - 5) / 10.0, (height - frame_width - 5) / 10.0, 0),
        )

        extrude_input_panel = extrudes.createInput(
            sketch_panel.profiles.item(0), adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        distance_panel = adsk.core.ValueInput.createByReal(panel_thickness / 10.0)
        extrude_input_panel.setDistanceExtent(False, distance_panel)
        extrude_panel = extrudes.add(extrude_input_panel)
        extrude_panel.bodies.item(0).name = "Pannello_Centrale"

    # -------------------------------------------------------------------------
    # PREPARAZIONE CERNIERE (placeholder)
    # -------------------------------------------------------------------------
    def add_hinge_preparation(self, door_comp, hinge_type="clip_top", hinge_count=2):
        """
        Aggiunge le preparazioni per le cerniere (fori tazza).
        """
        features = []

        bbox = door_comp.bRepBodies.item(0).boundingBox
        height = (bbox.maxPoint.z - bbox.minPoint.z) * 10  # cm → mm

        if hinge_count == 2:
            positions = [height * 0.15, height * 0.85]
        elif hinge_count == 3:
            positions = [height * 0.1, height * 0.5, height * 0.9]
        else:
            spacing = height / (hinge_count + 1)
            positions = [spacing * (i + 1) for i in range(hinge_count)]

        if hinge_type == "clip_top":
            hole_diameter = 35
            hole_depth = 12

            for pos in positions:
                feature = self._create_hinge_hole(door_comp, pos, hole_diameter, hole_depth)
                if feature:
                    features.append(feature)

        return features

    def _create_hinge_hole(self, component, z_position, diameter, depth):
        """
        Crea un singolo foro per cerniera (foro tazza).
        """
        try:
            sketches = component.sketches
            extrudes = component.features.extrudeFeatures

            yz_plane = component.yZConstructionPlane
            sketch = sketches.add(yz_plane)

            bbox = component.bRepBodies.item(0).boundingBox
            y_center = (bbox.maxPoint.y - bbox.minPoint.y) / 2.0

            center_point = adsk.core.Point3D.create(0, y_center, z_position / 10.0)
            
            sketch.sketchCurves.sketchCircles.addByCenterRadius(
                center_point,
                diameter / 20.0,
            )

            extrude_input = extrudes.createInput(
                sketch.profiles.item(0), adsk.fusion.FeatureOperations.CutFeatureOperation
            )
            distance = adsk.core.ValueInput.createByReal(depth / 10.0)
            extrude_input.setDistanceExtent(False, distance)
            extrude = extrudes.add(extrude_input)

            return extrude
        except:
            return None
