"""
Scassi per pannelli posteriori e schienali
Crea scanalature per l'inserimento di pannelli sottili
"""

import adsk.core
import adsk.fusion

class Grooves:
    """Generatore di scassi e scanalature"""
    
    def __init__(self, component):
        """
        Inizializza il generatore
        
        Args:
            component: Componente Fusion
        """
        self.component = component
        self.default_groove_width = 4.0   # Larghezza scasso (mm)
        self.default_groove_depth = 10.0  # Profondità scasso (mm)
    
    def add_back_panel_grooves(self, cabinet_bodies, params):
        """
        Aggiunge scassi per pannello posteriore
        
        Args:
            cabinet_bodies: Lista di BRepBody (fianchi, cielo, fondo)
            params: Dizionario parametri
                - panel_thickness: Spessore pannello retro (mm, default 3)
                - groove_depth: Profondità scasso (mm, default 10)
                - offset_from_back: Distanza dal retro (mm, default 10)
        
        Returns:
            list: Lista di feature scassi create
        """
        panel_thickness = params.get('panel_thickness', 3)
        groove_depth = params.get('groove_depth', 10)
        offset_from_back = params.get('offset_from_back', 10)
        
        # Larghezza scasso = spessore pannello + tolleranza
        groove_width = panel_thickness + 0.5
        
        grooves = []
        
        for body in cabinet_bodies:
            # Determina su quale faccia creare lo scasso
            # (semplificazione: scasso su faccia interna)
            groove = self._create_groove_on_body(
                body,
                groove_width,
                groove_depth,
                offset_from_back
            )
            
            if groove:
                grooves.append(groove)
        
        return grooves
    
    def add_shelf_grooves(self, body, params):
        """
        Aggiunge scassi per ripiani (alternativa ai fori).
        
        Gli scassi orizzontali permettono l'inserimento di ripiani
        a diverse altezze Y.
        
        Args:
            body: BRepBody su cui creare scassi
            params: Dizionario parametri
                - positions: Lista di posizioni Y (altezza in mm)
                - groove_width: Larghezza scasso (mm)
                - groove_depth: Profondità scasso (mm)
        
        Returns:
            list: Lista di feature scassi
        """
        positions = params.get('positions', [])
        groove_width = params.get('groove_width', self.default_groove_width)
        groove_depth = params.get('groove_depth', self.default_groove_depth)
        
        grooves = []
        
        for y_pos in positions:
            groove = self._create_horizontal_groove(
                body,
                y_pos,
                groove_width,
                groove_depth
            )
            
            if groove:
                grooves.append(groove)
        
        return grooves
    
    def add_drawer_bottom_groove(self, drawer_bodies, params):
        """
        Aggiunge scasso per fondo cassetto
        
        Args:
            drawer_bodies: Lista di corpi cassetto (fianchi, fronte, retro)
            params: Dizionario parametri
                - bottom_thickness: Spessore fondo (mm, default 3)
                - groove_height: Altezza scasso da base (mm, default 10)
                - groove_depth: Profondità scasso (mm, default 8)
        
        Returns:
            list: Lista di scassi
        """
        bottom_thickness = params.get('bottom_thickness', 3)
        groove_height = params.get('groove_height', 10)
        groove_depth = params.get('groove_depth', 8)
        
        groove_width = bottom_thickness + 0.5
        
        grooves = []
        
        for body in drawer_bodies:
            groove = self._create_drawer_groove(
                body,
                groove_width,
                groove_depth,
                groove_height
            )
            
            if groove:
                grooves.append(groove)
        
        return grooves
    
    def _create_groove_on_body(self, body, width, depth, offset):
        """
        Crea uno scasso su un corpo
        
        Args:
            body: BRepBody
            width: Larghezza scasso (mm)
            depth: Profondità scasso (mm)
            offset: Offset dalla faccia (mm)
        
        Returns:
            Feature o None
        """
        try:
            # Ottieni bbox per determinare dimensioni
            bbox = body.boundingBox
            body_depth = (bbox.maxPoint.y - bbox.minPoint.y) * 10  # cm to mm
            body_height = (bbox.maxPoint.z - bbox.minPoint.z) * 10
            
            # Crea sketch su faccia interna
            sketches = self.component.sketches
            yz_plane = self.component.yZConstructionPlane
            
            sketch = sketches.add(yz_plane)
            lines = sketch.sketchCurves.sketchLines
            
            # Rettangolo scasso
            x1 = (body_depth - offset - depth) / 10.0
            x2 = (body_depth - offset) / 10.0
            y1 = 0
            y2 = body_height / 10.0
            
            p1 = adsk.core.Point3D.create(x1, y1, 0)
            p2 = adsk.core.Point3D.create(x2, y1, 0)
            p3 = adsk.core.Point3D.create(x2, y2, 0)
            p4 = adsk.core.Point3D.create(x1, y2, 0)
            
            lines.addByTwoPoints(p1, p2)
            lines.addByTwoPoints(p2, p3)
            lines.addByTwoPoints(p3, p4)
            lines.addByTwoPoints(p4, p1)
            
            # Estrudi come taglio
            extrudes = self.component.features.extrudeFeatures
            
            extrude_input = extrudes.createInput(
                sketch.profiles.item(0),
                adsk.fusion.FeatureOperations.CutFeatureOperation
            )
            
            distance = adsk.core.ValueInput.createByReal(width / 10.0)
            extrude_input.setDistanceExtent(False, distance)
            
            groove_feature = extrudes.add(extrude_input)
            return groove_feature
        except:
            return None
    
    def _create_horizontal_groove(self, body, y_position, width, depth):
        """
        Crea uno scasso orizzontale (per ripiani).
        
        SISTEMA COORDINATE (allineato con Fusion 360):
        - X = larghezza
        - Y = altezza
        - Z = profondità
        
        Gli scassi orizzontali sono tipicamente per ripiani e si sviluppano
        nel piano XZ (orizzontale) a una certa altezza Y.
        
        Args:
            body: BRepBody
            y_position: Posizione Y (altezza) dello scasso (mm)
            width: Larghezza scasso (mm)
            depth: Profondità scasso (mm)
        
        Returns:
            Feature o None
        """
        try:
            sketches = self.component.sketches
            xz_plane = self.component.xZConstructionPlane
            
            # Crea piano offset alla posizione Y (altezza)
            planes = self.component.constructionPlanes
            plane_input = planes.createInput()
            
            offset_value = adsk.core.ValueInput.createByReal(y_position / 10.0)
            plane_input.setByOffset(xz_plane, offset_value)
            
            offset_plane = planes.add(plane_input)
            
            # Crea sketch su piano offset
            sketch = sketches.add(offset_plane)
            
            # Ottieni dimensioni corpo
            bbox = body.boundingBox
            body_width = (bbox.maxPoint.x - bbox.minPoint.x) * 10
            body_depth = (bbox.maxPoint.z - bbox.minPoint.z) * 10  # Profondità lungo Z
            
            # Rettangolo scasso (lungo tutta la profondità)
            lines = sketch.sketchCurves.sketchLines
            
            half_width = width / 2.0
            
            p1 = adsk.core.Point3D.create(0, -half_width / 10.0, 0)
            p2 = adsk.core.Point3D.create(body_depth / 10.0, -half_width / 10.0, 0)
            p3 = adsk.core.Point3D.create(body_depth / 10.0, half_width / 10.0, 0)
            p4 = adsk.core.Point3D.create(0, half_width / 10.0, 0)
            
            lines.addByTwoPoints(p1, p2)
            lines.addByTwoPoints(p2, p3)
            lines.addByTwoPoints(p3, p4)
            lines.addByTwoPoints(p4, p1)
            
            # Estrudi come taglio
            extrudes = self.component.features.extrudeFeatures
            
            extrude_input = extrudes.createInput(
                sketch.profiles.item(0),
                adsk.fusion.FeatureOperations.CutFeatureOperation
            )
            
            distance = adsk.core.ValueInput.createByReal(depth / 10.0)
            extrude_input.setDistanceExtent(False, distance)
            
            groove_feature = extrudes.add(extrude_input)
            return groove_feature
        except:
            return None
    
    def _create_drawer_groove(self, body, width, depth, height_from_base):
        """
        Crea scasso per fondo cassetto
        
        Args:
            body: BRepBody (fianco o fronte cassetto)
            width: Larghezza scasso (mm)
            depth: Profondità scasso (mm)
            height_from_base: Altezza dal fondo (mm)
        
        Returns:
            Feature o None
        """
        # Simile a horizontal groove ma ad altezza specifica
        return self._create_horizontal_groove(body, height_from_base, width, depth)
    
    def create_custom_groove(self, body, profile_points, extrude_distance):
        """
        Crea uno scasso con profilo personalizzato
        
        Args:
            body: BRepBody
            profile_points: Lista di Point3D per il profilo
            extrude_distance: Distanza di estrusione (mm)
        
        Returns:
            Feature o None
        """
        try:
            sketches = self.component.sketches
            xy_plane = self.component.xYConstructionPlane
            
            sketch = sketches.add(xy_plane)
            lines = sketch.sketchCurves.sketchLines
            
            # Crea profilo da punti
            for i in range(len(profile_points) - 1):
                lines.addByTwoPoints(profile_points[i], profile_points[i + 1])
            
            # Chiudi profilo
            lines.addByTwoPoints(profile_points[-1], profile_points[0])
            
            # Estrudi come taglio
            extrudes = self.component.features.extrudeFeatures
            
            extrude_input = extrudes.createInput(
                sketch.profiles.item(0),
                adsk.fusion.FeatureOperations.CutFeatureOperation
            )
            
            distance = adsk.core.ValueInput.createByReal(extrude_distance / 10.0)
            extrude_input.setDistanceExtent(False, distance)
            
            groove_feature = extrudes.add(extrude_input)
            return groove_feature
        except:
            return None
