"""
Geometry Builder for FurnitureAI
Simplified 3D cabinet box generation for AI-driven furniture creation
"""

import adsk.core
import adsk.fusion

class GeometryBuilder:
    """Builder for creating 3D cabinet geometry"""
    
    def __init__(self, design):
        """
        Initialize geometry builder
        
        Args:
            design: Fusion 360 design object
        """
        self.design = design
        self.root_comp = design.rootComponent
        self.app = adsk.core.Application.get()
    
    def create_simple_cabinet(self, params):
        """
        Create a simple cabinet box with panels
        
        Args:
            params: Cabinet parameters dict
                - width: Cabinet width (mm)
                - height: Cabinet height (mm)
                - depth: Cabinet depth (mm)
                - material_thickness: Panel thickness (mm)
                - has_back: Include back panel (bool)
                - back_thickness: Back panel thickness (mm)
                - name: Cabinet name (optional)
        
        Returns:
            adsk.fusion.Component: Created cabinet component
        """
        from .cabinet_generator import CabinetGenerator
        
        # Use existing CabinetGenerator for actual creation
        generator = CabinetGenerator(self.design)
        
        # Ensure all required parameters are present
        validated_params = self._validate_params(params)
        
        # Create cabinet using generator
        cabinet_comp = generator.create_cabinet(validated_params)
        
        return cabinet_comp
    
    def create_panel(self, sketch_plane, width, height, thickness):
        """
        Create a single rectangular panel
        
        Args:
            sketch_plane: Sketch plane for panel
            width: Panel width (cm)
            height: Panel height (cm)
            thickness: Panel thickness (cm)
        
        Returns:
            adsk.fusion.BRepBody: Panel body
        """
        # Create sketch
        sketches = self.root_comp.sketches
        sketch = sketches.add(sketch_plane)
        
        # Draw rectangle
        rect = sketch.sketchCurves.sketchLines.addTwoPointRectangle(
            adsk.core.Point3D.create(0, 0, 0),
            adsk.core.Point3D.create(width, height, 0)
        )
        
        # Extrude to create panel
        profile = sketch.profiles.item(0)
        extrudes = self.root_comp.features.extrudeFeatures
        
        distance = adsk.core.ValueInput.createByReal(thickness)
        extrude = extrudes.addSimple(
            profile,
            distance,
            adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        
        return extrude.bodies.item(0)
    
    def _validate_params(self, params):
        """Validate and set default parameters"""
        defaults = {
            'width': 800,
            'height': 720,
            'depth': 580,
            'material_thickness': 18,
            'has_back': True,
            'back_thickness': 3,
            'has_plinth': False,
            'plinth_height': 100,
            'shelves_count': 0,
            'divisions_count': 0
        }
        
        validated = defaults.copy()
        validated.update(params)
        
        # Ensure positive dimensions
        for key in ['width', 'height', 'depth', 'material_thickness', 'back_thickness']:
            if validated[key] <= 0:
                validated[key] = defaults[key]
        
        # Ensure non-negative counts
        for key in ['shelves_count', 'divisions_count']:
            if validated[key] < 0:
                validated[key] = 0
        
        return validated
    
    def create_panel_at(self, component, width, height, thickness, origin_x, origin_y, origin_z, name="Panel"):
        """
        Create a panel (box) at a specific position
        
        Args:
            component: Target component to create panel in
            width: Panel width in mm
            height: Panel height in mm
            thickness: Panel thickness in mm
            origin_x: X position in mm
            origin_y: Y position in mm
            origin_z: Z position in mm
            name: Name for the panel body
        
        Returns:
            adsk.fusion.BRepBody: Created panel body
        """
        try:
            sketches = component.sketches
            extrudes = component.features.extrudeFeatures
            move_feats = component.features.moveFeatures
            
            # Create sketch on XY plane
            xy_plane = component.xYConstructionPlane
            sketch = sketches.add(xy_plane)
            
            # Draw rectangle
            rect = sketch.sketchCurves.sketchLines.addTwoPointRectangle(
                adsk.core.Point3D.create(0, 0, 0),
                adsk.core.Point3D.create(width / 10.0, height / 10.0, 0)
            )
            
            # Extrude to create panel
            extrude_input = extrudes.createInput(
                sketch.profiles.item(0),
                adsk.fusion.FeatureOperations.NewBodyFeatureOperation
            )
            distance = adsk.core.ValueInput.createByReal(thickness / 10.0)
            extrude_input.setDistanceExtent(False, distance)
            extrude = extrudes.add(extrude_input)
            
            body = extrude.bodies.item(0)
            body.name = name
            
            # Move to specified position
            if origin_x != 0 or origin_y != 0 or origin_z != 0:
                transform = adsk.core.Matrix3D.create()
                transform.translation = adsk.core.Vector3D.create(
                    origin_x / 10.0,  # mm to cm
                    origin_y / 10.0,
                    origin_z / 10.0
                )
                
                bodies = adsk.core.ObjectCollection.create()
                bodies.add(body)
                move_input = move_feats.createInput(bodies, transform)
                move_feats.add(move_input)
            
            return body
        except Exception as e:
            self.app.log(f"Error creating panel at position: {e}")
            return None
    
    def create_box_from_dimensions(self, width, height, depth, thickness):
        """
        Create a simple box with given dimensions
        
        Args:
            width, height, depth: External dimensions in cm
            thickness: Panel thickness in cm
        
        Returns:
            list: List of created bodies
        """
        bodies = []
        
        # Convert to internal dimensions
        internal_width = width - 2 * thickness
        internal_height = height - 2 * thickness
        internal_depth = depth
        
        try:
            # Get XY plane for base
            xy_plane = self.root_comp.xYConstructionPlane
            
            # Left panel
            left_panel = self.create_panel(xy_plane, depth, height, thickness)
            if left_panel:
                bodies.append(left_panel)
            
            # Right panel
            # (Would need proper positioning - simplified for now)
            
            # Top and bottom
            # (Would need proper positioning - simplified for now)
            
        except Exception as e:
            self.app.log(f"Error creating box: {e}")
        
        return bodies
    
    def get_box_volume(self, width, height, depth):
        """
        Calculate box volume
        
        Args:
            width, height, depth: Dimensions in mm
        
        Returns:
            float: Volume in cubic cm
        """
        # Convert mm to cm
        w_cm = width / 10
        h_cm = height / 10
        d_cm = depth / 10
        
        return w_cm * h_cm * d_cm
    
    def get_panel_count(self, params):
        """
        Calculate number of panels needed
        
        Args:
            params: Cabinet parameters
        
        Returns:
            int: Number of panels
        """
        count = 4  # Left, right, top, bottom
        
        if params.get('has_back', True):
            count += 1
        
        count += params.get('shelves_count', 0)
        count += params.get('divisions_count', 0)
        
        return count
