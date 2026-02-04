"""
Profilo anta custom - Importazione da DXF
"""

import adsk.core
import adsk.fusion
import os

def create_custom_door(design, params):
    """
    Crea anta da profilo DXF personalizzato
    
    Args:
        design: adsk.fusion.Design
        params: Parametri con 'dxf_path'
    
    Returns:
        adsk.fusion.Component
    """
    width = params.get('width', 400)
    height = params.get('height', 700)
    thickness = params.get('thickness', 18)
    dxf_path = params.get('dxf_path')
    
    root_comp = design.rootComponent
    
    occurrence = root_comp.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    door_comp = occurrence.component
    door_comp.name = f"Anta_Custom_{int(width)}x{int(height)}"
    
    if dxf_path and os.path.exists(dxf_path):
        try:
            # Importa DXF
            import_manager = design.importManager
            dxf_options = import_manager.createDXF2DImportOptions(dxf_path, door_comp.xYConstructionPlane)
            import_manager.importToTarget(dxf_options, door_comp)
            
            # Estrudi il profilo importato
            if door_comp.sketches.count > 0:
                sketch = door_comp.sketches.item(0)
                if sketch.profiles.count > 0:
                    extrudes = door_comp.features.extrudeFeatures
                    extrude_input = extrudes.createInput(
                        sketch.profiles.item(0),
                        adsk.fusion.FeatureOperations.NewBodyFeatureOperation
                    )
                    
                    distance = adsk.core.ValueInput.createByReal(thickness / 10.0)
                    extrude_input.setDistanceExtent(False, distance)
                    
                    door_extrude = extrudes.add(extrude_input)
                    door_extrude.bodies.item(0).name = "Pannello_Custom"
        except:
            # Fallback: anta piatta
            from .profile_flat import create_flat_door
            return create_flat_door(design, params)
    else:
        # Nessun DXF: crea anta piatta di default
        from .profile_flat import create_flat_door
        return create_flat_door(design, params)
    
    return door_comp
