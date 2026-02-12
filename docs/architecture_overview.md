# FurnitureAI-Professional - Architecture Overview

**Version**: 2.0  
**Last Updated**: 2026-02-12  
**Status**: Production-ready base features, AI integration in progress

---

## Table of Contents
1. [Overview](#overview)
2. [High-Level Architecture](#high-level-architecture)
3. [Core Components](#core-components)
4. [Cabinet & Door Generation Flow](#cabinet--door-generation-flow)
5. [Command System](#command-system)
6. [Data Model](#data-model)
7. [AI Integration Points](#ai-integration-points)
8. [Testing Strategy](#testing-strategy)
9. [Future Roadmap](#future-roadmap)

---

## Overview

**FurnitureAI-Professional** is a Autodesk Fusion 360 add-in for professional furniture design and manufacturing. It provides parametric cabinet generation, door design with multiple profiles, hardware management, and AI-powered design assistance.

### Key Features
- **Parametric Cabinet Generation**: Professional carcass creation with System 32 drilling patterns, professional back mounting (flush rabbet, groove, surface), and adjustable shelf systems
- **Door Design System**: Multiple door profiles (flat, shaker, raised panel, glass, custom), automatic hinge placement (Blum Clip-top 110°), configurable mounting types
- **Drawer Generation**: Standard and dovetail drawers with slide integration
- **Hardware Management**: Comprehensive hardware library (hinges, slides, handles, feet) with automatic suggestions
- **Cut List & Export**: Automatic material lists with CNC export capabilities
- **AI Integration**: Natural language furniture generation (OpenAI, Azure OpenAI, Anthropic, local LLMs via Ollama)

### Target Users
- Cabinet makers and furniture manufacturers
- Interior designers and architects  
- CNC shop operators
- Hobbyist woodworkers with Fusion 360

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Fusion 360 Add-in Layer                      │
│                  (FurnitureAI.py + manifest)                    │
└──────────────────────────┬──────────────────────────────────────┘
                           │
           ┌───────────────┴───────────────┐
           │    fusion_addin/lib/          │
           │                               │
    ┌──────┴──────┬─────────┬──────────┬──┴────────┬────────┐
    │             │         │          │           │        │
┌───▼────┐  ┌────▼───┐ ┌───▼────┐ ┌───▼────┐ ┌───▼───┐ ┌─▼──┐
│commands│  │  core  │ │ doors  │ │joinery │ │  ai   │ │ ui │
└───┬────┘  └────┬───┘ └───┬────┘ └────────┘ └───┬───┘ └────┘
    │            │         │                      │
    │            │         │                      │
    ├─ wizard   │         │                      │
    ├─ cutlist  │         │                      │
    ├─ ai_genera│         │                      │
    │            │         │                      │
    │      ┌─────┴──────┐  │                ┌─────┴─────┐
    │      │            │  │                │           │
    │   ┌──▼───┐  ┌────▼──▼──┐      ┌──────▼─┐  ┌─────▼────┐
    │   │Cabinet│  │Door     │      │ OpenAI │  │ Anthropic│
    │   │Gen.   │  │Generator│      └────────┘  └──────────┘
    │   └───────┘  └─────────┘
    │
    └─► FurniturePiece (data model)
```

### Directory Structure

```
FurnitureAI-Professional/
├── FurnitureAI.py              # Add-in entry point
├── FurnitureAI.manifest        # Fusion 360 manifest
├── docs/                       # Documentation
│   ├── architecture_overview.md (this file)
│   ├── changelog.md
│   ├── CABINET_PARAMETERS.md
│   └── ai_configuration.md
├── fusion_addin/
│   ├── lib/
│   │   ├── commands/           # UI commands
│   │   │   ├── wizard_command.py       # Main wizard UI
│   │   │   ├── ai_genera_command.py    # AI generation
│   │   │   ├── cutlist_command.py      # Cut list export
│   │   │   └── door_designer_command.py
│   │   ├── core/               # Core geometry generators
│   │   │   ├── cabinet_generator.py    # Carcass generation
│   │   │   ├── door_generator.py       # Door geometry
│   │   │   ├── drawer_generator.py     # Drawer generation
│   │   │   ├── furniture_model.py      # Data model (FurniturePiece)
│   │   │   ├── furniture_types.py      # Type definitions
│   │   │   ├── geometry_builder.py     # Low-level helpers
│   │   │   ├── anchor_system.py        # Multi-cabinet layout
│   │   │   └── cutlist.py              # Material list generation
│   │   ├── doors/              # Door design system
│   │   │   ├── door_designer.py        # Door configuration logic
│   │   │   ├── profile_flat.py         # Flat door profile
│   │   │   ├── profile_shaker.py       # Shaker profile
│   │   │   ├── profile_raised.py       # Raised panel
│   │   │   ├── profile_glass.py        # Glass insert
│   │   │   └── profile_custom.py       # Custom DXF import
│   │   ├── joinery/            # Joinery and drilling
│   │   │   ├── system32.py
│   │   │   ├── dowels.py
│   │   │   └── pocket_holes.py
│   │   ├── ai/                 # AI integration
│   │   │   ├── providers/
│   │   │   │   ├── openai_provider.py
│   │   │   │   ├── anthropic_provider.py
│   │   │   │   └── ollama_provider.py
│   │   │   └── prompt_builder.py
│   │   ├── hardware/           # Hardware libraries
│   │   ├── materials/          # Material definitions
│   │   ├── ui_manager.py       # UI utilities
│   │   ├── config_manager.py   # Configuration
│   │   └── logging_utils.py    # Logging
│   ├── scripts/
│   │   └── install.sh          # Installation script
│   └── tests/                  # Unit tests
├── resources/                  # Icons, images
└── config/                     # Configuration files
```

---

## Core Components

### 1. CabinetGenerator (`fusion_addin/lib/core/cabinet_generator.py`)

**Responsibility**: Generate parametric furniture carcass (structural box) with professional machining features.

**What It Does**:
- Creates side panels (left/right vertical panels)
- Creates top and bottom horizontal panels
- Creates back panel with configurable mounting (flush rabbet, groove, surface)
- Creates plinth/toe kick base
- Creates adjustable shelves with front setback
- Creates vertical dividers for multi-compartment cabinets
- Generates System 32 drilling patterns (placeholder for CNC export)
- Generates dowel joinery placeholders
- Stores user parameters in Fusion component

**What It Does NOT Do** (as of architecture refactor):
- ❌ Does NOT create doors (removed duplicate door generation logic)
- ❌ Does NOT create drawers
- ❌ Does NOT handle door configuration/layout logic

**Key Methods**:
```python
create_cabinet(params) -> adsk.fusion.Component
    # Main entry point
    # Params: width, height, depth, material_thickness, has_back, 
    #         back_thickness, back_mounting, has_plinth, plinth_height,
    #         shelves_count, divisions_count, etc. (all in mm)
    # Returns: Cabinet component with all carcass geometry
```

**Coordinate System**:
- **X**: Width (left to right)
- **Y**: Depth (back to front, Y=0 is back)
- **Z**: Height (bottom to top, Z=0 is floor)
- **Units**: Internal cm (Fusion 360 standard), input/output in mm

**Default Professional Settings**:
- System 32 drilling: 37mm system line, 32mm vertical spacing
- Blum Clip-top 110° hinge specs: 35mm cup, 12.5mm depth, K=21.5mm
- Back mounting options: flush_rabbet (12mm), groove (10mm), surface (0mm)
- Shelf front setback: 3mm default
- Dowel joinery: 8mm diameter, 35mm edge distance, 64mm spacing

---

### 2. DoorGenerator (`fusion_addin/lib/core/door_generator.py`)

**Responsibility**: Generate door geometry and position it in 3D space relative to the cabinet.

**What It Does**:
- Creates single door geometry (flat or frame style)
- Creates double door pairs
- Positions door in 3D based on:
  - `x_offset`: Horizontal position from left cabinet edge
  - `cabinet_plinth_height`: Z-baseline for door (typically plinth top)
  - `cabinet_depth`: Y-position for mounting type (overlay/flush/semi-overlay)
- Applies small gaps (1.5mm sides, 2mm top, 0mm bottom by default)
- Creates door as child component of parent cabinet
- Handles mounting types: `copertura_totale` (full overlay), `filo` (flush), `semicopertura` (semi-overlay)

**What It Does NOT Do**:
- ❌ Does NOT decide how many doors to create
- ❌ Does NOT calculate door widths/heights from cabinet
- ❌ Does NOT compute x_offset positioning logic
- ❌ Does NOT handle door profiles (delegates to profile modules)

**Key Methods**:
```python
create_door(params) -> adsk.fusion.Component
    # Params: width, height, thickness, door_type, position,
    #         parent_component, cabinet_depth, cabinet_plinth_height,
    #         x_offset, mounting_type (all dimensions in mm)
    # Returns: Door component positioned in 3D

create_double_door(params) -> tuple[Component, Component]
    # Creates pair of doors with central gap
```

**Positioning Logic**:
```python
# X: left edge + x_offset + side_gap
x_position_cm = (x_offset_mm + side_gap_mm) / 10.0

# Y: front of cabinet minus thickness (for overlay)
if mounting_type == "copertura_totale":
    y_position_cm = (cabinet_depth - thickness) / 10.0

# Z: plinth top + bottom_gap
z_position_cm = (cabinet_plinth_height + bottom_gap_mm) / 10.0
```

---

### 3. DoorDesigner (`fusion_addin/lib/doors/door_designer.py`)

**Responsibility**: Compute door configurations (business logic layer) from high-level cabinet and furniture data.

**What It Does** (after refactor):
- Takes `cabinet_info` dict (width, height, carcass_height, plinth_height, depth, thickness, type)
- Takes `door_options` dict from furniture model (n_doors, mounting_type, door_type, thickness, gaps)
- Computes how many doors to create (single, double, triple, etc.)
- Calculates each door's dimensions (width, height after gaps)
- Calculates each door's x_offset position
- Returns list of door config dicts ready for DoorGenerator

**Key Methods** (new architecture):
```python
compute_door_configs(cabinet_info, door_options) -> list[dict]
    # Returns list of dicts:
    # [
    #   {
    #     'width': 400, 'height': 700, 'thickness': 18,
    #     'door_type': 'flat', 'position': 'left',
    #     'x_offset': 0, 'mounting_type': 'copertura_totale'
    #   },
    #   ...
    # ]

create_door_with_profile(params) -> Component
    # Delegates to profile modules (profile_flat, profile_shaker, etc.)
    # Used for specialized door creation with decorative profiles

get_profile_info(profile_type) -> dict
    # Returns metadata about door profile types

estimate_cost(params) -> dict
    # Estimates material and machining costs
```

**Door Configuration Logic** (example):
```python
# Single door: uses full width minus gaps
door_width = cabinet_width - 2 * side_gap

# Double doors: split width, add center gap
single_width = (cabinet_width - center_gap) / 2

# Door height: carcass height minus top gap
door_height = carcass_height - top_gap - bottom_gap
```

---

### 4. FurniturePiece Data Model (`fusion_addin/lib/core/furniture_model.py`)

**Responsibility**: Unified data model for all furniture configuration.

**Structure**:
```python
FurniturePiece:
    - tipo: str (e.g., 'base_cucina', 'pensile', 'colonna')
    - dimensioni: dict {'larghezza': 800, 'altezza': 720, 'profondita': 580}
    - materiale_principale: str
    - elementi: dict {
        'fianchi': {'spessore': 18},
        'top': {'tipo': 'a_cappello', 'spessore': 18},
        'fondo': {'presente': True, 'spessore': 18},
        'schienale': {'presente': True, 'spessore': 3},
        'ante': [
            {'tipo_montaggio': 'copertura_totale', 
             'larghezza': 400, 'altezza': 700, 'spessore': 18,
             'apertura': 'cerniera', 'materiale': 'truciolare'}
        ],
        'cassetti': [...],
        'ripiani': [...]
    }
    - ferramenta: dict {
        'cerniere': [...],
        'guide_cassetto': [...],
        'piedini': [...],
        'maniglie': [...]
    }
```

**Key Methods**:
```python
validate() -> (bool, list[str])
calculate_door_dimensions(mounting_type, gap) -> dict
suggest_hardware() -> dict
suggest_drilling() -> dict
to_json() -> str
from_json(json_str) -> FurniturePiece
```

---

### 5. Wizard Command (`fusion_addin/lib/commands/wizard_command.py`)

**Responsibility**: Main UI entry point for guided furniture creation.

**Architecture** (after refactor):
```
User Input (Tabbed Dialog)
    ↓
WizardExecuteHandler.notify()
    ↓
1. Build FurniturePiece model from inputs
    ↓
2. Create cabinet via CabinetGenerator
    cabinet_comp = CabinetGenerator.create_cabinet(cabinet_params)
    ↓
3. Build cabinet_info dict
    cabinet_info = {
        'component': cabinet_comp,
        'width': dimensioni['larghezza'],
        'total_height': dimensioni['altezza'],
        'carcass_height': dimensioni['altezza'] - plinth_height,
        'plinth_height': plinth_height,
        'depth': dimensioni['profondita'],
        'thickness': material_thickness,
        'type': tipo_id
    }
    ↓
4. Compute door configurations
    door_configs = DoorDesigner.compute_door_configs(
        cabinet_info, 
        furniture.elementi['ante']
    )
    ↓
5. Generate doors
    for door_config in door_configs:
        door_comp = DoorGenerator.create_door(door_config)
    ↓
6. Generate drawers (if present)
    for cassetto in furniture.elementi['cassetti']:
        drawer_comp = DrawerGenerator.create_drawer(...)
    ↓
7. Save FurniturePiece as component attribute
    cabinet_comp.attributes.add('FurnitureAI', 'model', furniture.to_json())
```

**Dialog Structure** (5 tabs):
1. **Tipo & Dimensioni**: Category, type, width/height/depth
2. **Elementi**: Panels (sides, top, bottom, back), shelves, dividers
3. **Aperture**: Doors (count, mounting, opening type), drawers
4. **Struttura**: Construction details, joinery, hardware
5. **Materiale**: Material selection, finish, edge banding

---

## Cabinet & Door Generation Flow

### Current Architecture (Unified, Clean)

```
┌─────────────────────┐
│   Wizard Command    │
│  (User Interface)   │
└──────────┬──────────┘
           │
           ├─► 1. Create FurniturePiece Model
           │      (dimensioni, elementi, ferramenta)
           │
           ├─► 2. Generate Cabinet Carcass
           │      ┌─────────────────────┐
           │      │ CabinetGenerator    │
           │      │ ──────────────────  │
           │      │ • Side panels       │
           │      │ • Top/Bottom        │
           │      │ • Back panel        │
           │      │ • Plinth            │
           │      │ • Shelves           │
           │      │ • Dividers          │
           │      │ • Machining holes   │
           │      └──────┬──────────────┘
           │             │
           │             └─► cabinet_comp
           │
           ├─► 3. Build cabinet_info dict
           │      {width, total_height, carcass_height,
           │       plinth_height, depth, thickness, type}
           │
           ├─► 4. Compute Door Configurations
           │      ┌─────────────────────┐
           │      │   DoorDesigner      │
           │      │ ──────────────────  │
           │      │ • Analyze cabinet   │
           │      │ • Analyze door opts │
           │      │ • Compute widths    │
           │      │ • Compute x_offsets │
           │      │ • Return configs    │
           │      └──────┬──────────────┘
           │             │
           │             └─► [door_config_1, door_config_2, ...]
           │
           ├─► 5. Generate Door Geometry (loop)
           │      ┌─────────────────────┐
           │      │   DoorGenerator     │
           │      │ ──────────────────  │
           │      │ • Create geometry   │
           │      │ • Position in 3D    │
           │      │ • Apply gaps        │
           │      │ • Add to cabinet    │
           │      └─────────────────────┘
           │
           └─► 6. Generate Drawers (if any)
                  └─► DrawerGenerator.create_drawer(...)
```

### Responsibilities Matrix

| Component         | Carcass | Door Config | Door Geometry | Door Position | Drawers |
|-------------------|---------|-------------|---------------|---------------|---------|
| CabinetGenerator  | ✅       | ❌           | ❌             | ❌             | ❌       |
| DoorDesigner      | ❌       | ✅           | ❌             | ✅ (x_offset)  | ❌       |
| DoorGenerator     | ❌       | ❌           | ✅             | ✅ (3D coords) | ❌       |
| DrawerGenerator   | ❌       | ❌           | ❌             | ❌             | ✅       |
| Wizard Command    | ❌       | ❌           | ❌             | ❌             | ❌       |

**Wizard acts as orchestrator only** - no business logic for dimensions/positioning.

---

## Command System

### Registered Commands

1. **Wizard Command** (`FAI_Wizard_Native`)
   - Main guided creation dialog
   - Entry: Toolbar button "Wizard Mobili"
   - Handler: `WizardCommand` → `WizardCreatedHandler` → `WizardExecuteHandler`

2. **AI Genera Command** (`AI_Genera`)
   - Natural language furniture generation
   - Entry: Toolbar button "AI Genera"
   - Handler: `AIGeneraCommand`
   - Providers: OpenAI, Anthropic, Azure, Ollama

3. **Cut List Command** (`FAI_Cutlist`)
   - Generate material cut list from selected components
   - Entry: Toolbar button "Distinta Taglio"
   - Handler: `CutlistCommand`

4. **Door Designer Command** (`FAI_DoorDesigner`)
   - Standalone door design with profiles
   - Entry: Toolbar button "Designer Ante"
   - Handler: `DoorDesignerCommand`

5. **Configura IA** (`FAI_ConfiguraIA`)
   - Configure AI providers and settings
   - Entry: Toolbar button "Configura IA"
   - Native dialog with API key management

### Command Registration Flow

```python
# FurnitureAI.py (entry point)
def run(context):
    app = adsk.core.Application.get()
    
    # Initialize managers
    startup_manager = StartupManager(app, addon_path)
    startup_manager.startup()
    
    # Register all commands
    ui_manager = UIManager(app, addon_path)
    ui_manager.create_toolbar()
    # Creates panel + buttons for all commands
```

---

## Data Model

### FurniturePiece Validation Rules

```python
- dimensioni.larghezza: 200-3000 mm
- dimensioni.altezza: 200-3000 mm  
- dimensioni.profondita: 200-800 mm
- elementi.fianchi.spessore: 12-25 mm
- elementi.ante[].spessore: 12-25 mm
- Back panel must be thinner than sides (3-6mm typical)
- Door overlay must be >= gap to avoid collision
- Shelf count must fit within carcass height
```

### Hardware Suggestion Logic

```python
# Auto-suggest based on furniture type and dimensions
suggest_hardware():
    if has_doors:
        # Hinge count: 2 for ≤900mm, 3 for 900-1500mm, 4+ for >1500mm
        cerniere = auto_calculate_hinges(door_height)
    
    if has_drawers:
        # Slide type: ball-bearing full extension for >600mm depth
        guide = select_slide_type(drawer_depth)
    
    if is_base_cabinet:
        # Adjustable feet for base cabinets
        piedini = [{'tipo': 'regolabile', 'altezza': 100}]
```

---

## AI Integration Points

### Current Implementation

**Providers Supported**:
- OpenAI GPT-4 / GPT-3.5
- Anthropic Claude 3 (Opus, Sonnet, Haiku)
- Azure OpenAI (enterprise)
- Ollama (local LLMs: Llama 3, Mistral, etc.)

**Architecture**:
```
AI Genera Command
    ↓
User enters text: "Cucina con 3 ante e 2 cassetti, 80x72x58"
    ↓
PromptBuilder.build_furniture_prompt(user_text)
    ↓
AIProvider.generate(prompt) → JSON response
    ↓
Parse JSON → FurniturePiece
    ↓
Validate → Generate 3D (same flow as wizard)
```

**AI Provider Interface**:
```python
class AIProvider:
    def generate(self, prompt: str) -> str:
        # Returns JSON furniture specification
        pass
    
    def validate_config(self) -> bool:
        # Check API keys, endpoints
        pass
```

**Future AI Extensions** (planned):
- Style transfer: "Make it more modern/traditional"
- Optimization: "Minimize waste" / "Optimize for cost"
- Design variations: "Show me 3 alternatives"
- Automatic hardware selection based on usage patterns
- CNC toolpath optimization

---

## Testing Strategy

### Unit Tests (`fusion_addin/tests/`)

**Philosophy**: Pure calculation tests without Fusion 360 dependency.

```python
# Tests avoid importing adsk modules
# Focus on parameter validation, calculations, data model

test_geometry.py:
    - Dimension calculations
    - Unit conversions (mm to cm)
    - Coordinate transforms

test_joinery.py:
    - Dowel positioning
    - System 32 hole patterns
    - Hinge placement calculations

test_cabinet_orientation.py:
    - Panel orientation (YZ plane extrusion along X)
    - Coordinate system validation
    - Position calculations

test_furniture_model.py:
    - FurniturePiece validation
    - JSON serialization
    - Hardware suggestions

test_door_designer.py: (NEW after refactor)
    - Door configuration calculations
    - Single/double door logic
    - x_offset positioning
```

### Integration Tests (Manual in Fusion 360)

1. **Wizard Full Flow**: Create base cabinet with 2 doors, 1 drawer, 2 shelves
2. **AI Generation**: "Kitchen base cabinet 800x720x580 with 2 doors"
3. **Cut List Export**: Generate and verify cut list accuracy
4. **Multi-Cabinet Layout**: Use anchor system to place 3 adjacent cabinets

### Test Commands
```bash
# Run unit tests (outside Fusion 360)
cd fusion_addin
python -m pytest tests/ -v

# Run specific test
python -m pytest tests/test_door_designer.py -v
```

---

## Future Roadmap

### Short Term (Q1 2026)
- ✅ Unified cabinet/door architecture (this PR)
- [ ] Complete drawer positioning logic for multi-drawer cabinets
- [ ] Implement all door profile types (shaker, raised, glass complete)
- [ ] CNC export (G-code generation from machining patterns)
- [ ] Material library expansion (edge banding, finishes)

### Medium Term (Q2-Q3 2026)
- [ ] IA-powered room layout: "Design a 3m kitchen with storage"
- [ ] Cost estimation with supplier database integration
- [ ] Cut optimization (minimize waste, batch by material)
- [ ] Assembly instructions auto-generation
- [ ] Parametric hardware components (3D hinges, slides, handles)

### Long Term (Q4 2026+)
- [ ] Multi-material support (wood + metal + glass in single piece)
- [ ] Advanced joinery: mortise & tenon, dovetails, finger joints
- [ ] Structural analysis (load calculations, sag prevention)
- [ ] Cloud collaboration (shared furniture libraries)
- [ ] VR/AR preview integration
- [ ] Automated quote generation for manufacturing

---

## Current Implementation Status

### ✅ Production-Ready Features
- Cabinet carcass generation (sides, top, bottom, back, plinth)
- Professional back mounting (flush rabbet, groove, surface)
- Adjustable shelf systems with front setback
- System 32 drilling pattern calculations
- Basic door generation (flat profile)
- Drawer generation with slide integration
- Hardware library and auto-suggestions
- Cut list generation
- AI integration (OpenAI, Anthropic, Ollama)
- Multi-cabinet layout (anchor system)
- Native UI with tabbed wizard dialog

### 🚧 In Progress / Partially Implemented
- Door profile types (shaker, raised, glass - placeholder code exists)
- CNC export (machining patterns calculated, export not implemented)
- Dowel joinery (positioning calculated, geometry not created)
- Advanced drawer configurations (basic working, multi-drawer stacking needs refinement)

### 📋 Planned / Not Yet Started
- Advanced AI features (style transfer, optimization)
- Cost estimation with live supplier data
- Assembly instruction generation
- Cloud collaboration features
- VR/AR preview

---

## Key Design Decisions

### 1. Why Separate DoorDesigner from DoorGenerator?

**Separation of Concerns**:
- **DoorDesigner**: Business logic (how many doors? what widths? where positioned?)
- **DoorGenerator**: Geometry creation (create and position a door at X,Y,Z)

**Benefits**:
- DoorGenerator can be reused for AI-generated designs without wizard
- Business logic can be unit-tested without Fusion 360 dependency
- Easy to extend: new mounting types only touch DoorDesigner
- Future IA modules can call DoorDesigner directly

### 2. Why mm Input/Output with cm Internal?

**Fusion 360 uses cm internally**, but furniture industry uses mm.

**Approach**:
- All public APIs accept/return **mm**
- Internal calculations use **cm** (Fusion native)
- Conversion constant: `MM_TO_CM = 10.0`
- Helper: `_mm_to_cm(value_mm) -> value_cm`

**Example**:
```python
# User inputs 800mm width
width_mm = 800

# Internal calculation
width_cm = width_mm / MM_TO_CM  # 80.0 cm
point = adsk.core.Point3D.create(width_cm, 0, 0)

# Output to user: 800mm
```

### 3. Why Remove Door Creation from CabinetGenerator?

**Problem**: Duplication and tight coupling.
- CabinetGenerator had `_create_door_panel()` method creating doors
- Wizard also calculated door dimensions inline
- Two paths to create doors = confusion and bugs

**Solution**:
- **CabinetGenerator**: Carcass only (single responsibility)
- **DoorDesigner**: Configuration logic
- **DoorGenerator**: Geometry only
- **Wizard**: Orchestrates all three

**Migration**: Old code moved to DoorGenerator, CabinetGenerator cleaned up.

### 4. Why Store FurniturePiece as Component Attribute?

**Traceability and Round-Tripping**:
- User creates furniture via wizard → generates 3D
- User later selects component → can retrieve original parameters
- Enables future "Edit" command to modify existing furniture
- Supports AI: "Modify this cabinet to add a drawer"

**Implementation**:
```python
furniture_json = furniture.to_json()
cabinet_comp.attributes.add('FurnitureAI', 'model', furniture_json)
```

**Future Use**:
```python
attr = cabinet_comp.attributes.itemByName('FurnitureAI', 'model')
if attr:
    furniture = FurniturePiece.from_json(attr.value)
    # Now can modify and regenerate
```

---

## Coordinate System Reference

### Fusion 360 Conventions
- **Origin**: (0, 0, 0) at back-left-bottom of cabinet
- **X-axis**: Width (left to right, positive = right)
- **Y-axis**: Depth (back to front, positive = front)
- **Z-axis**: Height (bottom to top, positive = up)

### Cabinet Coordinate System
```
        Z (Height)
        ↑
        |     Y (Depth, front)
        |    ↗
        |   /
        |  /
        | /
        |/________→ X (Width)
       (0,0,0)
    Back-Left-Bottom
```

### Key Reference Points
```python
# Cabinet dimensions (example 800x720x580, plinth 100)
origin = (0, 0, 0)  # Back-left-bottom

# Carcass corners
back_left_bottom = (0, 0, plinth_height)  # (0, 0, 100)
back_right_bottom = (width, 0, plinth_height)  # (800, 0, 100)
front_left_top = (0, depth, height)  # (0, 580, 720)
front_right_top = (width, depth, height)  # (800, 580, 720)

# Panel references
left_side_panel_plane = YZ plane at X=0, extrude +X direction
right_side_panel_plane = YZ plane at X=(width - thickness), extrude +X
top_panel_plane = YZ plane, extrude along X (internal width)
bottom_panel_plane = YZ plane at Z=plinth_height, extrude along X
back_panel_plane = YZ plane at Y=back_inset, extrude along X

# Door positioning (full overlay)
door_y = depth - door_thickness  # Front of cabinet
door_z = plinth_height + bottom_gap  # Base on top of plinth
door_x = x_offset + side_gap  # Offset from left + gap
```

---

## Logging and Debugging

### Log Levels
```python
logger.info("✅ Success message")
logger.warning("⚠️ Warning message")  
logger.error("❌ Error message")
```

### Key Log Points (Defensive Logging)
```python
# Cabinet generation
logger.info(f"🏗️ Creating cabinet: {width}x{height}x{depth} mm")
logger.info(f"📐 Carcass height: {carcass_height}, Plinth: {plinth_height}")

# Door configuration
logger.info(f"🚪 Computing door configs: {n_doors} doors")
logger.info(f"📏 Door dimensions: {door_width}x{door_height} at x_offset={x_offset}")

# Positioning
logger.info(f"📍 Door position: X={x_pos}, Y={y_pos}, Z={z_pos} cm")

# Completion
logger.info(f"✅ Cabinet component created: {cabinet_comp.name}")
logger.info(f"✅ Door {i+1} created: {door_comp.name}")
```

### Debug Output Locations
- **Console**: Fusion 360 Text Commands window
- **Log File**: `%TEMP%/FurnitureAI.log` (Windows) or `/tmp/FurnitureAI.log` (Mac)
- **UI Messages**: `ui.messageBox()` for critical errors only

---

## Contributing Guidelines

### Code Style
- Python 3.7+ (Fusion 360 Python environment)
- 4-space indentation
- Type hints encouraged: `def create_door(width: int, height: int) -> Component:`
- Docstrings for public methods
- Italian for domain terms (anta, fianco, ripiano), English for technical terms

### Adding New Features

**Example: Adding a New Door Profile**

1. Create profile module: `fusion_addin/lib/doors/profile_new.py`
```python
def create_new_profile_door(design, params):
    # Implementation
    pass
```

2. Register in DoorDesigner:
```python
# door_designer.py
elif profile_type == 'new_profile':
    from .profile_new import create_new_profile_door
    return create_new_profile_door(self.design, params)
```

3. Add to UI dropdown (wizard_command.py)
4. Add unit tests (tests/test_door_profiles.py)
5. Update documentation (this file + changelog.md)

### Git Workflow
1. Branch from `main`: `git checkout -b feature/new-profile`
2. Make changes
3. Test manually in Fusion 360
4. Run unit tests: `python -m pytest tests/`
5. Commit: `git commit -m "feat: add shaker door profile"`
6. Push and create PR

---

## Troubleshooting

### Common Issues

**1. "Component is null" Error**
- **Cause**: Cabinet not created before trying to add doors
- **Fix**: Ensure `cabinet_comp = cabinet_generator.create_cabinet()` succeeds before door generation

**2. Doors Not Positioned Correctly (Z-axis)**
- **Cause**: Plinth height not passed to door generator
- **Fix**: Verify `cabinet_plinth_height` param includes plinth if `has_plinth=True`

**3. Door Width Incorrect**
- **Cause**: Gaps not applied or applied twice
- **Fix**: DoorDesigner computes nominal width, DoorGenerator applies gaps internally

**4. "Cannot find module" Import Error**
- **Cause**: Fusion 360 Python path not set correctly
- **Fix**: Verify `addon_path` in FurnitureAI.py points to repo root

**5. AI Generation Returns Invalid JSON**
- **Cause**: LLM hallucinated invalid furniture spec
- **Fix**: Validate with `furniture.validate()` before 3D generation, show errors to user

---

## Glossary

### Italian Furniture Terms
- **Anta**: Door
- **Fianco**: Side panel
- **Top**: Top panel
- **Fondo**: Bottom panel
- **Schienale**: Back panel
- **Zoccolo**: Plinth / toe kick
- **Ripiano**: Shelf
- **Divisorio**: Vertical divider
- **Cassetto**: Drawer
- **Cerniera**: Hinge
- **Guida**: Slide (drawer slide)
- **Maniglia**: Handle
- **Piedino**: Foot (adjustable foot)
- **Carcassa**: Carcass (box structure)

### Technical Terms
- **System 32**: European standard 32mm drilling pattern for adjustable shelves/hinges
- **Rabbet Joint**: L-shaped groove cut into edge (for back panel)
- **Groove**: Slot cut into face (for back panel)
- **Overlay**: Door extends past cabinet front edge (typical 18mm)
- **Flush Mount**: Door is flush with cabinet face
- **Cup Hole**: 35mm diameter hole for European hinge cup
- **K Dimension**: Distance from door edge to hinge cup center (typically 21.5mm for Blum)

---

## References

### External Documentation
- [Fusion 360 API Reference](https://help.autodesk.com/view/fusion360/ENU/?guid=GUID-A92A4B10-3781-4925-94C6-47DA85A4F65A)
- [Blum Hinge Specifications](https://www.blum.com/us/en/products/hinges/)
- [System 32 Standard](https://en.wikipedia.org/wiki/32_mm_cabinetmaking_system)

### Internal Documentation
- `docs/CABINET_PARAMETERS.md`: Detailed parameter reference for CabinetGenerator
- `docs/ai_configuration.md`: AI provider setup and configuration
- `docs/changelog.md`: Chronological change history

---

**Document Version**: 1.0  
**Author**: FurnitureAI Development Team  
**License**: See LICENSE file in repository root
