import time
import cv2
import numpy as np
from rapidocr_onnxruntime import RapidOCR

# --- Configuration ---
IMAGE_PATH = 'test.png'  # Use your dark mode test image
# ---------------------

def get_clean_image(img_path):
    """
    Loads an image and applies our "smart-invert" heuristic
    to ensure it's black-on-white for the OCR engine.
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
        # Invert the image to make it black-on-white
        clean_image = cv2.bitwise_not(gray)
    else:
        print("  (Smart-Check: Light mode detected, using original.)")
        clean_image = gray
        
    return clean_image

def test_final_backend():
    """
    Runs the full pre-processing + OCR pipeline.
    """
    print(f"--- Running Final Backend on '{IMAGE_PATH}' ---")

    # 1. Initialize the OCR Engine (one-time cost)
    print("Loading RapidOCR models...")
    start_load = time.time()
    try:
        ocr_engine = RapidOCR()
        print(f"--- Models loaded in {time.time() - start_load:.4f} seconds ---")
    except Exception as e:
        print(f"Error initializing RapidOCR: {e}")
        return

    # 2. Get the Pre-Processed Image
    print("\nPre-processing image...")
    clean_image_array = get_clean_image(IMAGE_PATH)

    # 3. Run OCR on the clean image array
    print("\nRunning OCR...")
    start_ocr = time.time()
    
    # Pass the numpy array directly (faster than passing a path)
    result, elapsed = ocr_engine(clean_image_array)
    
    ocr_time = time.time() - start_ocr
    print(f"--- OCR Finished in {ocr_time:.4f} seconds ---")

    # 4. Analyze and Print Results
    if not result:
        print("No text found.")
        return

    print("\n--- Extracted Text ---")

    full_text = []
    # Make parsing robust to multiple result formats (box,(text,conf)) or (box,text,conf)
    def extract_text_conf(item):
        if item is None:
            return (None, None)
        if isinstance(item, (list, tuple)):
            if len(item) == 2:
                _, second = item
                if isinstance(second, (list, tuple)) and len(second) == 2:
                    return (second[0], second[1])
                return (second, None)
            if len(item) == 3:
                _, text, conf = item
                return (text, conf)
            # deeper nested: search for first str and a numeric
            text = None
            conf = None
            for x in item:
                if isinstance(x, str) and text is None:
                    text = x
                if isinstance(x, (float, int)) and conf is None:
                    conf = float(x)
                if text is not None and conf is not None:
                    break
            return (text, conf)
        return (str(item), None)

    for item in result:
        text, confidence = extract_text_conf(item)
        if text is None:
            continue
        try:
            conf_pct = (float(confidence) * 100.0) if confidence is not None else None
        except Exception:
            conf_pct = None
        if conf_pct is not None:
            print(f"  Text: \"{text}\" (Confidence: {conf_pct:.2f}%)")
        else:
            print(f"  Text: \"{text}\"")
        full_text.append(text)

    clipboard_text = '\n'.join(full_text)
    print("\n--- Final Joined Text (ready for clipboard) ---")
    print(clipboard_text)

if __name__ == "__main__":
    test_final_backend()