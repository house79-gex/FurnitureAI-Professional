# 🪑 FurnitureAI Professional

**Intelligent furniture design for Fusion 360 with multimodal AI**

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Fusion 360](https://img.shields.io/badge/Fusion%20360-Compatible-orange)](https://www.autodesk.com/products/fusion-360)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/)

[🇮🇹 Italiano](docs/README_IT.md) | [🇬🇧 English](docs/README_EN.md) | [🇩🇪 Deutsch](docs/README_DE.md) | [🇫🇷 Français](docs/README_FR.md)

---

## 🌟 Features

### 🏗️ Core (based on WoodWorkingWizard)
- ✅ **Perfect geometry**: Rectangular panels, no distortion
- ✅ **Cabinets**: Base/wall/tall with shelves/drawers
- ✅ **Doors**: Single/double with soft-close
- ✅ **Drawers**: Full-extension with grooves
- ✅ **Cut list**: Automatic with optimization
- ✅ **Nesting**: Panel layout optimizer

### 🔩 Hardware & Joinery (NEW)
- ✅ **Hardware catalog**: Blum, Hettich, Salice, Hafele
- ✅ **AI selector**: Automatic hardware selection by description
- ✅ **32mm system**: Automatic shelf pin holes
- ✅ **Dowel joints**: Ø8 automatic spinatura
- ✅ **Cam locks**: Flat-pack connectors
- ✅ **Grooves**: Back panel grooves

### 🚪 Door Designer (NEW)
- ✅ **Flat**: Simple smooth door
- ✅ **Shaker**: Frame + recessed panel
- ✅ **Raised panel**: Beveled center with loft
- ✅ **Glass frame**: Wood frame + glass insert
- ✅ **Custom DXF**: Import custom profiles

### 🎨 Materials (NEW)
- ✅ **Local library**: Wood/laminates/lacquers
- ✅ **Online scraper**: Egger/Cleaf/Abet catalogs
- ✅ **From photo**: AI extracts material from image
- ✅ **Auto-apply**: Material manager

### 🤖 AI Multimodal (NEW)
- ✅ **LLM (Llama 3.1 8B)**: Text → layout/hardware/parameters
- ✅ **Vision (LLaVA 13B)**: Floor plan → layout / Photo → style
- ✅ **Speech (Whisper Large)**: Voice commands
- ✅ **Local/Cloud**: LM Studio, Ollama, or cloud API

### 🌍 Internationalization
- ✅ **Auto-detect**: Follows Fusion 360 language
- ✅ **Languages**: IT, EN, DE, FR, ES (+ more coming)
- ✅ **Easy translation**: JSON-based system

---

## 🚀 Quick Start

### Installation

#### Method 1: Automatic (recommended)
```bash
# Download installer
curl -O https://raw.githubusercontent.com/house79-gex/FurnitureAI-Professional/main/scripts/install.sh

# Run (macOS/Linux)
bash install.sh

# Or Windows
install.bat
