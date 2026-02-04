"""
Profilo anta shaker - Telaio con pannello centrale incassato
"""

import adsk.core
import adsk.fusion

def create_shaker_door(design, params):
    """
    Crea anta stile shaker (telaio + pannello)
    
    Args:
        design: adsk.fusion.Design
        params: Parametri
    
    Returns:
        adsk.fusion.Component
    """
    width = params.get('width', 400)
    height = params.get('height', 700)
    thickness = params.get('thickness', 18)
    frame_width = params.get('frame_width', 60)  # Larghezza telaio
    panel_recess = params.get('panel_recess', 4)  # Ribassamento pannello
    
    root_comp = design.rootComponent
    
    occurrence = root_comp.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    door_comp = occurrence.component
    door_comp.name = f"Anta_Shaker_{int(width)}x{int(height)}"
    
    sketches = door_comp.sketches
    extrudes = door_comp.features.extrudeFeatures
    xy_plane = door_comp.xYConstructionPlane
    
    # Telaio (profilo a cornice)
    sketch_frame = sketches.add(xy_plane)
    lines = sketch_frame.sketchCurves.sketchLines
    
    # Esterno
    lines.addTwoPointRectangle(
        adsk.core.Point3D.create(0, 0, 0),
        adsk.core.Point3D.create(width / 10.0, height / 10.0, 0)
    )
    
    # Interno (vuoto)
    inner_offset = frame_width / 10.0
    lines.addTwoPointRectangle(
        adsk.core.Point3D.create(inner_offset, inner_offset, 0),
        adsk.core.Point3D.create((width - frame_width) / 10.0, (height - frame_width) / 10.0, 0)
    )
    
    # Estrudi telaio
    extrude_input_frame = extrudes.createInput(
        sketch_frame.profiles.item(0),
        adsk.fusion.FeatureOperations.NewBodyFeatureOperation
    )
    distance_frame = adsk.core.ValueInput.createByReal(thickness / 10.0)
    extrude_input_frame.setDistanceExtent(False, distance_frame)
    frame_extrude = extrudes.add(extrude_input_frame)
    frame_extrude.bodies.item(0).name = "Telaio"
    
    # Pannello centrale incassato
    sketch_panel = sketches.add(xy_plane)
    panel_margin = (frame_width + 5) / 10.0
    
    sketch_panel.sketchCurves.sketchLines.addTwoPointRectangle(
        adsk.core.Point3D.create(panel_margin, panel_margin, 0),
        adsk.core.Point3D.create((width - frame_width - 5) / 10.0, (height - frame_width - 5) / 10.0, 0)
    )
    
    panel_thickness = thickness - panel_recess
    extrude_input_panel = extrudes.createInput(
        sketch_panel.profiles.item(0),
        adsk.fusion.FeatureOperations.NewBodyFeatureOperation
    )
    distance_panel = adsk.core.ValueInput.createByReal(panel_thickness / 10.0)
    extrude_input_panel.setDistanceExtent(False, distance_panel)
    panel_extrude = extrudes.add(extrude_input_panel)
    panel_extrude.bodies.item(0).name = "Pannello_Centrale"
    
    return door_comp
