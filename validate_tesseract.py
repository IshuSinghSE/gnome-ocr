import pytesseract
from PIL import Image
import cv2
import numpy as np
import time

# --- Configuration ---
IMAGE_PATH = 'test.png'  # Use your challenging image
# ---------------------

def get_preprocessed_image(img_path):
    """Loads an image and applies OpenCV pre-processing."""
    
    # Read the image with OpenCV
    img = cv2.imread(img_path)
    
    # 1. Convert to Grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 2. Upscale the image (e.g., 2x). This is a key step.
    # We use INTER_CUBIC for better quality interpolation
    width = int(gray.shape[1] * 2)
    height = int(gray.shape[0] * 2)
    dim = (width, height)
    resized = cv2.resize(gray, dim, interpolation=cv2.INTER_CUBIC)

    # 3. Apply adaptive thresholding to get a clean, binary image
    # This is better than a simple global threshold for screenshots
    processed_img = cv2.adaptiveThreshold(
        resized,
        255,  # Max value
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C, # Method
        cv2.THRESH_BINARY, # Threshold type
        11, # Block size
        2  # Constant subtracted from the mean
    )
    
    # Convert back to a PIL Image format for Pytesseract
    return Image.fromarray(processed_img)

def test_tesseract_performance():
    """
    Runs Tesseract on a non-processed and pre-processed image 
    and compares the results.
    """
    
    print(f"--- Running OCR on '{IMAGE_PATH}' ---")
    
    # --- Test 1: Original Image (The 'NormCap' way) ---
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

    # --- Test 2: Pre-processed Image (Our new method) ---
    print("[2] Testing on PRE-PROCESSED image...")
    start_time_proc = time.time()
    try:
        processed_image = get_preprocessed_image(IMAGE_PATH)
        
        # Save for inspection (optional)
        # processed_image.save("test_processed.png") 
        
        text_proc = pytesseract.image_to_string(processed_image)
        time_proc = time.time() - start_time_proc

        print(f"  Finished in {time_proc:.4f} seconds.")
        print(f"  Result:\n{text_proc}\n")
    except Exception as e:
        print(f"  Error on processed image: {e}")

if __name__ == "__main__":
    test_tesseract_performance()
