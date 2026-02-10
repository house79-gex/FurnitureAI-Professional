# Cabinet Parameters Documentation

Complete reference for professional cabinet generator parameters including door, hinge, back mounting, shelf, and dowel configurations.

## Table of Contents
- [Basic Cabinet Parameters](#basic-cabinet-parameters)
- [Door Parameters](#door-parameters)
- [Hinge Parameters (Blum Clip-top 110°)](#hinge-parameters-blum-clip-top-110)
- [Back Mounting Parameters](#back-mounting-parameters)
- [Shelf Parameters](#shelf-parameters)
- [Dowel/Joinery Parameters](#doweljoinery-parameters)
- [Usage Examples](#usage-examples)

---

## Basic Cabinet Parameters

### Dimensions
- **width** (mm): Total cabinet width (default: 800)
- **height** (mm): Total cabinet height (default: 720)
- **depth** (mm): Total cabinet depth (default: 580)

### Material
- **material_thickness** (mm): Panel thickness for sides, top, bottom (default: 18)
- **back_thickness** (mm): Back panel thickness (default: 3)

### Structure
- **has_back** (bool): Include back panel (default: True)
- **has_plinth** (bool): Include plinth/base (default: True)
- **plinth_height** (mm): Plinth height (default: 100)
- **shelves_count** (int): Number of internal shelves (default: 0)
- **divisions_count** (int): Number of vertical dividers (default: 0)

---

## Door Parameters

### Basic Door Configuration
- **has_door** (bool): Include door panel (default: False)
- **door_gap** (mm): Gap between double doors or door edge (default: 2)
- **door_thickness** (mm): Door panel thickness (default: 18)

### Door Overlay (Full Overlay Default)
The door extends beyond the cabinet opening by these amounts:

- **door_overlay_left** (mm): Left side overlay (default: 18)
- **door_overlay_right** (mm): Right side overlay (default: 18)
- **door_overlay_top** (mm): Top overlay (default: 18)
- **door_overlay_bottom** (mm): Bottom overlay (default: 18)

**Calculation:**
```
door_width = (width - 2×material_thickness) + door_overlay_left + door_overlay_right
door_height = (height - plinth_height) + door_overlay_top + door_overlay_bottom
```

**Example:** For a 600mm wide cabinet with 18mm sides and 18mm overlays:
- Internal opening: 600 - 36 = 564mm
- Door width: 564 + 18 + 18 = 600mm

---

## Hinge Parameters (Blum Clip-top 110°)

Professional cabinet hinges using the industry-standard Blum Clip-top 110° system with self-closing spring.

### Hinge Cup Parameters
- **hinge_type**: "clip_top_110" (Blum Clip-top 110° with spring)
- **cup_diameter** (mm): Hinge cup hole diameter (default: 35)
- **cup_depth** (mm): Hinge cup hole depth (default: 12.5)
- **cup_center_offset_from_edge** (mm): K dimension - distance from door edge to cup center (default: 21.5)

### Hinge Positioning
- **hinge_offset_top** (mm): Distance from top edge to first hinge center (default: 100)
- **hinge_offset_bottom** (mm): Distance from bottom edge to last hinge center (default: 100)

### Auto Hinge Count
The system automatically determines hinge quantity based on door height:
- **≤ 900 mm**: 2 hinges
- **901-1500 mm**: 3 hinges
- **> 1500 mm**: 4 hinges

**Thresholds (configurable):**
- **hinge_threshold_2** (mm): Maximum height for 2 hinges (default: 900)
- **hinge_threshold_3** (mm): Maximum height for 3 hinges (default: 1500)

### Mounting Plate Parameters (System 32)
- **mounting_plate_system_line** (mm): Distance from front edge to mounting holes (default: 37)
- **mounting_plate_hole_spacing** (mm): Vertical spacing between holes (default: 32)
- **mounting_plate_hole_diameter** (mm): Hole diameter (default: 5)
- **screw_depth** (mm): Screw hole depth for euro-screw (default: 13)

**System 32 Standard:**
The mounting plate holes follow the System 32 standard with 32mm vertical spacing and 37mm offset from the front edge (system line).

---

## Back Mounting Parameters

Three mounting methods are supported for the back panel:

### 1. Flush Rabbet (Default)
Back panel sits in a rabbet cut, flush with the rear surface.

- **back_mounting**: "flush_rabbet"
- **rabbet_width** (mm): Rabbet width (default: 12)
- **rabbet_depth** (mm): Rabbet depth (default: back_thickness)

**Effect:** Shelves and internal components are shortened by `rabbet_width`.

### 2. Groove
Back panel slides into a groove cut into the side panels.

- **back_mounting**: "groove"
- **groove_width** (mm): Groove width (default: back_thickness + 0.5)
- **groove_depth** (mm): Groove depth (default: back_thickness)
- **groove_offset_from_rear** (mm): Distance from rear edge to groove (default: 10)

**Effect:** Shelves and internal components are shortened by `groove_offset_from_rear`.

### 3. Surface Mount
Back panel is attached to the rear surface without cuts.

- **back_mounting**: "surface"

**Effect:** No reduction in shelf depth; back sits on the rear face.

---

## Shelf Parameters

### Shelf Positioning
- **shelf_front_setback** (mm): Distance shelves are set back from front edge (default: 3)

**Shelf Depth Calculation:**
```
shelf_depth = depth - shelf_front_setback - back_inset

where back_inset depends on back_mounting type:
  - flush_rabbet: back_inset = rabbet_width (12mm)
  - groove: back_inset = groove_offset_from_rear (10mm)
  - surface: back_inset = 0
```

### Adjustable Shelf Holes (System 32)
Optional drilling pattern for adjustable shelves:

- **shelf_bore_enabled** (bool): Enable shelf pin holes (default: False)
- **shelf_bore_diameter** (mm): Hole diameter (default: 5)
- **shelf_bore_front_distance** (mm): Distance from front edge (default: 37)
- **shelf_bore_pattern** (mm): Vertical spacing between holes (default: 32)

---

## Dowel/Joinery Parameters

Placeholder for future integration with Lavorazioni machining system:

- **dowels_enabled** (bool): Enable dowel joinery (default: False)
- **dowel_diameter** (mm): Dowel hole diameter (default: 8)
- **dowel_edge_distance** (mm): Distance from panel edge (default: 35)
- **dowel_spacing** (mm): Spacing between dowels (default: 64, multiple of 32mm)

---

## Usage Examples

### Example 1: Basic Cabinet with Door and Hinges
```python
from fusion_addin.lib.core.cabinet_generator import CabinetGenerator

# Create cabinet with door
params = {
    'width': 600,          # 600mm wide
    'height': 900,         # 900mm tall
    'depth': 500,          # 500mm deep
    'material_thickness': 18,
    'has_plinth': True,
    'plinth_height': 100,
    'has_back': True,
    'back_mounting': 'flush_rabbet',
    'has_door': True,      # Add door
    'door_gap': 2,
    'door_overlay_left': 18,
    'door_overlay_right': 18,
    'door_overlay_top': 18,
    'door_overlay_bottom': 18
}

generator = CabinetGenerator(design)
cabinet = generator.create_cabinet(params)
```

**Result:**
- Side panels: Z range 100mm to 900mm (800mm effective height)
- Bottom panel: at Z=100mm
- Top panel: at Z=882mm (100 + 800 - 18)
- Internal width: X from 18mm to 582mm (564mm span)
- Door: 600mm wide × 836mm tall with 2 hinges (auto-calculated)

### Example 2: Cabinet with Shelves and Groove Back
```python
params = {
    'width': 800,
    'height': 1200,
    'depth': 580,
    'material_thickness': 18,
    'has_back': True,
    'back_mounting': 'groove',       # Use groove mounting
    'groove_offset_from_rear': 10,
    'shelves_count': 3,              # 3 internal shelves
    'shelf_front_setback': 3,        # 3mm front setback
    'shelf_bore_enabled': True,      # Add adjustment holes
}

cabinet = generator.create_cabinet(params)
```

**Result:**
- Shelves depth: 580 - 3 - 10 = 567mm
- Back panel in groove 10mm from rear
- 3 evenly-spaced shelves with System 32 holes

### Example 3: Tall Cabinet with Custom Hinge Configuration
```python
params = {
    'width': 600,
    'height': 1800,        # Tall cabinet
    'depth': 500,
    'has_door': True,
    'hinge_offset_top': 120,      # Custom top offset
    'hinge_offset_bottom': 120,   # Custom bottom offset
    # Will auto-generate 4 hinges for 1800mm height
}

cabinet = generator.create_cabinet(params)
```

**Result:**
- Door height: ~1700mm (after plinth)
- 4 hinges auto-calculated (height > 1500mm)
- Custom spacing: 120mm from edges

### Example 4: Override All Hinge Parameters
```python
params = {
    'width': 600,
    'height': 900,
    'depth': 500,
    'has_door': True,
    # Blum parameters (custom)
    'cup_diameter': 35,
    'cup_depth': 12.5,
    'cup_center_offset_from_edge': 21.5,  # K dimension
    'hinge_offset_top': 100,
    'hinge_offset_bottom': 100,
    # Mounting plate (System 32)
    'mounting_plate_system_line': 37,
    'mounting_plate_hole_spacing': 32,
    'mounting_plate_hole_diameter': 5,
}

cabinet = generator.create_cabinet(params)
```

---

## Parameter Validation

All parameters have sensible defaults. The generator validates:
- Dimensions must be positive
- Overlays must not create negative opening sizes
- Hinge offsets must leave room for multiple hinges
- Material thickness must be compatible with cabinet size

---

## Units

**All input parameters use millimeters (mm).**

The generator internally converts to centimeters (cm) for Fusion 360 API using the constant:
```python
MM_TO_CM = 10.0
```

---

## Coordinate System

- **X axis**: Width (left to right)
- **Y axis**: Depth (front to back, Y=0 is back)
- **Z axis**: Height (bottom to top)

**Panel Orientations:**
- Side panels: YZ plane, extrude along X
- Top/Bottom panels: YZ plane, extrude along X
- Back panel: YZ plane, extrude along X
- Shelves: YZ plane, extrude along X
- Plinth: XY plane, extrude along Z

---

## Notes

### Production-Ready Features
- ✅ Full overlay door calculation
- ✅ Auto hinge count based on height
- ✅ Blum Clip-top 110° preset
- ✅ System 32 mounting plate holes
- ✅ Three back mounting methods
- ✅ Shelf front setback and back inset
- 🚧 Actual hole drilling (placeholder)
- 🚧 Rabbet/groove machining cuts (placeholder)

### Future Enhancements
- Dowel joinery integration with Lavorazioni
- Double door support with separate left/right panels
- Soft-close hinge variants
- Additional hinge types (Salice, Grass, Häfele)
- CNC drilling patterns export

---

## Implementation Details

### Helper Functions

#### `_compute_back_inset(back_mounting, groove_offset, rabbet_width=12)`

Calculates the depth reduction for shelves and internal components based on back mounting type.

```python
def _compute_back_inset(self, back_mounting, groove_offset, rabbet_width=12):
    """
    Calculates the back inset based on the back mounting type.
    
    Returns:
        float: Inset in mm
    """
    if back_mounting == 'flush_rabbet':
        return rabbet_width  # 12mm default
    elif back_mounting == 'groove':
        return groove_offset  # 10mm default
    else:  # 'surface'
        return 0  # No depth reduction
```

**Usage in shelf creation:**
```python
# Calculate effective shelf depth
back_inset = self._compute_back_inset(back_mounting, groove_offset, rabbet_width)
shelf_depth_eff = depth - back_inset - shelf_front_setback
```

**Examples:**
- Cabinet depth: 500mm, back_mounting: 'flush_rabbet', shelf_front_setback: 3mm
  - back_inset = 12mm → shelf_depth = 500 - 12 - 3 = **485mm**
- Cabinet depth: 500mm, back_mounting: 'groove', groove_offset: 10mm, shelf_front_setback: 3mm
  - back_inset = 10mm → shelf_depth = 500 - 10 - 3 = **487mm**
- Cabinet depth: 500mm, back_mounting: 'surface', shelf_front_setback: 3mm
  - back_inset = 0mm → shelf_depth = 500 - 0 - 3 = **497mm**

### Unit Conversion Helper

#### `_mm_to_cm(value_mm)`

Converts millimeters to centimeters for Fusion 360 API.

```python
def _mm_to_cm(self, value_mm):
    """
    Converts millimeters to centimeters (for Fusion 360 API).
    
    Args:
        value_mm: Value in millimeters
    
    Returns:
        float: Value in centimeters
    """
    return value_mm / MM_TO_CM  # MM_TO_CM = 10.0
```

**Usage:**
```python
# Convert dimension for Fusion API
width_cm = self._mm_to_cm(width_mm)

# Alternative inline conversion (also valid)
value_cm = value_mm / MM_TO_CM
value_cm = value_mm / 10.0
```

### Panel Orientation (YZ Plane)

All horizontal panels (Top, Bottom, Shelves, Back) are modeled on the YZ plane and extruded along X:

```python
# Bottom panel on YZ, extrude along X by internal width
W_in_mm = width - 2 * thickness  # Internal width
W_in_cm = W_in_mm / 10.0

sketch_bottom = sketches.add(yz_plane)
sketch_bottom.sketchCurves.sketchLines.addTwoPointRectangle(
    adsk.core.Point3D.create(0, Z_bottom_cm, 0),
    adsk.core.Point3D.create(depth_cm, (Z_bottom_mm + thickness) / 10.0, 0)
)
extrude_input = extrudes.createInput(sketch_bottom.profiles.item(0), ...)
extrude_input.setDistanceExtent(False, adsk.core.ValueInput.createByReal(W_in_cm))
```

**Z Coordinate Calculations:**
```python
# Bottom panel Z position
Z_bottom_mm = plinth_height  # e.g., 100mm

# Top panel Z position
H_eff_mm = height - plinth_height  # Effective height above plinth
Z_top_mm = plinth_height + H_eff_mm - thickness  # e.g., 100 + 800 - 18 = 882mm
```

### Wizard Parameter Passing

The wizard passes all professional parameters with defaults to the cabinet generator:

```python
cabinet_params = {
    # Basic dimensions
    'width': dimensioni['larghezza'],
    'height': dimensioni['altezza'],
    'depth': dimensioni['profondita'],
    'material_thickness': furniture.elementi['fianchi']['spessore'],
    
    # Back mounting
    'back_mounting': 'flush_rabbet',
    'rabbet_width': 12,
    'groove_offset_from_rear': 10,
    
    # Shelves
    'shelf_front_setback': 3,
    'shelf_bore_enabled': False,
    
    # Dowels
    'dowels_enabled': False,
    'dowel_diameter': 8,
    
    # Doors/Hinges (Blum Clip-top 110°)
    'door_gap': 2,
    'door_overlay_left': 18,
    'door_overlay_right': 18,
    'hinge_cup_diameter': 35,
    'hinge_offset_top': 100,
    # ... additional parameters
}

cabinet_generator = CabinetGenerator(design)
cabinet_comp = cabinet_generator.create_cabinet(cabinet_params)
```

---

## References

- **Blum Clip-top 110°**: Industry standard concealed hinge
- **System 32**: European standard for hole spacing (32mm grid)
- **K Dimension**: Standard measurement for hinge cup offset (21.5mm for Clip-top)
- **Full Overlay**: Door covers the entire cabinet front with 18mm standard overlay

---

*Last updated: 2026-02-10*
