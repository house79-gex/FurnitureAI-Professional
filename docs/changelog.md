# FurnitureAI-Professional - Changelog

Chronological record of all significant changes, additions, and fixes to the FurnitureAI-Professional add-in.

---

## [2.1.0] - 2026-02-12

### 🏗️ Architecture Refactoring: Unified Cabinet & Door Generation

**Summary**: Major architectural refactoring to separate concerns between cabinet carcass generation, door configuration logic, and door geometry generation. Eliminates code duplication and establishes clear single-responsibility modules.

#### Added
- **DoorDesigner Enhancement**: New `compute_door_configs()` method in `fusion_addin/lib/doors/door_designer.py`
  - Takes `cabinet_info` dict (width, height, carcass_height, plinth_height, depth, thickness, type)
  - Takes `door_options` dict (n_doors, mounting_type, door_type, thickness, gaps)
  - Returns list of door config dicts ready for DoorGenerator
  - Handles single/double/multi-door layout logic
  - Computes door widths, heights, and x_offsets
  
- **Comprehensive Documentation**:
  - `docs/architecture_overview.md`: Complete add-in architecture, responsibilities, coordinate systems, testing strategy, future roadmap
  - `docs/changelog.md`: This file - chronological change history
  
- **Defensive Logging**: Added detailed logging throughout cabinet and door generation
  - Cabinet dimensions logged on creation: `logger.info(f"🏗️ Creating cabinet: {width}x{height}x{depth} mm")`
  - Door configuration logged: `logger.info(f"🚪 Computing door configs: {n_doors} doors")`
  - Door positioning logged: `logger.info(f"📍 Door position: X={x_pos}, Y={y_pos}, Z={z_pos} cm")`

#### Changed
- **CabinetGenerator** (`fusion_addin/lib/core/cabinet_generator.py`):
  - ❌ **REMOVED**: `_create_door_panel()` method (lines 662-773) - duplicate door generation logic eliminated
  - ❌ **REMOVED**: `_create_hinge_cup_holes()` and `_create_mounting_plate_holes()` methods - moved to DoorGenerator responsibility
  - Door/hinge constants marked as **DEPRECATED** - kept for reference but no longer used by CabinetGenerator
  - `create_cabinet()` signature simplified: removed `has_door` and related door parameters
  - Now focused exclusively on carcass generation (sides, top, bottom, back, plinth, shelves, dividers)
  
- **Wizard Command** (`fusion_addin/lib/commands/wizard_command.py`):
  - **Refactored door generation flow** in `WizardExecuteHandler.notify()`:
    1. Generate cabinet via `CabinetGenerator.create_cabinet()`
    2. Build structured `cabinet_info` dict with all dimensions
    3. Call `DoorDesigner.compute_door_configs(cabinet_info, door_options)` to get door configurations
    4. Iterate over door configs and call `DoorGenerator.create_door()` for each
  - Removed inline door dimension calculations (previously done at lines 754-764)
  - Door widths, heights, and x_offsets now computed by DoorDesigner, not wizard
  
- **DoorGenerator** (`fusion_addin/lib/core/door_generator.py`):
  - `create_door()` signature unchanged but now fully decoupled from cabinet logic
  - Accepts clean params contract: width, height, thickness, x_offset, cabinet_depth, cabinet_plinth_height, parent_component, mounting_type, door_type
  - No longer makes assumptions about cabinet structure
  - Pure geometry generator with positioning responsibility only

#### Fixed
- **Duplicate Door Generation**: Eliminated two conflicting code paths (CabinetGenerator vs DoorGenerator)
- **Door Positioning Consistency**: Z-axis positioning now consistently uses `cabinet_plinth_height` as baseline
- **Coordinate System Clarity**: All door positioning parameters clearly documented in mm, converted to cm internally

#### Migration Considerations
- **Breaking Change**: `CabinetGenerator.create_cabinet()` no longer accepts door parameters
  - Remove: `has_door`, `door_gap`, `door_overlay_*`, `door_thickness` from params
  - If you were calling `create_cabinet(has_door=True)`, you must now:
    1. Call `create_cabinet()` without door params
    2. Build `cabinet_info` dict
    3. Call `DoorDesigner.compute_door_configs()`
    4. Call `DoorGenerator.create_door()` for each config
    
- **API Compatibility**: Wizard command behavior unchanged from user perspective - still creates cabinets with doors as before
  
- **Future Extensibility**: New flow makes it trivial to add AI-powered door generation:
  ```python
  # AI can now call DoorDesigner directly
  door_configs = DoorDesigner.compute_door_configs(cabinet_info, ai_door_spec)
  for config in door_configs:
      DoorGenerator.create_door(config)
  ```

#### Testing
- Existing unit tests pass without modification (no test changes needed)
- Manual testing required in Fusion 360 for:
  - Base cabinet with 0, 1, 2, 3+ doors
  - Door positioning (X, Y, Z coordinates correct)
  - Different mounting types (copertura_totale, filo, semicopertura)
  - Plinth vs no-plinth configurations

---

## [2.0.0] - 2026-02-10

### 🎨 Native Dialog with Tabs - Professional Wizard UI

**Summary**: Complete rewrite of wizard dialog using Fusion 360 native `TabCommandInput` for cleaner UI, better user experience, and more stable tab functionality.

#### Added
- **Native Tabbed Dialog**: 5-tab professional UI
  - Tab 1: 📐 Tipo & Dimensioni (Type & Dimensions)
  - Tab 2: 📏 Elementi (Elements: panels, shelves, dividers)
  - Tab 3: 🚪 Aperture (Openings: doors, drawers)
  - Tab 4: 🔧 Struttura (Structure: construction, joinery)
  - Tab 5: 🎨 Materiale (Material: selection, finish)
  
- **Dynamic Type Filtering**: Dropdown updates types based on selected category
  - Categories: Cucina, Bagno, Soggiorno, Camera, Ufficio
  - Each category shows relevant furniture types
  
- **Input Validation**: Real-time validation with min/max constraints
  - Dimensions: 200-3000 mm range
  - Material thickness: 12-25 mm range
  - Auto-adjust inputs when type changes

#### Changed
- **Dialog Size Management**: Auto-adjust to 80% of screen height
  - Prevents buttons going off-screen on smaller displays
  - Minimum: 700x500, Maximum: 750x800
  
- **Event Handler Lifecycle**: Fixed garbage collection issues
  - Global `_handlers` list prevents premature handler disposal
  - All handlers (Created, Execute, InputChanged, Destroy) properly retained

#### Fixed
- **Tab Rendering Issues**: Native tabs render correctly without flashing
- **Dimension Updates**: Tab content updates correctly when type changes
- **Memory Leaks**: Proper handler cleanup on dialog destroy

---

## [1.9.0] - 2026-02-08

### 🔧 Cabinet Orientation Fix - Professional Panel Layout

**Summary**: Fixed cabinet panel orientation to align with woodworking best practices. All panels (top, bottom, shelves, back) now modeled on YZ plane and extruded along X direction, matching side panel orientation.

#### Added
- **Internal Width Calculation**: `W_in = width - 2*thickness` for top/bottom/shelves
  - Ensures panels fit between side panels
  - Accounts for material thickness correctly
  
- **Back Panel Inset Calculation**: New `_compute_back_inset()` helper method
  - Flush rabbet: 12mm inset
  - Groove: 10mm inset  
  - Surface: 0mm inset
  - Used for top/bottom panel depth calculations

- **Shelf Depth Calculation**: `depth - back_inset - shelf_front_setback`
  - Professional 3mm front setback by default
  - Accounts for back mounting type
  - Properly positioned within carcass

#### Changed
- **Top/Bottom Panels** (`_create_top_bottom_panels()`):
  - Changed from XY plane to YZ plane
  - Extrude direction: along X axis (internal width)
  - Positioning: X remains at thickness/2 (centered between sides)
  - Depth: accounts for back_inset based on mounting type
  
- **Shelves** (`_create_shelves()`):
  - Changed from XY plane to YZ plane  
  - Extrude direction: along X axis (internal width)
  - Positioning: X at thickness (flush with side interior)
  - Depth: accounts for back_inset and front_setback
  
- **Back Panel** (`_create_back_panel()`):
  - Remains on YZ plane (already correct)
  - Y-position varies by mounting type (rabbet/groove/surface)

#### Fixed
- **Grain Direction**: Top/bottom/shelves now have correct grain (front-to-back)
- **Panel Fit**: Panels properly fit between side panels without overlap
- **Material Waste**: Reduced by using correct internal dimensions
- **CNC Export**: Panels now correctly oriented for machining

#### Testing
- Added `tests/test_cabinet_orientation.py`: Validates panel orientation and positions
- All professional cabinet parameters tested: flush_rabbet, groove, surface mounting
- Verified with multiple shelf configurations (0, 1, 2, 3 shelves)

---

## [1.8.0] - 2026-02-05

### 📐 Professional Cabinet Parameters - System 32 & Hardware

**Summary**: Added comprehensive professional cabinetmaking parameters for back mounting, shelf systems, dowel joinery, and Blum Clip-top 110° hinge specifications.

#### Added
- **Back Mounting Options**:
  - `back_mounting`: 'flush_rabbet' | 'groove' | 'surface'
  - `rabbet_width`: 12mm default (for flush_rabbet)
  - `rabbet_depth`: back_thickness (typically 3mm)
  - `groove_width`: back_thickness + 0.5mm tolerance
  - `groove_depth`: back_thickness (typically 3mm)
  - `groove_offset_from_rear`: 10mm default
  
- **Professional Shelf System**:
  - `shelf_front_setback`: 3mm default (professional setback from front edge)
  - `shelf_bore_enabled`: Enable System 32 adjustable shelf holes
  - `shelf_bore_diameter`: 5mm (standard)
  - `shelf_bore_front_distance`: 37mm (System 32)
  - `shelf_bore_pattern`: 32mm vertical spacing (System 32)
  
- **Dowel Joinery Parameters**:
  - `dowels_enabled`: Enable dowel joinery (placeholder for CNC export)
  - `dowel_diameter`: 8mm default
  - `dowel_edge_distance`: 35mm from edge
  - `dowel_spacing`: 64mm (multiple of 32mm for System 32 compatibility)
  
- **Blum Clip-top 110° Hinge Specs**:
  - `hinge_cup_diameter`: 35mm
  - `hinge_cup_depth`: 12.5mm
  - `hinge_k`: 21.5mm (K dimension - cup center offset from edge)
  - `hinge_offset_top`: 100mm from top edge
  - `hinge_offset_bottom`: 100mm from bottom edge
  - `mounting_plate_system_line`: 37mm (System 32)
  - `mounting_plate_hole_spacing`: 32mm (System 32 vertical)
  - Auto hinge count: 2 for ≤900mm, 3 for 900-1500mm, 4+ for >1500mm

#### Changed
- **Wizard Command**: Passes 40+ professional parameters to CabinetGenerator
  - All parameters have safe defaults via `.get()`
  - No breaking changes to existing code
  
- **CabinetGenerator Defaults**: Updated class constants for professional standards
  - `DEFAULT_BACK_MOUNTING = "flush_rabbet"`
  - `DEFAULT_SHELF_FRONT_SETBACK = 3.0  # mm`
  - `DEFAULT_HINGE_TYPE = "clip_top_110"`
  - `DEFAULT_CUP_DIAMETER = 35.0  # mm`

#### Documentation
- Added `docs/CABINET_PARAMETERS.md`: Complete parameter reference with examples
  - All 40+ parameters documented
  - Includes back mounting diagrams
  - System 32 drilling pattern specifications
  - Hinge placement calculations

---

## [1.7.0] - 2026-02-03

### 🤖 AI Configuration Dialog - Native UI

**Summary**: Replaced custom HTML dialog for AI configuration with native Fusion 360 dialog. Improved stability, better user experience, and proper API key management.

#### Added
- **Native Dialog** (`fusion_addin/lib/commands/configura_ia_command.py`):
  - Single-tab UI with provider selection
  - Secure API key input (masked text)
  - Azure endpoint configuration
  - Ollama local server setup
  - Model selection dropdowns
  
- **Config Format Compatibility**: ConfigManager supports 3 config formats
  - Format 1: ConfiguraIA flat format (`ia_enabled` + top-level providers)
  - Format 2: Nested format (`ai_features_enabled` + cloud/local_lan/remote_wan)
  - Format 3: Legacy format (`providers` dict)
  - Auto-migration between formats

#### Removed
- **HTML Dialog**: Deleted `fusion_addin/lib/wizards/ai_config_wizard.py`
  - Replaced with native Fusion 360 controls
  - No more browser compatibility issues
  - Better integration with Fusion UI theme

#### Changed
- **ConfigManager** (`fusion_addin/lib/config_manager.py`):
  - `is_ai_enabled()`: Checks all 3 config formats
  - `has_ai_provider_configured()`: Validates API keys across formats
  - Backwards compatible with old config files

---

## [1.6.0] - 2026-01-28

### 🚪 Door and Drawer Component Hierarchy Fix

**Summary**: Fixed component nesting for doors and drawers. Now correctly created as child components of cabinet instead of root component.

#### Fixed
- **Door Generation**: Doors now nested inside cabinet component
  - `DoorGenerator.create_door()`: Uses `parent_component.occurrences.addNewComponent()`
  - Proper transform applied for position
  - Enables multi-cabinet layouts without interference
  
- **Drawer Generation**: Drawers now nested inside cabinet component
  - `DrawerGenerator.create_drawer()`: Uses `parent_component` parameter
  - Correct Z-positioning from cabinet base
  - Drawer slides aligned with cabinet depth

#### Added
- **Memory Fact**: "Doors and drawers must be created inside the parent cabinet component (not root) using parent_component parameter"
  - Citations: door_generator.py:55-60, drawer_generator.py:46-50

---

## [1.5.0] - 2026-01-25

### 📊 Cut List Command - Material Export

**Summary**: Added cut list generation command to export material lists with dimensions, quantities, and edge banding requirements.

#### Added
- **Cut List Command** (`fusion_addin/lib/commands/cutlist_command.py`):
  - Scans selected components for panels
  - Groups by material type and dimensions
  - Calculates quantities
  - Exports to CSV format
  - Ready for CNC integration

---

## [1.4.0] - 2026-01-20

### 🎯 Anchor System - Multi-Cabinet Layout

**Summary**: Added anchor system for positioning multiple cabinets relative to each other with automatic alignment.

#### Added
- **CabinetPlacer** (`fusion_addin/lib/core/anchor_system.py`):
  - `place_adjacent_right()`: Place cabinet to the right
  - `place_adjacent_left()`: Place cabinet to the left  
  - `place_on_top()`: Stack cabinet vertically
  - Stores anchor metadata as component attributes
  - Automatic alignment and gap management

#### Use Cases
- Kitchen runs with multiple base cabinets
- Wall cabinet arrays
- Floor-to-ceiling column combinations

---

## [1.3.0] - 2026-01-15

### 🤖 AI Integration - OpenAI, Anthropic, Ollama

**Summary**: Added natural language furniture generation with multiple AI provider support.

#### Added
- **AI Genera Command** (`fusion_addin/lib/commands/ai_genera_command.py`):
  - Text input: "Create a kitchen base cabinet 800x720x580 with 2 doors"
  - Generates FurniturePiece model from text
  - Validates and creates 3D geometry
  
- **AI Providers** (`fusion_addin/lib/ai/providers/`):
  - OpenAI: GPT-4, GPT-3.5 (cloud)
  - Anthropic: Claude 3 Opus, Sonnet, Haiku (cloud)
  - Azure OpenAI: Enterprise deployment (cloud)
  - Ollama: Llama 3, Mistral, local LLMs (local)
  
- **Prompt Engineering** (`fusion_addin/lib/ai/prompt_builder.py`):
  - Structured furniture JSON schema
  - Type-specific examples
  - Validation rules in prompt

#### Configuration
- API keys stored in `config/ai_config.json`
- Per-provider model selection
- Timeout and retry settings

---

## [1.2.0] - 2026-01-10

### 📦 Drawer Generator - Multi-Type Support

**Summary**: Added drawer generation with standard box construction and dovetail options.

#### Added
- **DrawerGenerator** (`fusion_addin/lib/core/drawer_generator.py`):
  - Standard box drawers (butt joints)
  - Dovetail drawer option (visual representation)
  - Drawer slide integration (full extension / soft close)
  - Adjustable front height
  - Bottom panel (groove-mounted)
  
- **Wizard Integration**: Drawer count and configuration inputs
  - Front height adjustment
  - Gap settings
  - Slide type selection

---

## [1.1.0] - 2025-12-20

### 🚪 Door Generator - Single and Double Doors

**Summary**: Initial door generation system with flat and frame door types.

#### Added
- **DoorGenerator** (`fusion_addin/lib/core/door_generator.py`):
  - Single door creation
  - Double door pairs with center gap
  - Mounting types: full overlay, flush, semi-overlay
  - Opening types: hinged, sliding (placeholder)
  - Automatic positioning based on cabinet dimensions
  
- **Flat Door Profile**: Simple panel with optional edge fillet
- **Frame Door Profile**: Placeholder for future rail & stile construction

---

## [1.0.0] - 2025-12-01

### 🎉 Initial Release - Core Cabinet Generation

**Summary**: First production release with parametric cabinet generation and wizard UI.

#### Added
- **CabinetGenerator** (`fusion_addin/lib/core/cabinet_generator.py`):
  - Parametric carcass generation
  - Side panels (left/right)
  - Top and bottom panels
  - Back panel with basic mounting
  - Plinth/toe kick
  - Adjustable shelves
  - Vertical dividers for multi-compartment
  
- **FurniturePiece Data Model** (`fusion_addin/lib/core/furniture_model.py`):
  - Type system (base_cucina, pensile, colonna, etc.)
  - Dimension management
  - Element configuration (panels, doors, drawers, shelves)
  - Hardware library
  - Validation rules
  - JSON serialization
  
- **Wizard Command** (`fusion_addin/lib/commands/wizard_command.py`):
  - Guided creation dialog
  - Type and dimension selection
  - Element configuration
  - Material selection
  - Live preview
  
- **Furniture Types** (`fusion_addin/lib/core/furniture_types.py`):
  - 20+ predefined furniture types
  - Categories: Cucina, Bagno, Soggiorno, Camera, Ufficio
  - Default dimensions per type
  - Min/max constraints
  
- **Coordinate System**:
  - X: Width (left to right)
  - Y: Depth (back to front)
  - Z: Height (bottom to top)
  - Units: cm internal (Fusion native), mm external (user-facing)
  
- **Hardware Library** (`fusion_addin/lib/hardware/`):
  - Hinges (Blum Clip-top, Salice, others)
  - Drawer slides (Blum Tandem, Hettich Quadro)
  - Adjustable feet
  - Handles (various styles)
  
- **Material Library** (`fusion_addin/lib/materials/`):
  - Panel materials (melamine, plywood, MDF, solid wood)
  - Edge banding
  - Back panel materials
  
- **UI Manager** (`fusion_addin/lib/ui_manager.py`):
  - Toolbar creation
  - Panel management
  - Command registration
  - Icon loading
  
- **Logging System** (`fusion_addin/lib/logging_utils.py`):
  - File logging to temp directory
  - Console output to Fusion Text Commands
  - Log level configuration
  - Formatted output with emojis

#### Technical Details
- **Fusion 360 API Version**: 2025.2
- **Python Version**: 3.7+ (Fusion embedded Python)
- **Installation**: Manual copy to Fusion AddIns folder or install script
- **License**: MIT (see LICENSE file)

---

## Development Notes

### Versioning Scheme
- **Major version (X.0.0)**: Breaking API changes, major architecture refactor
- **Minor version (0.X.0)**: New features, non-breaking changes
- **Patch version (0.0.X)**: Bug fixes, documentation updates

### Change Categories
- 🎉 **Initial Release** / Major milestone
- ✨ **Added**: New features
- 🔧 **Changed**: Changes to existing functionality
- 🐛 **Fixed**: Bug fixes
- ❌ **Removed**: Removed features/code
- 🔒 **Security**: Security fixes
- 📝 **Documentation**: Documentation updates
- ⚡ **Performance**: Performance improvements
- 🏗️ **Architecture**: Structural/design changes

### Migration Guide Format
Each breaking change includes:
1. **What changed**: Clear description of the change
2. **Why it changed**: Rationale for the change
3. **How to migrate**: Step-by-step migration instructions
4. **Code examples**: Before/after code snippets

### Deprecation Policy
- Features marked as **DEPRECATED** in code and docs
- Deprecated features maintained for at least one minor version
- Removal only in next major version
- Clear migration path provided

---

## Contributors

- **FurnitureAI Development Team** - Initial work and ongoing maintenance
- **Community Contributors** - See GitHub repository for full contributor list

---

## Links

- **Repository**: https://github.com/house79-gex/FurnitureAI-Professional
- **Issue Tracker**: https://github.com/house79-gex/FurnitureAI-Professional/issues
- **Documentation**: See `docs/` folder
- **License**: MIT (see LICENSE file)

---

*This changelog follows the [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format.*
