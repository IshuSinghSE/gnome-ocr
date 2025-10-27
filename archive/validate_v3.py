import pytesseract
from PIL import Image
import cv2
import numpy as np
import time

# --- Configuration ---
# *** TEST WITH A DARK MODE IMAGE FIRST, THEN YOUR ORIGINAL LIGHT MODE IMAGE ***
IMAGE_PATH = 'dark_mode_test.png'  
# ---------------------

def get_final_processed_image(img_path):
    """
    Applies the "Mean Intensity" heuristic to fix dark mode images
    without damaging light mode images.
    """
    
    img = cv2.imread(img_path)
    
    # 1. Grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 2. Calculate mean brightness
    mean_intensity = np.mean(gray)
    
    print(f"  (Smart-Check: Mean intensity is {mean_intensity:.2f})")

    # 3. Heuristic: If mean is < 127, it's probably dark mode.
    if mean_intensity < 127:
        print("  (Smart-Check: Dark mode detected, inverting image...)")
        # Invert the image
        final_image = cv2.bitwise_not(gray)
    else:
        print("  (Smart-Check: Light mode detected, using original image.)")
        # Use the original grayscale image
        final_image = gray
        
    # Optional: Apply a simple, non-destructive upscale
    # This can still help Tesseract
    width = int(final_image.shape[1] * 2)
    height = int(final_image.shape[0] * 2)
    final_image = cv2.resize(final_image, (width, height), interpolation=cv2.INTER_LANCZOS4)

    return Image.fromarray(final_image)

def test_final_heuristic():
    print(f"--- Running Final Heuristic OCR on '{IMAGE_PATH}' ---")
    
    # --- Test 1: Original Image ---
    print("\n[1] Testing on ORIGINAL image...")
    start_time_orig = time.time()
    try:
        original_image = Image.open(IMAGE_PATH)
        text_orig = pytesseract.image_to_string(original_image)
        time_orig = time.time() - start_time_orig
        
        print(f"  Finished in {time_orig:.4f} seconds.")
        print(f"  Result:\n{text_orig}\n")
    except Exception as e:
        print(f"  Error on original image: {e}")

    # --- Test 2: Final Heuristic Image ---
    print("[2] Testing on FINAL HEURISTIC image...")
    start_time_proc = time.time()
    try:
        processed_image = get_final_processed_image(IMAGE_PATH)
        
        # Save for inspection
        processed_image.save("test_processed_final.png") 
        
        text_proc = pytesseract.image_to_string(processed_image)
        time_proc = time.time() - start_time_proc

        print(f"  Finished in {time_proc:.4f} seconds.")
        print(f"  Result:\n{text_proc}\n")
    except Exception as e:
        print(f"  Error on processed image: {e}")

if __name__ == "__main__":
    test_final_heuristic()