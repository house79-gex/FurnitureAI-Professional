# 🪑 FurnitureAI Professional

**Intelligent furniture design for Fusion 360 with multimodal AI**

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Fusion 360](https://img.shields.io/badge/Fusion%20360-Compatible-orange)](https://www.autodesk.com/products/fusion-360)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/)

[🇮🇹 Italiano](docs/README_IT.md) | [🇬🇧 English](docs/README_EN.md) | [🇩🇪 Deutsch](docs/README_DE.md) | [🇫🇷 Français](docs/README_FR.md)

---

## 🌟 Features

### 🏗️ Core
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

# Or Windows (PowerShell)
.\install.bat
```

#### Method 2: Manual Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/house79-gex/FurnitureAI-Professional.git
   ```

2. Copy to Fusion 360 add-ins folder:
   - **Windows**: `%AppData%\Autodesk\Autodesk Fusion 360\API\AddIns\`
   - **macOS**: `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns/`

3. Restart Fusion 360

4. Enable the add-in:
   - Open Fusion 360
   - Go to **Tools** → **Add-Ins** → **Scripts and Add-Ins**
   - Select **FurnitureAI** and click **Run**

---

## 📖 Usage

### Creating Your First Cabinet

1. Launch the **Wizard** from the FurnitureAI toolbar
2. Select cabinet type (Base/Wall/Tall)
3. Enter dimensions (width, height, depth)
4. Choose options (shelves, drawers, doors)
5. Click **Generate** - your cabinet is ready!

### AI-Powered Design

- **Text to Model**: Describe your furniture in natural language
- **Voice Commands**: Use speech to create and modify designs
- **Vision Analysis**: Upload floor plans or photos for automatic layout

### Hardware Integration

- Browse the hardware catalog
- Let AI select appropriate hinges and slides
- Automatic drilling patterns for 32mm system

---

## 🗺️ Roadmap

### Current Focus (2026)
- ✅ Complete core functionality
- ✅ AI multimodal integration
- ✅ Professional hardware catalog
- 🔄 Advanced cut list optimization
- 🔄 CNC export capabilities

### Future Enhancements
- [ ] Photorealistic rendering integration
- [ ] Cloud project synchronization
- [ ] AR preview support
- [ ] Multi-agent AI orchestration
- [ ] Pricing and BOM management

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup
```bash
# Clone repository
git clone https://github.com/house79-gex/FurnitureAI-Professional.git

# Navigate to repository
cd FurnitureAI-Professional

# The add-in uses Python libraries available in Fusion 360
# No additional dependencies need to be installed
```

---

## 📄 License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

---

## 💬 Support

- **Documentation**: [Full Documentation](docs/)
- **Issues**: [GitHub Issues](https://github.com/house79-gex/FurnitureAI-Professional/issues)
- **Discussions**: [GitHub Discussions](https://github.com/house79-gex/FurnitureAI-Professional/discussions)

---

**FurnitureAI Professional** - A complete, independent solution for professional furniture design in Fusion 360.
