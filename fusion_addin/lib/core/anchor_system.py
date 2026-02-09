"""
Anchor and Placement System for Multi-Cabinet Compositions
Enables positioning multiple cabinets relative to each other for kitchen/office layouts
"""

import adsk.core
import adsk.fusion
import json


class AnchorPoint:
    """
    Represents a connection point on a cabinet for positioning adjacent cabinets
    """
    
    def __init__(self, face_type, position, cabinet_dimensions):
        """
        Initialize an anchor point
        
        Args:
            face_type: Type of face ('left_face', 'right_face', 'top_face', 'bottom_face', 'back_face', 'front_face')
            position: 3D position tuple (x, y, z) in mm from cabinet origin
            cabinet_dimensions: Dict with 'width', 'height', 'depth' in mm
        """
        self.face_type = face_type
        self.position = position  # (x, y, z) in mm
        self.cabinet_dimensions = cabinet_dimensions
    
    def to_dict(self):
        """Convert to dictionary for serialization"""
        return {
            'face_type': self.face_type,
            'position': self.position,
            'cabinet_dimensions': self.cabinet_dimensions
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create from dictionary"""
        return cls(
            data['face_type'],
            tuple(data['position']),
            data['cabinet_dimensions']
        )


class CabinetPlacer:
    """
    Handles placement of cabinets relative to existing cabinets using anchor points
    """
    
    def __init__(self, design):
        """
        Initialize cabinet placer
        
        Args:
            design: Fusion 360 design object
        """
        self.design = design
        self.root_comp = design.rootComponent
    
    def place_adjacent_right(self, existing_component, new_cabinet_generator, new_cabinet_params, gap=0):
        """
        Place a new cabinet to the right of an existing cabinet
        
        Args:
            existing_component: Existing cabinet component
            new_cabinet_generator: CabinetGenerator instance
            new_cabinet_params: Parameters dict for new cabinet
            gap: Gap between cabinets in mm (default 0)
        
        Returns:
            adsk.fusion.Component: New cabinet component
        """
        # Get anchor points from existing cabinet
        anchors = self.get_anchor_points(existing_component)
        right_anchor = anchors.get('right_face')
        
        if not right_anchor:
            raise ValueError("Existing cabinet has no right anchor point")
        
        # Create new cabinet
        new_cabinet = new_cabinet_generator.create_cabinet(new_cabinet_params)
        
        # Calculate X offset: position at right side of existing cabinet + gap
        x_offset = right_anchor.position[0] + gap
        
        # Find the occurrence of the new cabinet and move it
        for occ in self.root_comp.allOccurrences:
            if occ.component == new_cabinet:
                transform = adsk.core.Matrix3D.create()
                transform.translation = adsk.core.Vector3D.create(
                    x_offset / 10.0,  # mm to cm
                    0,
                    0
                )
                occ.transform = transform
                break
        
        # Store anchor metadata on new cabinet
        self._store_anchor_metadata(new_cabinet, new_cabinet_params)
        
        return new_cabinet
    
    def place_adjacent_left(self, existing_component, new_cabinet_generator, new_cabinet_params, gap=0):
        """
        Place a new cabinet to the left of an existing cabinet
        
        Args:
            existing_component: Existing cabinet component
            new_cabinet_generator: CabinetGenerator instance
            new_cabinet_params: Parameters dict for new cabinet
            gap: Gap between cabinets in mm (default 0)
        
        Returns:
            adsk.fusion.Component: New cabinet component
        """
        # Get anchor points from existing cabinet
        anchors = self.get_anchor_points(existing_component)
        left_anchor = anchors.get('left_face')
        
        if not left_anchor:
            raise ValueError("Existing cabinet has no left anchor point")
        
        # Create new cabinet
        new_cabinet = new_cabinet_generator.create_cabinet(new_cabinet_params)
        
        # Calculate X offset: position new cabinet's right side at existing cabinet's left side - gap
        new_width = new_cabinet_params.get('width', 800)
        x_offset = left_anchor.position[0] - new_width - gap
        
        # Find the occurrence of the new cabinet and move it
        for occ in self.root_comp.allOccurrences:
            if occ.component == new_cabinet:
                transform = adsk.core.Matrix3D.create()
                transform.translation = adsk.core.Vector3D.create(
                    x_offset / 10.0,  # mm to cm
                    0,
                    0
                )
                occ.transform = transform
                break
        
        # Store anchor metadata on new cabinet
        self._store_anchor_metadata(new_cabinet, new_cabinet_params)
        
        return new_cabinet
    
    def place_on_top(self, existing_component, new_cabinet_generator, new_cabinet_params):
        """
        Place a new cabinet on top of an existing cabinet (e.g., wall unit above base)
        
        Args:
            existing_component: Existing cabinet component
            new_cabinet_generator: CabinetGenerator instance
            new_cabinet_params: Parameters dict for new cabinet
        
        Returns:
            adsk.fusion.Component: New cabinet component
        """
        # Get anchor points from existing cabinet
        anchors = self.get_anchor_points(existing_component)
        top_anchor = anchors.get('top_face')
        
        if not top_anchor:
            raise ValueError("Existing cabinet has no top anchor point")
        
        # Create new cabinet
        new_cabinet = new_cabinet_generator.create_cabinet(new_cabinet_params)
        
        # Calculate Z offset: position at top of existing cabinet
        z_offset = top_anchor.position[2]
        
        # Find the occurrence of the new cabinet and move it
        for occ in self.root_comp.allOccurrences:
            if occ.component == new_cabinet:
                transform = adsk.core.Matrix3D.create()
                transform.translation = adsk.core.Vector3D.create(
                    0,
                    0,
                    z_offset / 10.0  # mm to cm
                )
                occ.transform = transform
                break
        
        # Store anchor metadata on new cabinet
        self._store_anchor_metadata(new_cabinet, new_cabinet_params)
        
        return new_cabinet
    
    def get_anchor_points(self, component):
        """
        Get anchor points for a cabinet component
        
        Args:
            component: Cabinet component
        
        Returns:
            dict: Dictionary of anchor points by face type
        """
        # Try to read from component attributes first
        try:
            attrs = component.attributes
            anchors_group = attrs.itemByName('FurnitureAI', 'anchors')
            if anchors_group:
                anchors_data = json.loads(anchors_group.value)
                return {
                    face_type: AnchorPoint.from_dict(data)
                    for face_type, data in anchors_data.items()
                }
        except Exception:
            # Attribute not found or parse error, will calculate from dimensions
            pass
        
        # If not found in attributes, calculate from component dimensions
        # Read dimensions from component attributes
        try:
            dims_attr = component.attributes.itemByName('FurnitureAI', 'model')
            if dims_attr:
                model_data = json.loads(dims_attr.value)
                dimensions = model_data.get('dimensioni', {})
                width = dimensions.get('larghezza', 800)
                height = dimensions.get('altezza', 720)
                depth = dimensions.get('profondita', 580)
            else:
                # Use bounding box as fallback
                bbox = component.bRepBodies.item(0).boundingBox if component.bRepBodies.count > 0 else None
                if bbox:
                    width = (bbox.maxPoint.x - bbox.minPoint.x) * 10  # cm to mm
                    height = (bbox.maxPoint.z - bbox.minPoint.z) * 10
                    depth = (bbox.maxPoint.y - bbox.minPoint.y) * 10
                else:
                    # Default dimensions
                    width = 800
                    height = 720
                    depth = 580
        except Exception:
            # Error reading dimensions, use defaults
            width = 800
            height = 720
            depth = 580
        
        cabinet_dims = {
            'width': width,
            'height': height,
            'depth': depth
        }
        
        # Create anchor points at key positions
        anchors = {
            'left_face': AnchorPoint('left_face', (0, depth/2, height/2), cabinet_dims),
            'right_face': AnchorPoint('right_face', (width, depth/2, height/2), cabinet_dims),
            'top_face': AnchorPoint('top_face', (width/2, depth/2, height), cabinet_dims),
            'bottom_face': AnchorPoint('bottom_face', (width/2, depth/2, 0), cabinet_dims),
            'back_face': AnchorPoint('back_face', (width/2, 0, height/2), cabinet_dims),
            'front_face': AnchorPoint('front_face', (width/2, depth, height/2), cabinet_dims)
        }
        
        return anchors
    
    def _store_anchor_metadata(self, component, cabinet_params):
        """
        Store anchor point metadata as component attributes
        
        Args:
            component: Cabinet component
            cabinet_params: Cabinet parameters dict
        """
        try:
            width = cabinet_params.get('width', 800)
            height = cabinet_params.get('height', 720)
            depth = cabinet_params.get('depth', 580)
            
            cabinet_dims = {
                'width': width,
                'height': height,
                'depth': depth
            }
            
            # Create anchor points
            anchors = {
                'left_face': AnchorPoint('left_face', (0, depth/2, height/2), cabinet_dims),
                'right_face': AnchorPoint('right_face', (width, depth/2, height/2), cabinet_dims),
                'top_face': AnchorPoint('top_face', (width/2, depth/2, height), cabinet_dims),
                'bottom_face': AnchorPoint('bottom_face', (width/2, depth/2, 0), cabinet_dims),
                'back_face': AnchorPoint('back_face', (width/2, 0, height/2), cabinet_dims),
                'front_face': AnchorPoint('front_face', (width/2, depth, height/2), cabinet_dims)
            }
            
            # Serialize to JSON
            anchors_data = {
                face_type: anchor.to_dict()
                for face_type, anchor in anchors.items()
            }
            anchors_json = json.dumps(anchors_data)
            
            # Store as attribute
            component.attributes.add('FurnitureAI', 'anchors', anchors_json)
        except Exception:
            # Failed to store anchor metadata, continue without it
            # This is not critical for cabinet functionality
            pass


# Convenience functions for common placement scenarios

def snap_cabinets_horizontal(design, cabinets_list, gap=0):
    """
    Snap multiple cabinets horizontally in a row
    
    Args:
        design: Fusion 360 design object
        cabinets_list: List of cabinet components to snap together
        gap: Gap between cabinets in mm (default 0)
    
    Returns:
        list: List of positioned cabinet components
    """
    if len(cabinets_list) < 2:
        return cabinets_list
    
    placer = CabinetPlacer(design)
    
    # First cabinet stays in place
    # Position subsequent cabinets to the right of previous one
    for i in range(1, len(cabinets_list)):
        prev_cabinet = cabinets_list[i - 1]
        current_cabinet = cabinets_list[i]
        
        # Get right anchor of previous cabinet
        anchors = placer.get_anchor_points(prev_cabinet)
        right_anchor = anchors.get('right_face')
        
        if right_anchor:
            # Calculate X offset
            x_offset = right_anchor.position[0] + gap
            
            # Find occurrence and move it
            for occ in design.rootComponent.allOccurrences:
                if occ.component == current_cabinet:
                    transform = adsk.core.Matrix3D.create()
                    transform.translation = adsk.core.Vector3D.create(
                        x_offset / 10.0,  # mm to cm
                        0,
                        0
                    )
                    occ.transform = transform
                    break
    
    return cabinets_list
