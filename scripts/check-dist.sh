#!/bin/bash
# Pre-distribution checklist and validation script

set -e

echo "========================================="
echo "GNOME Text Extractor - Distribution Check"
echo "========================================="
echo ""

ERRORS=0
WARNINGS=0

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

error() {
    echo -e "${RED}✗ $1${NC}"
    ERRORS=$((ERRORS + 1))
}

success() {
    echo -e "${GREEN}✓ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
    WARNINGS=$((WARNINGS + 1))
}

# Check required files exist
echo "[1/8] Checking required files..."
REQUIRED_FILES=(
    "README.md"
    "LICENSE"
    "CHANGELOG.md"
    "CONTRIBUTING.md"
    "pyproject.toml"
    "MANIFEST.in"
    "text_extractor/__init__.py"
    "text_extractor/main.py"
    "text_extractor/backend.py"
    "text_extractor/desktop.py"
    "install/install.sh"
    "install/text-extractor.desktop"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        success "$file"
    else
        error "Missing: $file"
    fi
done

# Check version consistency
echo ""
echo "[2/8] Checking version consistency..."
VERSION_PYPROJECT=$(grep '^version = ' pyproject.toml | cut -d'"' -f2)
VERSION_INIT=$(grep '__version__' text_extractor/__init__.py | cut -d'"' -f2)

if [ "$VERSION_PYPROJECT" == "$VERSION_INIT" ]; then
    success "Version $VERSION_PYPROJECT is consistent"
else
    error "Version mismatch: pyproject.toml ($VERSION_PYPROJECT) vs __init__.py ($VERSION_INIT)"
fi

# Check Python syntax
echo ""
echo "[3/8] Checking Python syntax..."
if command -v python3 &> /dev/null; then
    if python3 -m py_compile text_extractor/*.py 2>/dev/null; then
        success "Python syntax valid"
    else
        error "Python syntax errors found"
    fi
else
    warning "Python3 not found, skipping syntax check"
fi

# Check for TODO/FIXME comments
echo ""
echo "[4/8] Checking for TODO/FIXME comments..."
TODO_COUNT=$(grep -r "TODO\|FIXME" text_extractor/ --include="*.py" | wc -l || true)
if [ "$TODO_COUNT" -gt 0 ]; then
    warning "Found $TODO_COUNT TODO/FIXME comments in code"
else
    success "No TODO/FIXME comments"
fi

# Check dependencies are installable
echo ""
echo "[5/8] Checking dependencies..."
if command -v uv &> /dev/null; then
    if uv sync --no-install-project 2>&1 | grep -q "error"; then
        error "Dependency resolution failed"
    else
        success "Dependencies can be resolved"
    fi
else
    warning "uv not found, skipping dependency check"
fi

# Check documentation completeness
echo ""
echo "[6/8] Checking documentation..."

if grep -q "Installation" README.md && grep -q "Usage" README.md; then
    success "README.md contains Installation and Usage sections"
else
    error "README.md missing Installation or Usage sections"
fi

if grep -q "## \[" CHANGELOG.md; then
    success "CHANGELOG.md formatted correctly"
else
    warning "CHANGELOG.md may not be formatted correctly"
fi

# Check for sensitive data
echo ""
echo "[7/8] Checking for sensitive data..."
SENSITIVE_PATTERNS=("password" "secret" "api_key" "token" "private")
FOUND_SENSITIVE=false

for pattern in "${SENSITIVE_PATTERNS[@]}"; do
    if grep -ri "$pattern" text_extractor/ --include="*.py" | grep -v "# " | grep -v "def " > /dev/null; then
        warning "Found potential sensitive pattern: $pattern"
        FOUND_SENSITIVE=true
    fi
done

if [ "$FOUND_SENSITIVE" = false ]; then
    success "No obvious sensitive data found"
fi

# Test import
echo ""
echo "[8/8] Testing package import..."
if python3 -c "import text_extractor; print(f'Version: {text_extractor.__version__}')" 2>/dev/null; then
    success "Package imports successfully"
else
    error "Package import failed"
fi

# Summary
echo ""
echo "========================================="
echo "Summary"
echo "========================================="
if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✓ All checks passed! Ready for distribution.${NC}"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}⚠ $WARNINGS warning(s) found. Review before distribution.${NC}"
    exit 0
else
    echo -e "${RED}✗ $ERRORS error(s) and $WARNINGS warning(s) found.${NC}"
    echo "Please fix errors before distribution."
    exit 1
fi
