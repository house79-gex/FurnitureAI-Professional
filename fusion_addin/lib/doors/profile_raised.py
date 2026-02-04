"""
Profilo anta boiserie - Pannello rialzato con loft
"""

import adsk.core
import adsk.fusion

def create_raised_door(design, params):
    """
    Crea anta con pannello rialzato (raised panel)
    
    Args:
        design: adsk.fusion.Design
        params: Parametri
    
    Returns:
        adsk.fusion.Component
    """
    width = params.get('width', 400)
    height = params.get('height', 700)
    thickness = params.get('thickness', 22)  # Più spessa per raised panel
    frame_width = params.get('frame_width', 70)
    
    root_comp = design.rootComponent
    
    occurrence = root_comp.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    door_comp = occurrence.component
    door_comp.name = f"Anta_Raised_{int(width)}x{int(height)}"
    
    # Implementazione semplificata - telaio + pannello rialzato
    # (versione completa richiederebbe loft complesso)
    
    sketches = door_comp.sketches
    extrudes = door_comp.features.extrudeFeatures
    xy_plane = door_comp.xYConstructionPlane
    
    # Telaio base
    sketch_frame = sketches.add(xy_plane)
    lines = sketch_frame.sketchCurves.sketchLines
    
    lines.addTwoPointRectangle(
        adsk.core.Point3D.create(0, 0, 0),
        adsk.core.Point3D.create(width / 10.0, height / 10.0, 0)
    )
    
    inner_offset = frame_width / 10.0
    lines.addTwoPointRectangle(
        adsk.core.Point3D.create(inner_offset, inner_offset, 0),
        adsk.core.Point3D.create((width - frame_width) / 10.0, (height - frame_width) / 10.0, 0)
    )
    
    extrude_input = extrudes.createInput(
        sketch_frame.profiles.item(0),
        adsk.fusion.FeatureOperations.NewBodyFeatureOperation
    )
    distance = adsk.core.ValueInput.createByReal(thickness / 10.0)
    extrude_input.setDistanceExtent(False, distance)
    frame_extrude = extrudes.add(extrude_input)
    frame_extrude.bodies.item(0).name = "Telaio_Raised"
    
    # Pannello centrale rialzato (semplificato come cilindro)
    sketch_raised = sketches.add(xy_plane)
    margin = (frame_width + 10) / 10.0
    
    sketch_raised.sketchCurves.sketchLines.addTwoPointRectangle(
        adsk.core.Point3D.create(margin, margin, 0),
        adsk.core.Point3D.create((width - frame_width - 10) / 10.0, (height - frame_width - 10) / 10.0, 0)
    )
    
    raised_height = thickness + 4  # Rialzo di 4mm
    extrude_raised = extrudes.createInput(
        sketch_raised.profiles.item(0),
        adsk.fusion.FeatureOperations.NewBodyFeatureOperation
    )
    distance_raised = adsk.core.ValueInput.createByReal(raised_height / 10.0)
    extrude_raised.setDistanceExtent(False, distance_raised)
    raised_extrude = extrudes.add(extrude_raised)
    raised_extrude.bodies.item(0).name = "Pannello_Rialzato"
    
    return door_comp
