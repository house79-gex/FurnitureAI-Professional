"""
Generatore di ante (porte) singole e doppie per mobili
Supporta diverse tipologie di apertura e montaggio

RESPONSABILITÀ:
- Crea geometria ante (flat o frame)
- Posiziona ante nello spazio 3D relativo alla carcassa
- Applica giochi (gap) standard per funzionamento cerniere
- Gestisce montaggio copertura totale, filo, semicopertura
- Usa bounding box della carcassa per allineamento preciso

SISTEMA COORDINATE (allineato con Fusion 360 e CabinetGenerator):
- Cabinet (world): X=larghezza, Y=altezza, Z=profondità
- Door (local, prima rotazione): X=larghezza, Y=altezza, Z=spessore
- Trasformazione: Rotazione 90° attorno X per mapping door→cabinet
- Allineamento finale: usa bounding box cabinet per posizionamento preciso

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
        
        SISTEMA COORDINATE CABINET (world, allineato con Fusion 360):
        - X: Larghezza (0 = fianco sinistro → width = fianco destro)
        - Y: Altezza (0 = pavimento → height = top mobile)
        - Z: Profondità (0 = retro → depth = fronte)
        
        SISTEMA COORDINATE DOOR (local, prima della trasformazione):
        - X: Larghezza anta (0 → width)
        - Y: Altezza anta (0 → height)
        - Z: Spessore anta (0 → thickness)
        
        TRASFORMAZIONE & POSIZIONAMENTO:
        1. Geometria creata su piano XY locale (door coords)
        2. Allineamento finale via bounding box:
           - Base anta (Y_min) → base carcassa
           - Fronte interno anta (Z_min) → fronte carcassa
           - Spessore anta si sviluppa verso +Z (esterno)
        
        Parametri (tutti in mm):
        - width: Larghezza nominale anta
        - height: Altezza carcassa sopra zoccolo
        - thickness: Spessore anta
        - door_type: 'flat' o 'frame'
        - position: Posizione per naming ('left', 'right', 'center')
        - parent_component: Componente cabinet genitore
        - cabinet_depth: Profondità mobile (per posizionamento Z)
        - cabinet_plinth_height: Altezza zoccolo (per posizionamento Y base)
        - x_offset: Offset X da bordo sinistro
        - mounting_type: 'copertura_totale', 'filo', 'semicopertura'
        
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

        # --- CREA COMPONENTE ANTA (inizialmente senza trasformazione) ---
        transform_identity = adsk.core.Matrix3D.create()
        occurrence = target_comp.occurrences.addNewComponent(transform_identity)
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

        # DEBUG opzionale bounding box anta subito dopo la creazione
        try:
            if door_comp.bRepBodies.count > 0:
                door_body = door_comp.bRepBodies.item(0)
                bbox = door_body.boundingBox
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
        
        # --- RIALLINEAMENTO FINALE VIA BOUNDING BOX ---
        try:
            if door_comp.bRepBodies.count == 0:
                self.logger.warning("   ⚠️ Nessun body creato nell'anta, salto riallineamento")
                return door_comp
            
            # Bbox anta
            door_body = door_comp.bRepBodies.item(0)
            door_bbox_local = door_body.boundingBox
            
            self.logger.info(f"   📦 Bbox anta (locale, prima riallineamento):")
            self.logger.info(f"      X: [{door_bbox_local.minPoint.x:.2f}, {door_bbox_local.maxPoint.x:.2f}] cm")
            self.logger.info(f"      Y: [{door_bbox_local.minPoint.y:.2f}, {door_bbox_local.maxPoint.y:.2f}] cm")
            self.logger.info(f"      Z: [{door_bbox_local.minPoint.z:.2f}, {door_bbox_local.maxPoint.z:.2f}] cm")
            
            # Bbox carcassa (fianco sinistro se possibile)
            cabinet_bbox = None
            reference_body_name = "N/A"
            if parent_component and parent_component.bRepBodies.count > 0:
                for body in parent_component.bRepBodies:
                    if "Fianco_Sinistro" in body.name or "Fianco_Sinistra" in body.name:
                        cabinet_bbox = body.boundingBox
                        reference_body_name = body.name
                        break
                if not cabinet_bbox:
                    reference_body_name = parent_component.bRepBodies.item(0).name
                    cabinet_bbox = parent_component.bRepBodies.item(0).boundingBox
            
            if cabinet_bbox:
                self.logger.info(f"   📦 Bbox carcassa ({reference_body_name}):")
                self.logger.info(f"      X: [{cabinet_bbox.minPoint.x:.2f}, {cabinet_bbox.maxPoint.x:.2f}] cm")
                self.logger.info(f"      Y: [{cabinet_bbox.minPoint.y:.2f}, {cabinet_bbox.maxPoint.y:.2f}] cm")
                self.logger.info(f"      Z: [{cabinet_bbox.minPoint.z:.2f}, {cabinet_bbox.maxPoint.z:.2f}] cm")
                
                # 1. X: posizione da x_offset + side_gap
                desired_x_min_cm = (x_offset_mm + side_gap_mm) / 10.0
                delta_x = desired_x_min_cm - door_bbox_local.minPoint.x
                
                # 2. Y: base anta alla base carcassa
                desired_y_min_cm = cabinet_bbox.minPoint.y + (bottom_gap_mm / 10.0)
                delta_y = desired_y_min_cm - door_bbox_local.minPoint.y
                
                # 3. Z: faccia interna anta al fronte carcassa
                #    fronte = Z_max del fianco (es. -10 cm nei tuoi bbox)
                desired_z_min_cm = cabinet_bbox.maxPoint.z
                delta_z = desired_z_min_cm - door_bbox_local.minPoint.z
                
                self.logger.info(f"   🔧 Delta riallineamento:")
                self.logger.info(f"      ΔX = {delta_x:.3f} cm ({delta_x*10:.1f} mm)")
                self.logger.info(f"      ΔY = {delta_y:.3f} cm ({delta_y*10:.1f} mm)")
                self.logger.info(f"      ΔZ = {delta_z:.3f} cm ({delta_z*10:.1f} mm)")
                
                move_feats = door_comp.features.moveFeatures
                transform_move = adsk.core.Matrix3D.create()
                transform_move.translation = adsk.core.Vector3D.create(delta_x, delta_y, delta_z)
                
                bodies_to_move = adsk.core.ObjectCollection.create()
                bodies_to_move.add(door_body)
                move_input = move_feats.createInput(bodies_to_move, transform_move)
                move_feats.add(move_input)
                
                self.logger.info(f"   ✅ Anta riallineata via bounding box")
                
                door_bbox_final = door_body.boundingBox
                self.logger.info(f"   📦 Bbox anta (finale):")
                self.logger.info(f"      X: [{door_bbox_final.minPoint.x:.2f}, {door_bbox_final.maxPoint.x:.2f}] cm")
                self.logger.info(f"      Y: [{door_bbox_final.minPoint.y:.2f}, {door_bbox_final.maxPoint.y:.2f}] cm")
                self.logger.info(f"      Z: [{door_bbox_final.minPoint.z:.2f}, {door_bbox_final.maxPoint.z:.2f}] cm")
            else:
                # Fallback: posizionamento nominale se non troviamo la carcassa
                self.logger.warning("   ⚠️ Nessun bbox carcassa disponibile, uso posizionamento nominale")
                
                x_pos_cm = (x_offset_mm + side_gap_mm) / 10.0
                y_pos_cm = (cabinet_plinth_height + bottom_gap_mm) / 10.0
                z_pos_cm = (cabinet_depth) / 10.0 if cabinet_depth > 0 else 0
                
                delta_x = x_pos_cm - door_bbox_local.minPoint.x
                delta_y = y_pos_cm - door_bbox_local.minPoint.y
                delta_z = z_pos_cm - door_bbox_local.minPoint.z
                
                move_feats = door_comp.features.moveFeatures
                transform_move = adsk.core.Matrix3D.create()
                transform_move.translation = adsk.core.Vector3D.create(delta_x, delta_y, delta_z)
                
                bodies_to_move = adsk.core.ObjectCollection.create()
                bodies_to_move.add(door_body)
                move_input = move_feats.createInput(bodies_to_move, transform_move)
                move_feats.add(move_input)
                
        except Exception as e:
            self.logger.error(f"   ❌ Errore riallineamento anta: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
        
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
