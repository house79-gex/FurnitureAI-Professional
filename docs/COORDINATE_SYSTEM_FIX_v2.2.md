# Coordinate System Alignment - Version 2.2

## Overview

This document describes the coordinate system alignment completed in version 2.2 to ensure consistency across all modules of the FurnitureAI-Professional add-in for Fusion 360.

## Problem

The original implementation had inconsistencies between different modules:

- **CabinetGenerator** documentation claimed Y=depth, Z=height, but actual geometry had Y=height, Z=depth
- **DoorGenerator** used 90° rotation around X-axis assuming cabinet had Y=depth, Z=height
- **Plinth** was drawn on XY plane and extruded in Z, creating incorrect orientation
- These inconsistencies caused:
  - Doors positioned incorrectly or with thickness pointing inward
  - Plinth developing in wrong dimension (height instead of depth)
  - Misalignment between wizard parameters and actual geometry

## Solution

### Unified Coordinate System (aligned with Fusion 360)

All modules now use the same coordinate system:

```
Origin: (0, 0, 0) = Lower-left-back corner of cabinet
X-axis: Width    (0 = left side → width = right side)
Y-axis: Height   (0 = floor → height = top)
Z-axis: Depth    (0 = back → depth = front)
```

### Changes by Module

#### 1. CabinetGenerator (`cabinet_generator.py`)

**Documentation Updates:**
- Updated all docstrings to reflect Y=height, Z=depth
- Clarified that actual geometry was already correct

**Code Fixes:**
- `_create_side_panels`: Updated variable names (y_start not z_start) and comments
- `_create_top_bottom_panels`: Changed variable names from Z_bottom/Z_top to Y_bottom/Y_top
- `_create_back_panel`: Fixed coordinate mapping - back panel at Z=0+offset (not Y)
- `_create_plinth`: **Major rewrite**
  - Changed from XY plane to **XZ plane** (Y=0, floor level)
  - Draws rectangle in X×Z (width × depth)
  - Extrudes in **+Y direction** (upward) for plinth_height
  - Removed incorrect bbox realignment code
- `_create_shelves`: Updated Y/Z coordinate usage and comments
- `_create_divisions`: Updated Y/Z coordinate usage and comments

**Technical Details - Side Panels:**
```python
# Sketch on yZConstructionPlane (X=0 plane)
# Point(y_start, 0, 0) → Point(y_start+height, depth, 0)
# Maps to world: Y=plinth→height, Z=0→depth
# Extrusion in +X for thickness
```

**Technical Details - Plinth:**
```python
# Sketch on xZConstructionPlane (Y=0 plane, floor)
# Rectangle: (0,0) → (width, depth) in XZ
# Extrusion in +Y for plinth_height
# Result: X=0→width, Y=0→plinth_height, Z=0→depth
```

#### 2. DoorGenerator (`door_generator.py`)

**Major Changes:**
- Removed all debug `messageBox` popups
- Removed 90° rotation around X-axis (no longer needed!)
- Implemented **bounding box-based positioning**

**New Approach:**
1. Create door geometry on XY plane (X=width, Y=height, Z=thickness) at origin
2. Create component without initial transformation
3. Use bounding boxes to calculate correct position:
   - **X position**: x_offset + side_gap (from DoorDesigner)
   - **Y position**: Align door Y_min to cabinet Y_min (= plinth_height)
   - **Z position**: Align door Z_min to cabinet Z_max (= depth, front face)
4. Apply correction via `moveFeatures` to reposition door bodies

**Why This Works:**
- Door geometry created in correct orientation (no rotation needed!)
- Bbox alignment ensures precision regardless of parameter variations
- Thickness automatically extends in +Z (outward from cabinet front)

**Code Structure:**
```python
# 1. Create door component with identity transform
occurrence = target_comp.occurrences.addNewComponent(transform_identity)
door_comp = occurrence.component

# 2. Create geometry (already in correct orientation)
_create_flat_door(door_comp, width, height, thickness)

# 3. Calculate bbox-based alignment
cabinet_bbox = get_cabinet_reference_bbox()
door_bbox_local = door_body.boundingBox

# 4. Calculate deltas
delta_x = (x_offset + side_gap)/10 - door_bbox_local.minPoint.x
delta_y = cabinet_bbox.minPoint.y - door_bbox_local.minPoint.y  # Align bases
delta_z = cabinet_bbox.maxPoint.z - door_bbox_local.minPoint.z  # Front align

# 5. Apply moveFeatures
move_feats.add(move_input)  # Moves door bodies to correct position
```

#### 3. Wizard & FurnitureModel

**Verification:**
- Already correctly uses `furniture.zoccolo` for plinth configuration
- Correctly calculates `carcass_height = height - plinth_height`
- DoorDesigner passes `parent_component` in door configs
- All parameters flow correctly through the system

No changes needed - integration was already correct!

## Verification

### Expected Bounding Boxes

For a base cabinet 600mm wide × 720mm tall × 580mm deep, plinth 100mm, 1 door:

**Side Panel (Left):**
```
X: [0.0, 1.8] cm     (18mm thickness)
Y: [10.0, 72.0] cm   (100→720mm height, plinth to top)
Z: [0.0, 58.0] cm    (0→580mm depth, back to front)
```

**Plinth:**
```
X: [0.0, 60.0] cm    (0→600mm width)
Y: [0.0, 10.0] cm    (0→100mm height, floor to plinth top)
Z: [0.0, 58.0] cm    (0→580mm depth)
```

**Door:**
```
X: [0.15, 59.85] cm  (side gaps applied, ~600mm nominal)
Y: [10.0, 71.8] cm   (plinth→top-2mm, 100→718mm with top gap)
Z: [58.0, 59.8] cm   (front face at cabinet depth, 18mm thick extending outward)
```

### Testing Checklist

- [x] Side panels create correctly at Y=height, Z=depth
- [x] Plinth creates on floor (Y=0) extending upward to Y=plinth_height
- [x] Top/bottom panels positioned correctly in Y (height)
- [x] Back panel positioned at Z=0+offset (back/depth)
- [x] Shelves distributed correctly in Y (height)
- [x] Divisions span correctly in Y (height) and Z (depth)
- [x] Doors align to cabinet base in Y
- [x] Doors align to cabinet front in Z with thickness extending outward

## Benefits

1. **Consistency**: All modules use the same coordinate system
2. **Alignment with Fusion 360**: Matches Fusion's navigation cube orientation
3. **Precision**: Bbox-based positioning ensures correct alignment
4. **Maintainability**: Clear documentation prevents future confusion
5. **Extensibility**: New modules can follow the established system

## Migration Notes

### For Developers

If adding new geometry generation:

1. **Always** use the documented coordinate system (X=width, Y=height, Z=depth)
2. **Document** clearly in code which plane you're sketching on
3. **Use** bbox alignment when positioning relative to existing geometry
4. **Test** with different plinth heights to ensure Y coordinates are correct

### Breaking Changes

None - this is a fix to align actual behavior with expected behavior. Users should see improved alignment of doors and plinth.

## References

- CabinetGenerator: `fusion_addin/lib/core/cabinet_generator.py`
- DoorGenerator: `fusion_addin/lib/core/door_generator.py`
- Wizard: `fusion_addin/lib/commands/wizard_command.py`
- FurnitureModel: `fusion_addin/lib/core/furniture_model.py`

## Version History

- **v2.2.0**: Complete coordinate system alignment (this document)
- **v2.1.0**: Initial architectural separation of door/cabinet generation
- **v2.0.0**: Introduction of DoorDesigner pattern

---
*Last Updated: 2026-02-14*
*Author: house79-gex with GitHub Copilot assistance*
