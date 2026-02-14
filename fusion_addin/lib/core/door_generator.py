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
        self.logger = setup_logger('DoorGenerator')

    # -------------------------------------------------------------------------
    # ANTA SINGOLA
    # -------------------------------------------------------------------------
    def create_door(self, params):
        """
        Crea un'anta singola con geometria e posizionamento.
        
        IMPORTANTE - Sistema di coordinate:
        - X: Larghezza mobile (sinistra → destra, origine = fianco sinistro)
        - Y: Profondità mobile (retro → fronte, origine = retro mobile)
        - Z: Altezza mobile (pavimento → top, origine = pavimento)
        
        IMPORTANTE - Carcassa (cabinet carcass):
        - Base carcassa in Z = plinth_height (top dello zoccolo)
        - Top carcassa in Z = total_height (top mobile)
        - Altezza carcassa = total_height - plinth_height
        
        IMPORTANTE - Posizionamento anta:
        - Base anta in Z = plinth_height (allineata a base carcassa)
        - Altezza anta = carcass_height - top_gap (gioco superiore 2mm di default)
        - Top anta in Z = plinth_height + door_height
        
        Parametri (tutti in mm salvo indicazioni):
        - width: Larghezza nominale anta (spazio allocato a questa anta)
        - height: Altezza carcassa SOPRA lo zoccolo (= total_height - plinth_height)
        - thickness: Spessore anta in mm
        - door_type: Tipo anta ('flat' per pannello piatto, 'frame' per telaio)
        - position: Posizione anta ('left', 'right', 'center', etc.) per naming
        - parent_component: Componente cabinet genitore (per nested hierarchy)
        - cabinet_depth: Profondità mobile in mm (per posizionamento Y)
        - cabinet_plinth_height: Altezza zoccolo in mm (per posizionamento Z base)
        - x_offset: Offset X da bordo sinistro mobile in mm
        - mounting_type: Tipo montaggio ('copertura_totale', 'filo', 'semicopertura')
        
        Returns:
            adsk.fusion.Component: Componente anta creato e posizionato
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

        # DEBUG POPUP PARAMETRI INPUT
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
            # Se il popup fallisce (es. in test headless), proseguiamo comunque
            pass

        self.logger.info("=" * 70)
        self.logger.info(f"🚪 Creazione anta singola: {position}")
        self.logger.info(f"   Larghezza nominale: {nominal_width_mm}mm")
        self.logger.info(f"   Altezza carcassa: {carcass_height_mm}mm")
        self.logger.info(f"   Spessore: {thickness}mm")
        self.logger.info(f"   Tipo: {door_type}, Montaggio: {mounting_type}")
        self.logger.info(f"   Plinth height: {cabinet_plinth_height}mm")
        self.logger.info(f"   X offset: {x_offset_mm}mm")

        # --- GIOCHI (gap) PER FUNZIONAMENTO CERNIERE ---
        side_gap_mm = 1.5   # gioco laterale per lato (totale 3mm tra ante adiacenti)
        top_gap_mm = 2.0    # gioco superiore (anta non tocca cielo/top)
        bottom_gap_mm = 0.0 # filo in basso (anta allineata a base carcassa)

        # --- DIMENSIONI REALI ANTA (sottratti i giochi) ---
        door_width_mm = max(0.0, nominal_width_mm - 2 * side_gap_mm)
        door_height_mm = max(0.0, carcass_height_mm - top_gap_mm - bottom_gap_mm)
        
        self.logger.info(
            f"   Gap applicati: laterale={side_gap_mm}mm, "
            f"alto={top_gap_mm}mm, basso={bottom_gap_mm}mm"
        )
        self.logger.info(
            f"   Dimensioni reali anta: {door_width_mm}mm × {door_height_mm}mm × {thickness}mm"
        )

        # --- COMPONENTE TARGET (genitore per nested structure) ---
        target_comp = parent_component if parent_component else self.root_comp

        # --- CALCOLO TRASFORMAZIONE DI POSIZIONAMENTO ---
        transform = adsk.core.Matrix3D.create()

        # Posizione Y: anta posizionata davanti al fronte del mobile
        if cabinet_depth > 0:
            if mounting_type in ("copertura_totale", "filo"):
                # Anta a filo fronte: Y = depth - thickness
                y_position_cm = (cabinet_depth - thickness) / 10.0
            else:  # 'semicopertura'
                # Anta a metà spessore: Y = depth - thickness/2
                y_position_cm = (cabinet_depth - thickness / 2.0) / 10.0
        else:
            y_position_cm = 0.0

        # Posizione Z: base anta allineata alla base della carcassa
        z_position_cm = (cabinet_plinth_height + bottom_gap_mm) / 10.0

        # Posizione X: offset dal fianco sinistro + gap sinistro
        x_position_cm = (x_offset_mm + side_gap_mm) / 10.0

        self.logger.info("   Posizionamento anta (coordinate Fusion 360 in cm):")
        self.logger.info(
            f"      X = {x_position_cm:.2f}cm "
            f"(offset={x_offset_mm}mm + gap={side_gap_mm}mm)"
        )
        self.logger.info(
            f"      Y = {y_position_cm:.2f}cm "
            f"(depth={cabinet_depth}mm - thickness={thickness}mm)"
        )
        self.logger.info(
            f"      Z = {z_position_cm:.2f}cm "
            f"(plinth={cabinet_plinth_height}mm + gap_bottom={bottom_gap_mm}mm)"
        )
        
        # Range Z utile dell'anta (in mm)
        door_z_base_mm = cabinet_plinth_height + bottom_gap_mm
        door_z_top_mm = door_z_base_mm + door_height_mm
        self.logger.info(f"   Range Z anta: [{door_z_base_mm}mm, {door_z_top_mm}mm]")

        transform.translation = adsk.core.Vector3D.create(
            x_position_cm, y_position_cm, z_position_cm
        )

        # --- CREA COMPONENTE ANTA ---
        occurrence = target_comp.occurrences.addNewComponent(transform)
        door_comp = occurrence.component
        door_comp.name = f"Anta_{position.capitalize()}_{int(door_width_mm)}x{int(door_height_mm)}"
        
        self.logger.info(f"   Componente creato: {door_comp.name}")

        # --- GEOMETRIA INTERNA ANTA (origine locale 0,0,0) ---
        if door_type == "flat":
            self._create_flat_door(door_comp, door_width_mm, door_height_mm, thickness)
            self.logger.info("   Geometria: anta piatta (flat)")
        elif door_type == "frame":
            self._create_frame_door(door_comp, door_width_mm, door_height_mm, thickness)
            self.logger.info("   Geometria: anta a telaio (frame)")

                # DEBUG: bounding box anta (popup)
        try:
            if door_comp.bRepBodies.count > 0:
                bbox = door_comp.bRepBodies.item(0).boundingBox
                app = adsk.core.Application.get()
                ui = app.userInterface
                ui.messageBox(
                    f"DEBUG ANTA BBOX:\n"
                    f"x=({bbox.minPoint.x:.2f}, {bbox.maxPoint.x:.2f}) cm\n"
                    f"y=({bbox.minPoint.y:.2f}, {bbox.maxPoint.y:.2f}) cm\n"
                    f"z=({bbox.minPoint.z:.2f}, {bbox.maxPoint.z:.2f}) cm"
                )
        except:
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
        
        Wrapper di convenienza su create_door().
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

        # Larghezza singola anta
        single_width = (total_width - gap) / 2.0
        self.logger.info(f"   Larghezza singola anta: {single_width}mm")

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

        # Sketch rettangolare
        sketch = sketches.add(xy_plane)
        sketch.sketchCurves.sketchLines.addTwoPointRectangle(
            adsk.core.Point3D.create(0, 0, 0),
            adsk.core.Point3D.create(width / 10.0, height / 10.0, 0),  # mm → cm
        )

        # Estrusione
        extrude_input = extrudes.createInput(
            sketch.profiles.item(0), adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        distance = adsk.core.ValueInput.createByReal(thickness / 10.0)  # mm → cm
        extrude_input.setDistanceExtent(False, distance)
        extrude = extrudes.add(extrude_input)
        body = extrude.bodies.item(0)
        body.name = "Pannello_Anta"

        # Smusso R=2mm su tutti i bordi
        try:
            fillet_feats = component.features.filletFeatures
            edge_collection = adsk.core.ObjectCollection.create()
            for edge in body.edges:
                edge_collection.add(edge)
            if edge_collection.count > 0:
                fillet_input = fillet_feats.createInput()
                radius_val = adsk.core.ValueInput.createByReal(2.0 / 10.0)  # 2mm → 0.2cm
                fillet_input.addConstantRadiusEdgeSet(edge_collection, radius_val, True)
                fillet_feats.add(fillet_input)
        except:
            # Se il fillet fallisce non è critico
            pass

    def _create_frame_door(self, component, width, height, thickness):
        """
        Crea geometria anta a telaio (stile shaker semplificato).
        """
        frame_width = 60  # mm

        sketches = component.sketches
        extrudes = component.features.extrudeFeatures

        xy_plane = component.xYConstructionPlane

        # Telaio perimetrale
        sketch = sketches.add(xy_plane)
        lines = sketch.sketchCurves.sketchLines

        # Rettangolo esterno
        lines.addTwoPointRectangle(
            adsk.core.Point3D.create(0, 0, 0),
            adsk.core.Point3D.create(width / 10.0, height / 10.0, 0),
        )

        # Rettangolo interno (vuoto centrale)
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
    # PREPARAZIONE CERNIERE (placeholder)
    # -------------------------------------------------------------------------
    def add_hinge_preparation(self, door_comp, hinge_type="clip_top", hinge_count=2):
        """
        Aggiunge le preparazioni per le cerniere (fori tazza).
        """
        features = []

        # Calcola altezza anta dal bounding box
        bbox = door_comp.bRepBodies.item(0).boundingBox
        height = (bbox.maxPoint.z - bbox.minPoint.z) * 10  # cm → mm

        # Posizioni verticali cerniere
        if hinge_count == 2:
            positions = [height * 0.15, height * 0.85]
        elif hinge_count == 3:
            positions = [height * 0.1, height * 0.5, height * 0.9]
        else:
            spacing = height / (hinge_count + 1)
            positions = [spacing * (i + 1) for i in range(hinge_count)]

        if hinge_type == "clip_top":
            hole_diameter = 35  # mm
            hole_depth = 12     # mm

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

            # Centro Y = metà profondità anta
            bbox = component.bRepBodies.item(0).boundingBox
            y_center = (bbox.maxPoint.y - bbox.minPoint.y) / 2.0

            center_point = adsk.core.Point3D.create(0, y_center, z_position / 10.0)  # mm → cm
            
            sketch.sketchCurves.sketchCircles.addByCenterRadius(
                center_point,
                diameter / 20.0,  # mm → cm, diametro → raggio
            )

            extrude_input = extrudes.createInput(
                sketch.profiles.item(0), adsk.fusion.FeatureOperations.CutFeatureOperation
            )
            distance = adsk.core.ValueInput.createByReal(depth / 10.0)  # mm → cm
            extrude_input.setDistanceExtent(False, distance)
            extrude = extrudes.add(extrude_input)

            return extrude
        except:
            return None
