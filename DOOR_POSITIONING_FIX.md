# Door Positioning and Dimensions Fix

## Problem Statement

The FurnitureAI-Professional add-in had three main issues with door (ante) generation:

1. **Coordinate System Mismatch**: Cabinet and door generators used inconsistent coordinate systems
   - Cabinet: X=width, Y=depth, Z=height
   - Door (as created): X=width, Y=height, Z=thickness
   - Result: Doors appeared misaligned in Z relative to cabinet carcass

2. **Incorrect Door Dimensions**: `FurniturePiece.calculate_door_dimensions()` was adding panel thickness and overlays, causing oversized doors (e.g., 634×636mm instead of ~600×620mm for a 600mm cabinet)

3. **Wrong Plinth Source**: Wizard was reading plinth height from `furniture.ferramenta['piedini']` instead of `furniture.zoccolo`, causing misalignment

## Solution Implemented

### 1. Coordinate System Alignment (door_generator.py)

**Problem**: Door geometry created on XY plane (X=width, Y=height, Z=thickness) didn't match cabinet system (X=width, Y=depth, Z=height).

**Solution**: Apply 90° rotation around X-axis during door placement:
```python
transform = adsk.core.Matrix3D.create()
rotation_axis = adsk.core.Vector3D.create(1, 0, 0)  # X-axis
rotation_angle = math.pi / 2.0  # 90 degrees
transform.setToRotation(rotation_angle, rotation_axis, adsk.core.Point3D.create(0, 0, 0))
```

**Effect of Rotation**:
- X_door → X_cabinet (width, unchanged)
- Y_door → Z_cabinet (height aligned)
- Z_door → -Y_cabinet (thickness extends from front outward)

**Positioning After Rotation**:
```python
x_position_cm = (x_offset_mm + side_gap_mm) / 10.0
y_position_cm = cabinet_depth / 10.0  # Front of cabinet
z_position_cm = (cabinet_plinth_height + bottom_gap_mm) / 10.0  # Base alignment
```

### 2. Simplified Door Dimensions (furniture_model.py)

**Problem**: `calculate_door_dimensions()` was adding `18mm * 2` for panel thickness and `18mm` for top overlay, incompatible with DoorGenerator's gap handling.

**Solution**: Return nominal dimensions only:
```python
# For copertura_totale with 1 door:
larghezza_anta = larghezza_mobile / n_ante  # e.g., 600 / 1 = 600mm
altezza_anta = altezza_carcassa  # e.g., 720 - 100(plinth) = 620mm

# Gaps (side=1.5mm, top=2mm, bottom=0mm) applied by DoorGenerator
```

**Before**: 600mm cabinet → 634mm door width (600 + 36 - 2)  
**After**: 600mm cabinet → 600mm nominal → 597mm actual (600 - 2*1.5mm gaps)

### 3. Correct Plinth Source (wizard_command.py)

**Problem**: 
```python
# OLD (incorrect)
piedini = furniture.ferramenta.get('piedini', [])
has_plinth = len(piedini) > 0
plinth_height = piedini[0].get('altezza', 100) if has_plinth else 100
```

**Solution**:
```python
# NEW (correct)
zoccolo = getattr(furniture, 'zoccolo', None)
if zoccolo and zoccolo.get('presente', False):
    has_plinth = True
    plinth_height = zoccolo.get('altezza', 100)
else:
    has_plinth = False
    plinth_height = 0
```

### 4. Enhanced Logging

Added detailed bounding box logging to verify alignment:
```python
self.logger.info("📦 Bounding box anta finale (coordinate parent):")
self.logger.info(f"  X: [{bbox.minPoint.x:.2f}, {bbox.maxPoint.x:.2f}] cm")
self.logger.info(f"  Y: [{bbox.minPoint.y:.2f}, {bbox.maxPoint.y:.2f}] cm")
self.logger.info(f"  Z: [{bbox.minPoint.z:.2f}, {bbox.maxPoint.z:.2f}] cm")
```

### 5. Removed Debug Popups

Removed all `ui.messageBox()` debug popups from:
- `door_generator.py` (2 popups)
- `cabinet_generator.py` (1 popup)

## Expected Results

For a test case: **Base cucina 600×720×580mm, zoccolo 100mm, 1 anta copertura totale**

### Cabinet Carcass:
- Left side panel bbox: 
  - X: [0.0, 1.8] cm (18mm thickness)
  - Y: [0.0, 58.0] cm (580mm depth)
  - Z: [10.0, 72.0] cm (100mm plinth to 720mm top = 620mm carcass)

### Door (After Fix):
- Nominal dimensions: 600mm × 620mm
- After gaps: 597mm × 618mm (side gaps: 2×1.5mm, top gap: 2mm)
- Position:
  - X: 1.5mm (side gap)
  - Y: 580mm (at cabinet front)
  - Z: 100mm base (aligned with carcass base)
- Bounding box:
  - X: [0.15, 60.15] cm
  - Y: [56.2, 58.0] cm (18mm thickness from front)
  - Z: [10.0, 71.8] cm (620mm - 2mm top gap)

## Testing

All existing unit tests pass:
- ✅ `test_furniture_model.py`: Door dimensions now return correct nominal values
- ✅ `test_geometry.py`: Cabinet and door parameter tests pass

Manual testing required:
1. Create base cucina 600×720×580, zoccolo 100, 1 anta
2. Verify door base aligns with carcass base (Z=10cm)
3. Verify door height is ~62cm (carcass height - 2mm top gap)
4. Verify door front is at cabinet front (Y=58cm)

## Files Modified

1. **fusion_addin/lib/core/door_generator.py**:
   - Added 90° rotation transform
   - Updated positioning logic for rotated coordinates
   - Enhanced bounding box logging
   - Updated docstrings
   - Removed debug popups

2. **fusion_addin/lib/commands/wizard_command.py**:
   - Changed plinth source from `piedini` to `zoccolo`

3. **fusion_addin/lib/core/furniture_model.py**:
   - Simplified `calculate_door_dimensions()` to return nominal dimensions

4. **fusion_addin/lib/core/cabinet_generator.py**:
   - Removed debug popup

## Architecture Notes

- **No changes to CabinetGenerator coordinate system**: Cabinet continues to use X=width, Y=depth, Z=height
- **DoorDesigner unchanged**: Still computes door configs correctly
- **Backward compatible**: Existing furniture models and parameters work unchanged
- **Coordinate transform is transparent**: Door creation API unchanged, rotation handled internally

## Future Improvements

1. Consider creating door geometry directly on XZ plane to avoid rotation
2. Add unit tests for coordinate transformation
3. Consider adding optional bounding box verification in production (behind debug flag)
