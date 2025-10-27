#!/bin/bash
# Build distribution packages

set -e

echo "========================================="
echo "GNOME Text Extractor - Build Distribution"
echo "========================================="
echo ""

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "ERROR: Must run from project root directory"
    exit 1
fi

# Clean previous builds
echo "[1/5] Cleaning previous builds..."
rm -rf build/ dist/ *.egg-info/
echo "✓ Cleaned"

# Install build tools
echo ""
echo "[2/5] Installing build tools..."
if command -v uv &> /dev/null; then
    uv pip install build twine
else
    pip install build twine
fi
echo "✓ Build tools installed"

# Build source distribution and wheel
echo ""
echo "[3/5] Building distribution packages..."
python3 -m build
echo "✓ Built packages"

# List built packages
echo ""
echo "[4/5] Built packages:"
ls -lh dist/

# Validate packages
echo ""
echo "[5/5] Validating packages..."
python3 -m twine check dist/*
echo "✓ Packages validated"

echo ""
echo "========================================="
echo "✓ Build complete!"
echo "========================================="
echo ""
echo "Distribution packages are in: dist/"
echo ""
echo "To test the package locally:"
echo "  pip install dist/gnome_text_extractor-*.whl"
echo ""
echo "To upload to PyPI (after testing):"
echo "  python3 -m twine upload dist/*"
echo ""
echo "To create a GitHub release:"
echo "  1. Commit all changes"
echo "  2. Create and push a tag: git tag v1.0.0 && git push origin v1.0.0"
echo "  3. GitHub Actions will automatically create a release"
echo ""
