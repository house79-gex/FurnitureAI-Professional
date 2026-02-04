#!/bin/bash
# FurnitureAI Professional - Unix Installation Script

echo "🚀 FurnitureAI Professional v3.0 - Installer"
echo "============================================="
echo ""

# Detect OS
OS_TYPE=$(uname -s)
case "$OS_TYPE" in
    Darwin*)
        echo "✓ macOS detected"
        ADDINS_PATH="$HOME/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns"
        ;;
    Linux*)
        echo "✓ Linux detected"
        ADDINS_PATH="$HOME/.config/Autodesk/Autodesk Fusion 360/API/AddIns"
        ;;
    *)
        echo "❌ Unsupported OS: $OS_TYPE"
        exit 1
        ;;
esac

echo "📁 AddIns path: $ADDINS_PATH"
echo ""

# Check if Fusion 360 is installed
if [ ! -d "$ADDINS_PATH" ]; then
    echo "⚠️  Fusion 360 AddIns directory not found"
    echo "Creating directory..."
    mkdir -p "$ADDINS_PATH"
fi

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ADDON_SOURCE="$SCRIPT_DIR/.."
ADDON_DEST="$ADDINS_PATH/FurnitureAI"

echo "📦 Installing addon..."

# Remove old installation if exists
if [ -d "$ADDON_DEST" ]; then
    echo "🗑️  Removing old installation..."
    rm -rf "$ADDON_DEST"
fi

# Copy addon
echo "📋 Copying files..."
cp -R "$ADDON_SOURCE" "$ADDON_DEST"

# Set permissions
echo "🔐 Setting permissions..."
chmod -R 755 "$ADDON_DEST"

echo ""
echo "✅ Installation completed successfully!"
echo ""
echo "Next steps:"
echo "1. Launch Fusion 360"
echo "2. Go to TOOLS > ADD-INS > Scripts and Add-Ins"
echo "3. Select 'FurnitureAI' and click 'Run'"
echo ""
echo "For AI features, install:"
echo "- LM Studio (https://lmstudio.ai) for LLM"
echo "- Ollama (https://ollama.ai) for vision"
echo ""
echo "📚 Documentation: $ADDON_DEST/docs/"
echo ""
