#!/bin/bash
# Build .deb package for Debian/Ubuntu distribution

set -e

echo "========================================="
echo "GNOME Text Extractor - Build .deb Package"
echo "========================================="
echo ""

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "ERROR: Must run from project root directory"
    exit 1
fi

# Check for required build tools
echo "[1/6] Checking build dependencies..."
MISSING_TOOLS=()

if ! command -v dpkg-buildpackage &> /dev/null; then
    MISSING_TOOLS+=("dpkg-dev")
fi

if ! command -v dh &> /dev/null; then
    MISSING_TOOLS+=("debhelper")
fi

if ! command -v dh_python3 &> /dev/null; then
    MISSING_TOOLS+=("dh-python")
fi

if [ ${#MISSING_TOOLS[@]} -ne 0 ]; then
    echo "⚠ Missing build tools: ${MISSING_TOOLS[*]}"
    echo ""
    echo "Install them with:"
    echo "  sudo apt install build-essential debhelper dh-python python3-all python3-setuptools"
    echo ""
    read -p "Install automatically? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        sudo apt install -y build-essential debhelper dh-python python3-all python3-setuptools python3-pip
    else
        exit 1
    fi
fi

echo "✓ Build tools available"

# Make debian/rules executable
echo ""
echo "[2/6] Preparing debian files..."
chmod +x debian/rules
echo "✓ Debian files prepared"

# Clean previous builds
echo ""
echo "[3/6] Cleaning previous builds..."
rm -rf debian/.debhelper debian/gnome-text-extractor debian/files debian/*.substvars
rm -f ../*.deb ../*.changes ../*.buildinfo ../*.dsc ../*.tar.*
echo "✓ Cleaned"

# Build the package
echo ""
echo "[4/6] Building .deb package..."
echo "This may take a few minutes..."
dpkg-buildpackage -us -uc -b

echo "✓ Package built"

# Move .deb to dist directory
echo ""
echo "[5/6] Organizing output..."
mkdir -p dist/deb
mv ../*.deb dist/deb/ 2>/dev/null || true
mv ../*.changes dist/deb/ 2>/dev/null || true
mv ../*.buildinfo dist/deb/ 2>/dev/null || true

echo "✓ Package moved to dist/deb/"

# Show package info
echo ""
echo "[6/6] Package information:"
DEB_FILE=$(ls dist/deb/*.deb | head -1)
if [ -f "$DEB_FILE" ]; then
    dpkg-deb --info "$DEB_FILE"
    echo ""
    echo "Package contents:"
    dpkg-deb --contents "$DEB_FILE" | head -20
fi

echo ""
echo "========================================="
echo "✓ Build complete!"
echo "========================================="
echo ""
echo "Package location: $DEB_FILE"
echo ""
echo "To install locally:"
echo "  sudo dpkg -i $DEB_FILE"
echo "  sudo apt install -f  # Fix dependencies if needed"
echo ""
echo "To test the package:"
echo "  dpkg-deb --info $DEB_FILE"
echo "  dpkg-deb --contents $DEB_FILE"
echo ""
echo "To upload to PPA (Ubuntu):"
echo "  1. Sign up at https://launchpad.net"
echo "  2. Create a PPA"
echo "  3. Build source package: dpkg-buildpackage -S"
echo "  4. Upload: dput ppa:yourname/yourppa ../*.changes"
echo ""
echo "For Debian packages:"
echo "  See: https://www.debian.org/doc/manuals/maint-guide/"
echo ""
