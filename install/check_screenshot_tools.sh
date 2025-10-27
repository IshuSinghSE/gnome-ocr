#!/bin/bash
# Check for screenshot tool availability and provide installation guidance

echo "========================================="
echo "Screenshot Tool Check"
echo "========================================="
echo ""

FOUND_TOOLS=()

if command -v gnome-screenshot &> /dev/null; then
    FOUND_TOOLS+=("gnome-screenshot")
    echo "✓ gnome-screenshot found"
fi

if command -v flameshot &> /dev/null; then
    FOUND_TOOLS+=("flameshot")
    echo "✓ flameshot found"
fi

if command -v spectacle &> /dev/null; then
    FOUND_TOOLS+=("spectacle")
    echo "✓ spectacle found"
fi

if [ ${#FOUND_TOOLS[@]} -eq 0 ]; then
    echo "✗ No screenshot tools found!"
    echo ""
    echo "Please install one of the following:"
    echo ""
    echo "For GNOME users:"
    echo "  sudo apt install gnome-screenshot"
    echo ""
    echo "For a cross-desktop alternative:"
    echo "  sudo apt install flameshot"
    echo ""
    echo "For KDE users:"
    echo "  sudo apt install spectacle"
    echo ""
    echo "After installation, you can run:"
    echo "  python3 -m text_extractor.main"
    echo ""
    echo "Or test with an existing image:"
    echo "  python3 -m text_extractor.main path/to/image.png"
    exit 1
else
    echo ""
    echo "========================================="
    echo "✓ Screenshot tools available: ${FOUND_TOOLS[*]}"
    echo "========================================="
    echo ""
    echo "You can now run:"
    echo "  python3 -m text_extractor.main"
fi
