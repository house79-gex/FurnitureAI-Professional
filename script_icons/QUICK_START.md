# 🚀 Quick Start Guide - Icon Generation System

## Overview
This system generates **47 professional icons** in **4 resolutions** (16×16, 32×32, 64×64, 128×128px) for the FurnitureAI Professional application.

## Installation

```bash
cd script_icons
pip install -r requirements.txt
```

## Generate All Icons

```bash
python generate_all_simple.py
```

**What you get:**
- ✅ 188 SVG files in `output/svg/`
- ✅ 188 PNG files in `output/png/` (if svglib+reportlab installed)
- ✅ Interactive preview in `output/preview.html`
- ✅ Complete metadata in `output/metadata.json`

## Expected Output

```
============================================================
🎨 FurnitureAI Icon Generator
============================================================

📂 Design Panel (4 icons)
  ✓ FAI_LayoutIA (4/4 sizes)
  ✓ FAI_GeneraIA (4/4 sizes)
  ✓ FAI_Wizard (4/4 sizes)
  ✓ FAI_Template (4/4 sizes)

📂 Componenti Panel (8 icons)
  ✓ FAI_Designer (4/4 sizes)
  ✓ FAI_Anta (4/4 sizes)
  ... (all 8 icons)

... (all 9 panels)

============================================================
✅ Generation Complete!
============================================================
SVG files: 188
PNG files: 188
Time: 0.2 seconds
Output: output/svg/ and output/png/
============================================================
```

## File Structure

```
output/
├── svg/
│   ├── FAI_LayoutIA_16.svg      # 16×16px
│   ├── FAI_LayoutIA_32.svg      # 32×32px
│   ├── FAI_LayoutIA_64.svg      # 64×64px
│   ├── FAI_LayoutIA_128.svg     # 128×128px
│   └── ... (all 188 SVG files)
│
├── png/
│   ├── FAI_LayoutIA_16.png
│   ├── FAI_LayoutIA_32.png
│   ├── FAI_LayoutIA_64.png
│   ├── FAI_LayoutIA_128.png
│   └── ... (all 188 PNG files)
│
├── preview.html     # Open this to view all icons!
└── metadata.json    # Complete generation metadata
```

## View Icons

Open `output/preview.html` in your browser to:
- 🔍 Search icons by name
- 📏 Switch between sizes (16/32/64/128)
- 📊 See generation statistics
- 🎨 Preview all icons interactively

## All 47 Icons

### Design Panel (4)
- FAI_LayoutIA, FAI_GeneraIA, FAI_Wizard, FAI_Template

### Components Panel (8)
- FAI_Designer, FAI_Anta, FAI_Cassetto, FAI_Ripiano
- FAI_Schienale, FAI_Cornice, FAI_Cappello, FAI_Zoccolo

### Edita Panel (7)
- FAI_EditaStruttura, FAI_EditaLayout, FAI_EditaInterno
- FAI_EditaAperture, FAI_ApplicaMateriali, FAI_DuplicaMobile, FAI_ModSolido

### Hardware Panel (3)
- FAI_Ferramenta, FAI_Accessori, FAI_Cataloghi

### Lavorazioni Panel (3)
- FAI_Forature, FAI_Giunzioni, FAI_Scanalature

### Qualità Panel (3)
- FAI_Verifica, FAI_Render, FAI_Viewer

### Produzione Panel (7)
- FAI_Preventivo, FAI_DistintaMateriali, FAI_ListaTaglio
- FAI_Nesting, FAI_Disegni2D, FAI_Etichette, FAI_Esporta

### Guida & Info Panel (7)
- FAI_GuidaRapida, FAI_TutorialVideo, FAI_EsempiProgetti
- FAI_DocumentazioneAPI, FAI_Community, FAI_CheckUpdate, FAI_About

### Impostazioni Panel (5)
- FAI_ConfiguraIA, FAI_Preferenze, FAI_LibreriaMateriali
- FAI_CataloghiMateriali, FAI_ListiniPrezzi

## Windows Compatibility

The system includes a Windows-compatible PNG converter that uses `svglib` and `reportlab` instead of `cairosvg` (which requires Cairo DLLs that can be problematic on Windows).

**Manual PNG conversion:**
```bash
python convert_svg_to_png_windows.py output/svg output/png
```

## Troubleshooting

**Q: PNG files not generated?**
A: Install PNG conversion libraries:
```bash
pip install svglib reportlab
```

**Q: Icons look wrong?**
A: Make sure you have the latest version of all generators. Re-run generation:
```bash
python generate_all_simple.py
```

**Q: Need to regenerate specific icons?**
A: Delete the output folder and run again:
```bash
rm -rf output
python generate_all_simple.py
```

## Next Steps

1. Open `output/preview.html` to view all icons
2. Use SVG files directly in your application
3. Convert SVGs to PNGs if needed (Windows-compatible)
4. Check `output/metadata.json` for complete icon information

---

**✨ System Status:** ✅ All 188 files generated successfully
**⏱️ Generation Time:** ~0.2 seconds
**📦 Total Size:** Minimal (SVG is vector-based)
