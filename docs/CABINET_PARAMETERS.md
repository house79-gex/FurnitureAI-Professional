# Cabinet Generator - Professional Parameters

## Overview

The cabinet generator now supports professional cabinetry parameters for accurate furniture manufacturing, including proper panel orientation, back mounting options, and machining preparations.

## Panel Orientation (Fixed in v2.0)

### Previous Issue
Bottom, Top, Shelves, and Back panels were misoriented, causing alignment issues with side panels.

### Current Implementation
All panels are now correctly oriented:
- **Side panels (Fianco_Sinistro/Fianco_Destro)**: Modeled on YZ plane, extruded along X (thickness)
- **Bottom (Fondo)**: Modeled on YZ plane, extruded along X (internal width = W_in)
- **Top (Cielo)**: Modeled on YZ plane, extruded along X (internal width = W_in)
- **Shelves (Ripiani)**: Modeled on YZ plane, extruded along X (internal width = W_in)
- **Back (Retro)**: Modeled on YZ plane, extruded along X (width between sides)

This ensures all panels have consistent orientation with normals aligned properly.

## Parameters Reference

### Basic Dimensions
```python
params = {
    'width': 800,           # Total cabinet width (mm)
    'height': 720,          # Total cabinet height (mm)
    'depth': 580,           # Total cabinet depth (mm)
    'material_thickness': 18,  # Panel thickness (mm)
    'plinth_height': 100,   # Plinth/base height (mm)
    'has_plinth': True,     # Include plinth
}
```

### Back Panel Mounting

#### back_mounting
Type: `string` (enum)  
Default: `'flush_rabbet'`  
Options:
- `'flush_rabbet'`: Rabbet joint (battuta) - back sits flush in rabbet cut
- `'groove'`: Groove joint (canale) - back sits in routed groove
- `'surface'`: Surface mount - back panel overlaid on interior

#### Rabbet Parameters (for flush_rabbet)
```python
params = {
    'back_mounting': 'flush_rabbet',
    'rabbet_width': 12,     # Width of rabbet cut (mm) - default 12mm
    'rabbet_depth': 3,      # Depth of rabbet cut (mm) - default = back_thickness
}
```

The rabbet is a rectangular cut on the inner rear edge of side panels (and optionally top/bottom) to seat the back panel flush with the exterior.

#### Groove Parameters (for groove)
```python
params = {
    'back_mounting': 'groove',
    'groove_width': 3.5,    # Width of groove (mm) - default = back_thickness + 0.5mm clearance
    'groove_depth': 3,      # Depth of groove (mm) - default = back_thickness
    'groove_offset_from_rear': 10,  # Distance from rear edge (mm) - default 10mm
}
```

The groove is a routed pocket (fresata) on the inner face of side panels to accept the back panel with proper clearance.

#### Back Thickness
```python
params = {
    'back_thickness': 3,    # Thickness of back panel (mm) - default 3mm
    'has_back': True,       # Include back panel
}
```

### Shelf Parameters

#### shelf_front_setback
Type: `float`  
Default: `3` (mm)  
Description: Distance shelves are set back from the front edge

```python
params = {
    'shelves_count': 2,           # Number of shelves
    'shelf_front_setback': 3,     # Setback from front (mm) - default 3mm
}
```

Effective shelf depth is calculated as:
```
shelf_depth_eff = depth - retro_inset - shelf_front_setback
```

Where `retro_inset` depends on back mounting:
- `flush_rabbet`: 0mm (back is flush)
- `groove`: groove_offset_from_rear (default 10mm)
- `surface`: back_thickness (default 3mm)

### Dowel/Joint Parameters (Placeholders)

```python
params = {
    'dowels_enabled': False,      # Enable dowel drilling
    'dowel_diameter': 8,          # Dowel diameter (mm) - default 8mm
    'dowel_edge_distance': 37,    # Distance from edge (mm) - default 37mm
    'dowel_spacing': 32,          # Spacing between dowels (mm) - default 32mm (32mm system)
}
```

Note: Dowel holes are prepared as placeholders. Full implementation will integrate with the `fusion_addin/lib/joinery` module.

### Door Parameters (Placeholders)

```python
params = {
    'door_overlay_left': 0,       # Left overlay (mm)
    'door_overlay_right': 0,      # Right overlay (mm)
    'door_overlay_top': 0,        # Top overlay (mm)
    'door_overlay_bottom': 0,     # Bottom overlay (mm)
    'door_gap': 2,                # Gap between doors (mm) - default 2mm
}
```

These parameters prepare the API for door generator integration.

## Position Calculations

### Example: 600×900×500mm cabinet with 100mm plinth, 18mm thickness

```
Internal Width (W_in) = 600 - 2×18 = 564mm

Side Panels:
  - Start Z: 100mm (plinth_height)
  - End Z: 900mm (total height)
  - Height: 800mm (effective_height)

Bottom Panel:
  - Z position: 100mm
  - X span: 18mm → 582mm (positioned between sides)
  - Y span: 0 → 500mm (full depth)

Top Panel:
  - Z position: 882mm (plinth_height + effective_height - thickness)
  - X span: 18mm → 582mm (positioned between sides)
  - Y span: 0 → 500mm (full depth)

Shelves (with 3mm front setback, flush_rabbet back):
  - X span: 18mm → 582mm (positioned between sides)
  - Y span: 3mm → 500mm (depth - 0 - 3)
  - Effective depth: 497mm
```

## Machining Placeholders

### Rabbet Cuts
Function: `_create_rabbet_cuts()`

Creates extrude-cut features on the inner rear edges of side panels for rabbet joints.

**Status**: Placeholder - to be implemented with full 3D machining

### Groove Cuts
Function: `_create_groove_cuts()`

Creates pocket (fresata) features on the inner faces of side panels for groove joints.

**Status**: Placeholder - to be implemented with full 3D machining

### Dowel Holes
Function: `_create_dowel_holes()`

Creates cylindrical extrude-cut features for dowel joints using the 32mm system.

**Status**: Placeholder - to be integrated with `fusion_addin/lib/joinery`

## Future Integration

### Lavorazioni Module
The placeholder functions provide clean API hooks for future integration with a dedicated machining module:
- Rabbet and groove cutting with CNC paths
- Shelf pin holes (32mm system)
- Dowel drilling with precise positioning
- Hinge boring
- Handle drilling

### Door Generator
Door parameters expose the necessary interface for the door generator to:
- Calculate door dimensions with proper overlays
- Position doors with correct gaps
- Mount hinges at appropriate positions

## User Parameters in Fusion 360

All professional parameters are exposed as Fusion 360 User Parameters (Italian names):
- `Larghezza` - Width
- `Altezza` - Height
- `Profondita` - Depth
- `Spessore` - Panel thickness
- `SpessoreRetro` - Back thickness
- `AltezzaZoccolo` - Plinth height
- `LarghezzaBattuta` - Rabbet width
- `ProfonditaBattuta` - Rabbet depth
- `LarghezzaCanale` - Groove width
- `ProfonditaCanale` - Groove depth
- `OffsetCanaleRetro` - Groove offset from rear
- `ArretamentoRipianiFronte` - Shelf front setback
- `DiametroTassello` - Dowel diameter
- `DistanzaTasselloBordo` - Dowel edge distance
- `SpaziaturaTasselli` - Dowel spacing

These parameters can be modified in Fusion 360's Parameter dialog to update the cabinet parametrically.

## Example Usage

```python
from fusion_addin.lib.core.cabinet_generator import CabinetGenerator

# Initialize generator
generator = CabinetGenerator(design)

# Create cabinet with professional parameters
params = {
    # Basic dimensions
    'width': 600,
    'height': 900,
    'depth': 500,
    'material_thickness': 18,
    'plinth_height': 100,
    'has_plinth': True,
    
    # Back mounting with rabbet
    'has_back': True,
    'back_thickness': 3,
    'back_mounting': 'flush_rabbet',
    'rabbet_width': 12,
    'rabbet_depth': 3,
    
    # Shelves with setback
    'shelves_count': 2,
    'shelf_front_setback': 3,
    
    # Dowels (optional)
    'dowels_enabled': False,
    'dowel_diameter': 8,
    'dowel_edge_distance': 37,
    'dowel_spacing': 32,
}

cabinet = generator.create_cabinet(params)
```

## Testing

Test suite: `fusion_addin/tests/test_cabinet_orientation.py`

Run tests:
```bash
python -m unittest fusion_addin/tests/test_cabinet_orientation.py
```

Tests validate:
- Panel position calculations
- Internal width calculations
- Shelf depth with setback and inset
- Retro inset for different mounting types
- Parameter defaults and ranges
