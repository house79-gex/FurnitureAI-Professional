"""
Profilo anta con vetro - Telaio legno + inserto vetro
"""

import adsk.core
import adsk.fusion

def create_glass_door(design, params):
    """
    Crea anta con inserto vetro
    
    Args:
        design: adsk.fusion.Design
        params: Parametri
    
    Returns:
        adsk.fusion.Component
    """
    width = params.get('width', 400)
    height = params.get('height', 700)
    thickness = params.get('thickness', 18)
    frame_width = params.get('frame_width', 50)
    glass_thickness = params.get('glass_thickness', 4)
    
    root_comp = design.rootComponent
    
    occurrence = root_comp.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    door_comp = occurrence.component
    door_comp.name = f"Anta_Vetro_{int(width)}x{int(height)}"
    
    sketches = door_comp.sketches
    extrudes = door_comp.features.extrudeFeatures
    xy_plane = door_comp.xYConstructionPlane
    
    # Telaio legno
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
    
    extrude_frame = extrudes.createInput(
        sketch_frame.profiles.item(0),
        adsk.fusion.FeatureOperations.NewBodyFeatureOperation
    )
    distance_frame = adsk.core.ValueInput.createByReal(thickness / 10.0)
    extrude_frame.setDistanceExtent(False, distance_frame)
    frame_body = extrudes.add(extrude_frame)
    frame_body.bodies.item(0).name = "Telaio_Legno"
    
    # Inserto vetro (al centro del telaio)
    sketch_glass = sketches.add(xy_plane)
    glass_margin = (frame_width + 2) / 10.0
    
    sketch_glass.sketchCurves.sketchLines.addTwoPointRectangle(
        adsk.core.Point3D.create(glass_margin, glass_margin, 0),
        adsk.core.Point3D.create((width - frame_width - 2) / 10.0, (height - frame_width - 2) / 10.0, 0)
    )
    
    # Posiziona vetro al centro dello spessore
    glass_offset = (thickness - glass_thickness) / 2.0
    
    extrude_glass = extrudes.createInput(
        sketch_glass.profiles.item(0),
        adsk.fusion.FeatureOperations.NewBodyFeatureOperation
    )
    distance_glass = adsk.core.ValueInput.createByReal(glass_thickness / 10.0)
    extrude_glass.setDistanceExtent(False, distance_glass)
    glass_body = extrudes.add(extrude_glass)
    glass_body.bodies.item(0).name = "Vetro"
    
    # Applica aspetto vetro trasparente (se disponibile)
    try:
        appearance_lib = design.appearances
        glass_appearance = appearance_lib.itemByName("Glass")
        if glass_appearance:
            glass_body.bodies.item(0).appearance = glass_appearance
    except:
        pass
    
    return door_comp
