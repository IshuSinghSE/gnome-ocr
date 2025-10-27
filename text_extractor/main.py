"""
Main Entry Point for v1 (Cold-Start Mode)

This script coordinates the entire workflow:
1. Capture screenshot
2. Load OCR engine
3. Extract text
4. Copy to clipboard
5. Notify user
"""

import sys
import os
import tempfile
import time
from pathlib import Path

from rapidocr_onnxruntime import RapidOCR

from text_extractor import desktop, backend


def main():
    """Main entry point for the text extractor v1."""
    
    # Check for command line arguments (allow specifying existing image for testing)
    import sys
    
    if len(sys.argv) > 1:
        # Use provided image file instead of screenshot
        screenshot_path = sys.argv[1]
        if not os.path.exists(screenshot_path):
            print(f"ERROR: File not found: {screenshot_path}")
            sys.exit(1)
        print(f"GNOME Text Extractor v1 (using existing image)")
        print("=" * 40)
        print(f"\nUsing image: {screenshot_path}")
        skip_screenshot = True
    else:
        skip_screenshot = False
        print("GNOME Text Extractor v1")
        print("=" * 40)
    
    if not skip_screenshot:
        # Step 1: Capture screenshot
        print("\n[1/4] Capturing screenshot...")
        print("      Please select the area to extract text from.")
        
        # Create a temporary file for the screenshot
        temp_dir = tempfile.gettempdir()
        screenshot_path = os.path.join(temp_dir, 'text-extractor-screenshot.png')
        
        success, error_msg = desktop.capture_screenshot(screenshot_path)
        if not success:
            print(f"ERROR: {error_msg}")
            desktop.send_notification(
                "Text Extractor - Error",
                error_msg or "Screenshot capture failed",
                urgency="critical"
            )
            sys.exit(1)
        
        print(f"      ✓ Screenshot saved to: {screenshot_path}")
    else:
        print("\n[1/4] Skipping screenshot (using provided image)")

    
    # Step 2: Load OCR engine (this is the "cold start" part)
    print("\n[2/4] Loading OCR engine...")
    start_load = time.time()
    
    try:
        ocr_engine = RapidOCR()
        load_time = time.time() - start_load
        print(f"      ✓ Engine loaded in {load_time:.2f} seconds")
    except Exception as e:
        print(f"ERROR: Failed to load OCR engine: {e}")
        desktop.send_notification(
            "Text Extractor - Error",
            f"Failed to load OCR engine: {e}",
            urgency="critical"
        )
        sys.exit(1)
    
    # Step 3: Extract text
    print("\n[3/4] Extracting text from image...")
    start_ocr = time.time()
    
    try:
        extracted_text, text_conf_pairs = backend.extract_text_from_image(
            screenshot_path,
            ocr_engine
        )
        ocr_time = time.time() - start_ocr
        print(f"      ✓ OCR completed in {ocr_time:.2f} seconds")
        
        if not extracted_text:
            print("      ⚠ No text found in the image")
            desktop.send_notification(
                "Text Extractor",
                "No text found in the selected area",
                urgency="normal"
            )
            sys.exit(0)
            
        print(f"      ✓ Extracted {len(text_conf_pairs)} text segment(s)")
        
    except Exception as e:
        print(f"ERROR: Text extraction failed: {e}")
        desktop.send_notification(
            "Text Extractor - Error",
            f"Text extraction failed: {e}",
            urgency="critical"
        )
        sys.exit(1)
    
    # Step 4: Copy to clipboard
    print("\n[4/4] Copying text to clipboard...")
    
    if desktop.copy_to_clipboard(extracted_text):
        print("      ✓ Text copied to clipboard")
        
        # Show preview (first 100 chars)
        preview = extracted_text[:100]
        if len(extracted_text) > 100:
            preview += "..."
        print(f"\n--- Extracted Text Preview ---")
        print(preview)
        print("=" * 40)
        
        # Send success notification
        desktop.send_notification(
            "Text Extractor - Success",
            f"Extracted {len(extracted_text)} characters\nText copied to clipboard!",
            urgency="normal"
        )
    else:
        print("ERROR: Failed to copy text to clipboard")
        desktop.send_notification(
            "Text Extractor - Error",
            "Failed to copy text to clipboard",
            urgency="critical"
        )
        sys.exit(1)
    
    # Cleanup (only if we created the screenshot)
    if not skip_screenshot:
        try:
            os.remove(screenshot_path)
        except Exception:
            pass  # Ignore cleanup errors
    
    print("\n✓ Done!")


if __name__ == "__main__":
    main()
