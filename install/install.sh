#!/bin/bash
# Installation script for GNOME Text Extractor

set -e

echo "========================================="
echo "GNOME Text Extractor - Installation"
echo "========================================="
echo ""

# Check if running from project root
if [ ! -d "text_extractor" ]; then
    echo "ERROR: Please run this script from the project root directory"
    exit 1
fi

# Check for required system dependencies
echo "[1/5] Checking system dependencies..."

MISSING_DEPS=()
MISSING_SCREENSHOT=true

# Check for screenshot tools
if command -v gnome-screenshot &> /dev/null; then
    echo "✓ gnome-screenshot found"
    MISSING_SCREENSHOT=false
elif command -v flameshot &> /dev/null; then
    echo "✓ flameshot found"
    MISSING_SCREENSHOT=false
elif command -v spectacle &> /dev/null; then
    echo "✓ spectacle found"
    MISSING_SCREENSHOT=false
else
    echo "✗ No screenshot tool found (gnome-screenshot, flameshot, or spectacle)"
    echo "  Note: You can still test with existing images: python3 -m text_extractor.main image.png"
fi

if ! command -v notify-send &> /dev/null; then
    MISSING_DEPS+=("libnotify-bin")
fi

if [ ${#MISSING_DEPS[@]} -ne 0 ]; then
    echo "⚠ Missing optional dependencies: ${MISSING_DEPS[*]}"
    echo ""
    echo "Install them with:"
    echo "  sudo apt install ${MISSING_DEPS[*]}"
    echo ""
    read -p "Continue installation anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

if [ "$MISSING_SCREENSHOT" = true ]; then
    echo ""
    echo "⚠ WARNING: No screenshot tool installed!"
    echo "  Install one with:"
    echo "    sudo apt install gnome-screenshot  # For GNOME"
    echo "    sudo apt install flameshot         # Cross-desktop"
    echo "    sudo apt install spectacle         # For KDE"
    echo ""
    read -p "Continue installation anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "✓ System dependencies check complete"

# Check for Python 3
echo ""
echo "[2/5] Checking Python..."

if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is required but not found"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✓ Found Python $PYTHON_VERSION"

# Install Python dependencies using uv
echo ""
echo "[3/5] Installing Python dependencies..."

if command -v uv &> /dev/null; then
    echo "Using uv for dependency management..."
    uv sync
else
    echo "uv not found, falling back to pip..."
    python3 -m pip install -e .
fi

echo "✓ Python dependencies installed"

# Install desktop entry
echo ""
echo "[4/5] Installing desktop entry..."

DESKTOP_DIR="$HOME/.local/share/applications"
mkdir -p "$DESKTOP_DIR"

cp install/text-extractor.desktop "$DESKTOP_DIR/"
chmod +x "$DESKTOP_DIR/text-extractor.desktop"

echo "✓ Desktop entry installed to $DESKTOP_DIR"

# Update desktop database
echo ""
echo "[5/5] Updating desktop database..."

if command -v update-desktop-database &> /dev/null; then
    update-desktop-database "$DESKTOP_DIR"
    echo "✓ Desktop database updated"
else
    echo "⚠ update-desktop-database not found, skipping"
fi

# Done
echo ""
echo "========================================="
echo "✓ Installation complete!"
echo "========================================="
echo ""
echo "You can now:"
echo "  1. Find 'Text Extractor' in your application menu"
echo "  2. Or run from terminal: python3 -m text_extractor.main"
echo ""
echo "To set up a keyboard shortcut:"
echo "  1. Open Settings → Keyboard → Keyboard Shortcuts"
echo "  2. Scroll to 'Custom Shortcuts'"
echo "  3. Click '+' to add a new shortcut"
echo "  4. Name: 'Text Extractor'"
echo "  5. Command: python3 -m text_extractor.main"
echo "  6. Set your preferred shortcut (e.g., Super+Shift+T)"
echo ""
