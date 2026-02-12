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

    # -------------------------------------------------------------------------
    # ANTA SINGOLA
    # -------------------------------------------------------------------------
    def create_door(self, params):
        """
        Crea un'anta singola.

        Params (tutti in mm, tranne dove indicato):
        - width: larghezza nominale dell'anta (spazio assegnato a questa anta)
        - height: altezza carcassa SOPRA lo zoccolo
                  (il wizard attuale passa dimensioni['altezza'] - plinth)
        - thickness: spessore anta
        - door_type: 'flat' | 'frame'
        - position: 'left' | 'right' | 'top' | 'bottom' (per naming / logica futura)
        - parent_component: componente del cabinet che fa da genitore
        - cabinet_depth: profondità mobile
        - cabinet_plinth_height: altezza zoccolo da pavimento
        - x_offset: offset X di questa anta rispetto al fianco sinistro del mobile
        - mounting_type: 'copertura_totale' | 'filo' | 'semicopertura'
        """

        # --- INPUT BASE ---
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

        # --- GIOCHI (per ora costanti, poi li renderemo parametrici) ---
        side_gap_mm = 1.5   # gioco per lato
        top_gap_mm = 2.0    # gioco sopra
        bottom_gap_mm = 0.0 # filo in basso

        # --- DIMENSIONI REALI ANTA ---
        door_width_mm = max(0.0, nominal_width_mm - 2 * side_gap_mm)
        door_height_mm = max(0.0, carcass_height_mm - top_gap_mm - bottom_gap_mm)

        # --- COMPONENTE TARGET ---
        target_comp = parent_component if parent_component else self.root_comp

        # --- TRASFORMAZIONE DI POSIZIONAMENTO ---
        transform = adsk.core.Matrix3D.create()

        # Y: anta davanti al fronte del mobile
        if cabinet_depth > 0:
            if mounting_type in ("copertura_totale", "filo"):
                # Anta a filo del fronte (spessore verso l'esterno)
                y_position_cm = (cabinet_depth - thickness) / 10.0
            else:  # 'semicopertura'
                y_position_cm = (cabinet_depth - thickness / 2.0) / 10.0
        else:
            y_position_cm = 0.0

        # Z: base anta = plinth + bottom_gap
        z_position_cm = (cabinet_plinth_height + bottom_gap_mm) / 10.0

        # X: fianco sinistro + offset di questo modulo + gioco lato sinistro
        x_position_cm = (x_offset_mm + side_gap_mm) / 10.0

        transform.translation = adsk.core.Vector3D.create(x_position_cm, y_position_cm, z_position_cm)

        # --- CREA COMPONENTE ANTA ---
        occurrence = target_comp.occurrences.addNewComponent(transform)
        door_comp = occurrence.component
        door_comp.name = f"Anta_{position.capitalize()}_{int(door_width_mm)}x{int(door_height_mm)}"

        # --- GEOMETRIA INTERNA ANTA (origine locale 0,0,0) ---
        if door_type == "flat":
            self._create_flat_door(door_comp, door_width_mm, door_height_mm, thickness)
        elif door_type == "frame":
            self._create_frame_door(door_comp, door_width_mm, door_height_mm, thickness)

        return door_comp

    # -------------------------------------------------------------------------
    # ANTE DOPPIE (wrapper su create_door, pensato per estensioni future)
    # -------------------------------------------------------------------------
    def create_double_door(self, params):
        """
        Crea una coppia di ante doppie.

        Args:
            params: Dizionario con parametri
                - total_width: Larghezza totale (mm)
                - height: Altezza carcassa sopra zoccolo (mm)
                - thickness: Spessore (mm, default 18)
                - gap: Distanza tra le ante (mm, default 3)
                - door_type: Tipo anta ('flat'/'frame')
                - parent_component: Componente genitore (cabinet) - opzionale
                - cabinet_depth: Profondità mobile per posizionamento (mm)
                - cabinet_plinth_height: Altezza zoccolo per posizionamento Z (mm)
                - x_offset: Offset X iniziale per posizionamento (mm, default 0)
                - mounting_type: Tipo montaggio ('copertura_totale', 'filo', 'semicopertura')

        Returns:
            tuple: (componente_sinistra, componente_destra)
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

        # Calcola larghezza singola anta
        single_width = (total_width - gap) / 2.0

        # Anta sinistra
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

        # Anta destra
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

        return left_door, right_door

    # -------------------------------------------------------------------------
    # GEOMETRIA ANTA
    # -------------------------------------------------------------------------
    def _create_flat_door(self, component, width, height, thickness):
        """
        Crea anta piatta (pannello singolo).

        Args:
            component: Componente destinazione
            width, height, thickness: Dimensioni in mm
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

        # Smusso base sui bordi (R=2mm) utile per rendering
        try:
            fillet_feats = component.features.filletFeatures
            edge_collection = adsk.core.ObjectCollection.create()
            for edge in body.edges:
                edge_collection.add(edge)
            if edge_collection.count > 0:
                fillet_input = fillet_feats.createInput()
                radius_val = adsk.core.ValueInput.createByReal(2.0 / 10.0)  # 2 mm
                fillet_input.addConstantRadiusEdgeSet(edge_collection, radius_val, True)
                fillet_feats.add(fillet_input)
        except:
            pass

    def _create_frame_door(self, component, width, height, thickness):
        """
        Crea anta con telaio (stile shaker semplificato).

        Args:
            component: Componente destinazione
            width, height, thickness: Dimensioni in mm
        """
        frame_width = 60  # Larghezza telaio (mm)

        sketches = component.sketches
        extrudes = component.features.extrudeFeatures

        xy_plane = component.xYConstructionPlane

        sketch = sketches.add(xy_plane)
        lines = sketch.sketchCurves.sketchLines

        # Rettangolo esterno
        lines.addTwoPointRectangle(
            adsk.core.Point3D.create(0, 0, 0),
            adsk.core.Point3D.create(width / 10.0, height / 10.0, 0),
        )

        # Rettangolo interno (vuoto)
        lines.addTwoPointRectangle(
            adsk.core.Point3D.create(frame_width / 10.0, frame_width / 10.0, 0),
            adsk.core.Point3D.create((width - frame_width) / 10.0, (height - frame_width) / 10.0, 0),
        )

        # Estrudi telaio
        extrude_input = extrudes.createInput(
            sketch.profiles.item(0), adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        distance = adsk.core.ValueInput.createByReal(thickness / 10.0)
        extrude_input.setDistanceExtent(False, distance)
        extrude_frame = extrudes.add(extrude_input)
        extrude_frame.bodies.item(0).name = "Telaio_Anta"

        # Pannello centrale ribassato
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
    # PREPARAZIONE CERNIERE (placeholder, già esistente)
    # -------------------------------------------------------------------------
    def add_hinge_preparation(self, door_comp, hinge_type="clip_top", hinge_count=2):
        """
        Aggiunge le preparazioni per le cerniere.

        Args:
            door_comp: Componente anta
            hinge_type: Tipo cerniera ('clip_top', 'standard')
            hinge_count: Numero di cerniere

        Returns:
            list: Lista di feature create
        """
        features = []

        bbox = door_comp.bRepBodies.item(0).boundingBox
        height = (bbox.maxPoint.z - bbox.minPoint.z) * 10  # cm to mm

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
        Crea un foro per cerniera.

        Args:
            component: Componente destinazione
            z_position: Posizione Z del foro (mm)
            diameter: Diametro foro (mm)
            depth: Profondità foro (mm)
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
                diameter / 20.0,  # mm -> cm, raggio
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
