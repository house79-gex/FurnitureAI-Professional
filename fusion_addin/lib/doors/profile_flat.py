"""
Profilo anta piatta - Implementazione semplice e moderna
"""

import adsk.core
import adsk.fusion

def create_flat_door(design, params):
    """
    Crea anta piatta semplice
    
    Args:
        design: adsk.fusion.Design
        params: Parametri anta
    
    Returns:
        adsk.fusion.Component
    """
    width = params.get('width', 400)
    height = params.get('height', 700)
    thickness = params.get('thickness', 18)
    
    root_comp = design.rootComponent
    
    # Crea componente
    occurrence = root_comp.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    door_comp = occurrence.component
    door_comp.name = f"Anta_Piatta_{int(width)}x{int(height)}"
    
    # Crea sketch
    sketches = door_comp.sketches
    xy_plane = door_comp.xYConstructionPlane
    
    sketch = sketches.add(xy_plane)
    rect = sketch.sketchCurves.sketchLines.addTwoPointRectangle(
        adsk.core.Point3D.create(0, 0, 0),
        adsk.core.Point3D.create(width / 10.0, height / 10.0, 0)
    )
    
    # Estrudi
    extrudes = door_comp.features.extrudeFeatures
    extrude_input = extrudes.createInput(
        sketch.profiles.item(0),
        adsk.fusion.FeatureOperations.NewBodyFeatureOperation
    )
    
    distance = adsk.core.ValueInput.createByReal(thickness / 10.0)
    extrude_input.setDistanceExtent(False, distance)
    
    door_extrude = extrudes.add(extrude_input)
    door_extrude.bodies.item(0).name = "Pannello_Piatto"
    
    return door_comp
