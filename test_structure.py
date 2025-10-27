"""
Quick test to verify package structure and imports work correctly.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print("Testing GNOME Text Extractor package structure...")
print("=" * 50)

# Test 1: Import main package
try:
    import text_extractor
    print("✓ text_extractor package imports successfully")
    print(f"  Version: {text_extractor.__version__}")
except Exception as e:
    print(f"✗ Failed to import text_extractor: {e}")
    sys.exit(1)

# Test 2: Import backend module
try:
    from text_extractor import backend
    print("✓ text_extractor.backend module imports successfully")
    
    # Check functions exist
    assert hasattr(backend, 'get_clean_image')
    assert hasattr(backend, 'extract_text_from_image')
    assert hasattr(backend, 'extract_text_conf')
    print("  - get_clean_image() ✓")
    print("  - extract_text_from_image() ✓")
    print("  - extract_text_conf() ✓")
except Exception as e:
    print(f"✗ Failed to import backend: {e}")
    sys.exit(1)

# Test 3: Import desktop module
try:
    from text_extractor import desktop
    print("✓ text_extractor.desktop module imports successfully")
    
    # Check functions exist
    assert hasattr(desktop, 'capture_screenshot')
    assert hasattr(desktop, 'send_notification')
    assert hasattr(desktop, 'copy_to_clipboard')
    print("  - capture_screenshot() ✓")
    print("  - send_notification() ✓")
    print("  - copy_to_clipboard() ✓")
except Exception as e:
    print(f"✗ Failed to import desktop: {e}")
    sys.exit(1)

# Test 4: Import main module
try:
    from text_extractor import main
    print("✓ text_extractor.main module imports successfully")
    
    # Check main function exists
    assert hasattr(main, 'main')
    print("  - main() ✓")
except Exception as e:
    print(f"✗ Failed to import main: {e}")
    sys.exit(1)

# Test 5: Check dependencies
print("\nChecking dependencies...")
try:
    import cv2
    print("✓ opencv-python-headless")
except ImportError:
    print("✗ opencv-python-headless not installed")

try:
    import numpy
    print("✓ numpy")
except ImportError:
    print("✗ numpy not installed")

try:
    from rapidocr_onnxruntime import RapidOCR
    print("✓ rapidocr-onnxruntime")
except ImportError:
    print("✗ rapidocr-onnxruntime not installed")

try:
    import pyperclip
    print("✓ pyperclip")
except ImportError:
    print("✗ pyperclip not installed")

print("\n" + "=" * 50)
print("✓ Package structure is valid!")
print("\nYou can now:")
print("  1. Run: python3 -m text_extractor.main")
print("  2. Or install: ./install/install.sh")
