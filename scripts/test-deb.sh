#!/bin/bash
# Test the built .deb package in a clean environment

set -e

echo "========================================="
echo "Testing .deb Package"
echo "========================================="
echo ""

DEB_FILE=$(ls dist/deb/*.deb 2>/dev/null | head -1)

if [ ! -f "$DEB_FILE" ]; then
    echo "ERROR: No .deb package found in dist/deb/"
    echo "Run ./scripts/build-deb.sh first"
    exit 1
fi

echo "Testing package: $DEB_FILE"
echo ""

# Test 1: Validate package structure
echo "[1/5] Validating package structure..."
if lintian "$DEB_FILE" 2>&1 | grep -q "E:"; then
    echo "⚠ Package has errors (see lintian output above)"
else
    echo "✓ Package structure valid"
fi

# Test 2: Check package info
echo ""
echo "[2/5] Package information:"
dpkg-deb --info "$DEB_FILE"

# Test 3: Check files
echo ""
echo "[3/5] Package contents:"
dpkg-deb --contents "$DEB_FILE"

# Test 4: Check dependencies
echo ""
echo "[4/5] Checking dependencies..."
DEPS=$(dpkg-deb --field "$DEB_FILE" Depends | tr ',' '\n')
echo "$DEPS"

# Test 5: Offer to install
echo ""
echo "[5/5] Installation test"
echo ""
read -p "Install package for testing? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Installing..."
    sudo dpkg -i "$DEB_FILE" || true
    echo ""
    echo "Fixing dependencies..."
    sudo apt install -f
    echo ""
    echo "✓ Package installed"
    echo ""
    echo "Test the application:"
    echo "  text-extractor"
    echo "  # or find it in GNOME application menu"
    echo ""
    read -p "Uninstall after testing? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        sudo apt remove gnome-text-extractor
        echo "✓ Package removed"
    fi
else
    echo "Skipped installation test"
fi

echo ""
echo "========================================="
echo "✓ Testing complete"
echo "========================================="
