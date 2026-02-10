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
                - back_mounting: Tipo montaggio retro ('flush_rabbet', 'groove', 'surface', default 'flush_rabbet')
                - rabbet_width: Larghezza battuta (mm, default 12)
                - rabbet_depth: Profondità battuta (mm, default = back_thickness)
                - groove_width: Larghezza canale (mm, default = back_thickness + 0.5)
                - groove_depth: Profondità canale (mm, default = back_thickness)
                - groove_offset_from_rear: Distanza canale dal retro (mm, default 10)
                - shelf_front_setback: Arretramento ripiani dal fronte (mm, default 3)
                - dowels_enabled: Abilita forature spinatura (bool, default False)
                - dowel_diameter: Diametro tasselli (mm, default 8)
                - dowel_edge_distance: Distanza tasselli dal bordo (mm, default 37)
                - dowel_spacing: Spaziatura tasselli (mm, default 32)
                - door_overlay_left: Sovrapposizione anta sinistra (mm, default 0)
                - door_overlay_right: Sovrapposizione anta destra (mm, default 0)
                - door_overlay_top: Sovrapposizione anta superiore (mm, default 0)
                - door_overlay_bottom: Sovrapposizione anta inferiore (mm, default 0)
                - door_gap: Gap tra ante (mm, default 2)
        
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
        
        # Nuovi parametri professionali
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
        
        # Crea i pannelli principali
        self._create_side_panels(cabinet_comp, width, height, depth, thickness, has_plinth, plinth_height)
        self._create_top_bottom_panels(cabinet_comp, width, depth, thickness, height, has_plinth, plinth_height)
        
        # Aggiungi pannello posteriore se richiesto
        if has_back:
            # Calcola inset retro basato sul tipo di montaggio
            retro_inset = self._calculate_retro_inset(back_mounting, groove_offset_from_rear, back_thickness)
            self._create_back_panel(cabinet_comp, width, height, depth, thickness, back_thickness, has_plinth, plinth_height, 
                                   back_mounting, rabbet_width, rabbet_depth, groove_width, groove_depth, 
                                   groove_offset_from_rear, retro_inset)
        
        # Aggiungi zoccolo se richiesto
        if has_plinth:
            self._create_plinth(cabinet_comp, width, depth, thickness, plinth_height)
        
        # Aggiungi ripiani
        if shelves_count > 0:
            retro_inset = self._calculate_retro_inset(back_mounting, groove_offset_from_rear, back_thickness) if has_back else 0
            self._create_shelves(cabinet_comp, width, depth, thickness, height, shelves_count, has_plinth, plinth_height,
                               shelf_front_setback, retro_inset)
        
        # Aggiungi divisori verticali
        if divisions_count > 0:
            self._create_divisions(cabinet_comp, width, height, depth, thickness, divisions_count, has_plinth, plinth_height)
        
        # Aggiungi forature spinatura se richieste
        if dowels_enabled:
            self._create_dowel_holes(cabinet_comp, width, height, depth, thickness, has_plinth, plinth_height,
                                    dowel_diameter, dowel_edge_distance, dowel_spacing)
        
        return cabinet_comp
    
    def _calculate_retro_inset(self, back_mounting, groove_offset_from_rear, back_thickness):
        """
        Calcola l'inset del retro in base al tipo di montaggio
        
        Args:
            back_mounting: Tipo montaggio ('flush_rabbet', 'groove', 'surface')
            groove_offset_from_rear: Offset canale dal retro (mm)
            back_thickness: Spessore pannello retro (mm)
            
        Returns:
            float: Inset retro in mm
        """
        if back_mounting == 'flush_rabbet':
            return 0  # Il retro è a filo
        elif back_mounting == 'groove':
            return groove_offset_from_rear  # Il retro arretra di quanto il canale è offset
        else:  # 'surface'
            return back_thickness  # Il retro è sovrapposto
    
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
            # Nuovi parametri professionali
            ('LarghezzaBattuta', params.get('rabbet_width', 12), 'mm'),
            ('ProfonditaBattuta', params.get('rabbet_depth', params.get('back_thickness', 3)), 'mm'),
            ('LarghezzaCanale', params.get('groove_width', params.get('back_thickness', 3) + 0.5), 'mm'),
            ('ProfonditaCanale', params.get('groove_depth', params.get('back_thickness', 3)), 'mm'),
            ('OffsetCanaleRetro', params.get('groove_offset_from_rear', 10), 'mm'),
            ('ArretamentoRipianiFronte', params.get('shelf_front_setback', 3), 'mm'),
            ('DiametroTassello', params.get('dowel_diameter', 8), 'mm'),
            ('DistanzaTasselloBordo', params.get('dowel_edge_distance', 37), 'mm'),
            ('SpaziaturaTasselli', params.get('dowel_spacing', 32), 'mm'),
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
        # Convert to cm for Fusion 360 internal units
        z_start = plinth_height / 10.0 if has_plinth else 0  # cm
        
        # Pannello sinistro
        sketch_left = sketches.add(yz_plane)
        rect_left = sketch_left.sketchCurves.sketchLines.addTwoPointRectangle(
            adsk.core.Point3D.create(0, z_start, 0),  # z_start is in cm
            adsk.core.Point3D.create(depth / 10.0, z_start + effective_height / 10.0, 0)  # All in cm
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
        """
        Crea i pannelli superiore e inferiore
        Ora modellati su piano YZ ed estrusi lungo X (larghezza interna)
        """
        sketches = component.sketches
        extrudes = component.features.extrudeFeatures
        move_feats = component.features.moveFeatures
        
        # Piano YZ per modellare i pannelli
        yz_plane = component.yZConstructionPlane
        
        # Calcola larghezza interna (W_in = width - 2*thickness)
        W_in = width - 2 * thickness
        
        # Calcola posizioni Z
        z_bottom = plinth_height if has_plinth else 0  # mm
        
        # PANNELLO INFERIORE (Fondo)
        # Profilo su YZ: rettangolo depth × thickness alla quota Z = plinth_height
        sketch_bottom = sketches.add(yz_plane)
        rect_bottom = sketch_bottom.sketchCurves.sketchLines.addTwoPointRectangle(
            adsk.core.Point3D.create(0, z_bottom / 10.0, 0),  # Converti mm in cm
            adsk.core.Point3D.create(depth / 10.0, (z_bottom + thickness) / 10.0, 0)
        )
        
        # Estrudi lungo X per la larghezza interna
        extrude_input_bottom = extrudes.createInput(
            sketch_bottom.profiles.item(0),
            adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        distance_bottom = adsk.core.ValueInput.createByReal(W_in / 10.0)
        extrude_input_bottom.setDistanceExtent(False, distance_bottom)
        extrude_bottom = extrudes.add(extrude_input_bottom)
        body_bottom = extrude_bottom.bodies.item(0)
        body_bottom.name = "Fondo"
        
        # Sposta il fondo a X = thickness (tra i fianchi)
        transform_bottom = adsk.core.Matrix3D.create()
        transform_bottom.translation = adsk.core.Vector3D.create(thickness / 10.0, 0, 0)
        bodies_bottom = adsk.core.ObjectCollection.create()
        bodies_bottom.add(body_bottom)
        move_input_bottom = move_feats.createInput(bodies_bottom, transform_bottom)
        move_feats.add(move_input_bottom)
        
        # PANNELLO SUPERIORE (Cielo)
        if height is not None:
            effective_height = height - plinth_height if has_plinth else height
            z_top = plinth_height + effective_height - thickness  # mm
            
            # Profilo su YZ: rettangolo depth × thickness alla quota Z = z_top
            sketch_top = sketches.add(yz_plane)
            rect_top = sketch_top.sketchCurves.sketchLines.addTwoPointRectangle(
                adsk.core.Point3D.create(0, z_top / 10.0, 0),
                adsk.core.Point3D.create(depth / 10.0, (z_top + thickness) / 10.0, 0)
            )
            
            # Estrudi lungo X per la larghezza interna
            extrude_input_top = extrudes.createInput(
                sketch_top.profiles.item(0),
                adsk.fusion.FeatureOperations.NewBodyFeatureOperation
            )
            distance_top = adsk.core.ValueInput.createByReal(W_in / 10.0)
            extrude_input_top.setDistanceExtent(False, distance_top)
            extrude_top = extrudes.add(extrude_input_top)
            body_top = extrude_top.bodies.item(0)
            body_top.name = "Cielo"
            
            # Sposta il cielo a X = thickness (tra i fianchi)
            transform_top = adsk.core.Matrix3D.create()
            transform_top.translation = adsk.core.Vector3D.create(thickness / 10.0, 0, 0)
            bodies_top = adsk.core.ObjectCollection.create()
            bodies_top.add(body_top)
            move_input_top = move_feats.createInput(bodies_top, transform_top)
            move_feats.add(move_input_top)
    
    def _create_back_panel(self, component, width, height, depth, thickness, back_thickness, has_plinth, plinth_height,
                          back_mounting='flush_rabbet', rabbet_width=12, rabbet_depth=None, 
                          groove_width=None, groove_depth=None, groove_offset_from_rear=10, retro_inset=0):
        """
        Crea il pannello posteriore con montaggio professionale
        Supporta battuta (flush_rabbet), canale (groove), o superficie (surface)
        
        Args:
            back_mounting: Tipo montaggio ('flush_rabbet', 'groove', 'surface')
            rabbet_width: Larghezza battuta (mm)
            rabbet_depth: Profondità battuta (mm)
            groove_width: Larghezza canale (mm)
            groove_depth: Profondità canale (mm)
            groove_offset_from_rear: Offset canale dal retro (mm)
            retro_inset: Inset retro calcolato (mm)
        """
        sketches = component.sketches
        extrudes = component.features.extrudeFeatures
        move_feats = component.features.moveFeatures
        
        # Valori default
        if rabbet_depth is None:
            rabbet_depth = back_thickness
        if groove_width is None:
            groove_width = back_thickness + 0.5
        if groove_depth is None:
            groove_depth = back_thickness
        
        # Piano YZ per pannello posteriore (come i fianchi)
        yz_plane = component.yZConstructionPlane
        
        # Calcola dimensioni pannello retro
        effective_height = height - plinth_height if has_plinth else height
        panel_width = width - 2 * thickness  # Larghezza tra i fianchi
        panel_height = effective_height - 2 * thickness  # Altezza tra fondo e cielo
        
        # Calcola posizione Z del retro
        z_offset = (plinth_height + thickness) if has_plinth else thickness  # mm
        
        # Calcola posizione Y del retro in base al tipo di montaggio
        if back_mounting == 'flush_rabbet':
            # Battuta: retro a filo con esterno carcassa, seduto nella battuta
            y_position = depth - back_thickness  # mm
        elif back_mounting == 'groove':
            # Canale: retro arretrato nel canale
            y_position = depth - groove_offset_from_rear - back_thickness  # mm
        else:  # 'surface'
            # Superficie: retro sovrapposto internamente
            y_position = depth - back_thickness  # mm
        
        # Crea profilo rettangolare su YZ
        sketch = sketches.add(yz_plane)
        rect = sketch.sketchCurves.sketchLines.addTwoPointRectangle(
            adsk.core.Point3D.create(y_position / 10.0, z_offset / 10.0, 0),
            adsk.core.Point3D.create((y_position + back_thickness) / 10.0, (z_offset + panel_height) / 10.0, 0)
        )
        
        # Estrudi lungo X per la larghezza tra i fianchi
        extrude_input = extrudes.createInput(
            sketch.profiles.item(0),
            adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        distance = adsk.core.ValueInput.createByReal(panel_width / 10.0)
        extrude_input.setDistanceExtent(False, distance)
        extrude_back = extrudes.add(extrude_input)
        body_back = extrude_back.bodies.item(0)
        body_back.name = "Retro"
        
        # Sposta a X = thickness (tra i fianchi)
        transform_back = adsk.core.Matrix3D.create()
        transform_back.translation = adsk.core.Vector3D.create(thickness / 10.0, 0, 0)
        bodies_back = adsk.core.ObjectCollection.create()
        bodies_back.add(body_back)
        move_input_back = move_feats.createInput(bodies_back, transform_back)
        move_feats.add(move_input_back)
        
        # Crea lavorazioni per montaggio (battuta o canale) sui fianchi
        if back_mounting == 'flush_rabbet':
            self._create_rabbet_cuts(component, width, height, depth, thickness, back_thickness, 
                                    has_plinth, plinth_height, rabbet_width, rabbet_depth)
        elif back_mounting == 'groove':
            self._create_groove_cuts(component, width, height, depth, thickness, back_thickness,
                                    has_plinth, plinth_height, groove_width, groove_depth, groove_offset_from_rear)
    
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
    
    def _create_shelves(self, component, width, depth, thickness, height, count, has_plinth, plinth_height,
                       shelf_front_setback=3, retro_inset=0):
        """
        Crea ripiani intermedi
        Ora modellati su piano YZ ed estrusi lungo X con profondità effettiva
        
        Args:
            shelf_front_setback: Arretramento dal fronte (mm)
            retro_inset: Arretramento dal retro per il pannello posteriore (mm)
        """
        sketches = component.sketches
        extrudes = component.features.extrudeFeatures
        move_feats = component.features.moveFeatures
        
        # Piano YZ per modellare i ripiani
        yz_plane = component.yZConstructionPlane
        
        # Calcola spaziatura ripiani
        effective_height = height - plinth_height if has_plinth else height
        usable_height = effective_height - 2 * thickness
        spacing = usable_height / (count + 1)
        
        # Calcola larghezza interna e profondità effettiva
        W_in = width - 2 * thickness
        shelf_depth_eff = depth - retro_inset - shelf_front_setback  # mm
        
        for i in range(count):
            z_position = (plinth_height if has_plinth else 0) + thickness + spacing * (i + 1)  # mm
            
            # Profilo su YZ: rettangolo shelf_depth_eff × thickness alla quota Z
            sketch = sketches.add(yz_plane)
            rect = sketch.sketchCurves.sketchLines.addTwoPointRectangle(
                adsk.core.Point3D.create(shelf_front_setback / 10.0, z_position / 10.0, 0),
                adsk.core.Point3D.create((shelf_front_setback + shelf_depth_eff) / 10.0, (z_position + thickness) / 10.0, 0)
            )
            
            # Estrudi lungo X per la larghezza interna
            extrude_input = extrudes.createInput(
                sketch.profiles.item(0),
                adsk.fusion.FeatureOperations.NewBodyFeatureOperation
            )
            distance = adsk.core.ValueInput.createByReal(W_in / 10.0)
            extrude_input.setDistanceExtent(False, distance)
            extrude_shelf = extrudes.add(extrude_input)
            body_shelf = extrude_shelf.bodies.item(0)
            body_shelf.name = f"Ripiano_{i+1}"
            
            # Sposta a X = thickness (tra i fianchi)
            transform_shelf = adsk.core.Matrix3D.create()
            transform_shelf.translation = adsk.core.Vector3D.create(thickness / 10.0, 0, 0)
            bodies_shelf = adsk.core.ObjectCollection.create()
            bodies_shelf.add(body_shelf)
            move_input_shelf = move_feats.createInput(bodies_shelf, transform_shelf)
            move_feats.add(move_input_shelf)
    
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
