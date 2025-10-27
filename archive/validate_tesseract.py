import pytesseract
from PIL import Image
import cv2
import numpy as np
import time
import os
from pathlib import Path

# --- Configuration ---
IMAGE_PATH = 'images'  # directory containing images to test
RESULTS_DIR = 'results'  # output directory for per-image .txt and processed pngs
# ---------------------

def get_smart_preprocessed_image(img_path):
    """
    Loads an image, upscales it, and applies intelligent 
    thresholding to handle both light and dark modes.
    """
    
    img = cv2.imread(img_path)
    
    # 1. Grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 2. Upscale
    width = int(gray.shape[1] * 2)
    height = int(gray.shape[0] * 2)
    resized = cv2.resize(gray, (width, height), interpolation=cv2.INTER_CUBIC)

    # 3. Apply Otsu's thresholding
    # This is a 'global' threshold that's safer than adaptive
    # It automatically finds the best split-point
    (thresh_val, binary_img) = cv2.threshold(
        resized, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU
    )

    # 4. Check for "dark mode" (white text on black background)
    # We count the number of black vs. white pixels
    total_pixels = binary_img.size
    white_pixels = cv2.countNonZero(binary_img)
    black_pixels = total_pixels - white_pixels

    # If black pixels are the majority, we assume black background
    # and invert the image to make it black-on-white
    if black_pixels > white_pixels:
        print("  (Smart-check: Detected dark background, inverting image...)")
        binary_img = cv2.bitwise_not(binary_img)

    return Image.fromarray(binary_img)

def test_tesseract_performance_v2():
    """
    Walks `IMAGE_PATH` recursively, runs OCR on each image twice:
    - original image
    - smart pre-processed image

    For each image it writes a per-image text file under `RESULTS_DIR` with timings
    and the OCR results, and saves the processed image as `<basename>_processed.png`.

    Finally it writes `compare.txt` to `RESULTS_DIR` with a one-line-per-image summary
    of timings.
    """

    print(f"--- Running OCR v2 on images in '{IMAGE_PATH}' ---")

    # Prepare results directory
    Path(RESULTS_DIR).mkdir(parents=True, exist_ok=True)

    # gather image files (common extensions)
    p = Path(IMAGE_PATH)
    if not p.exists() or not p.is_dir():
        print(f"ERROR: IMAGE_PATH '{IMAGE_PATH}' not found or is not a directory.")
        return

    exts = {'.png', '.jpg', '.jpeg', '.tif', '.tiff', '.bmp', '.gif'}
    image_files = [f for f in p.rglob('*') if f.suffix.lower() in exts]

    if not image_files:
        print(f"No images found in '{IMAGE_PATH}' with extensions: {sorted(exts)}")
        return

    compare_rows = []

    for img_path in sorted(image_files):
        print(f"\nProcessing: {img_path}")
        base = img_path.stem
        out_txt = Path(RESULTS_DIR) / f"{base}.txt"
        processed_png = Path(RESULTS_DIR) / f"{base}_processed.png"

        # --- Original OCR ---
        try:
            start_time_orig = time.time()
            original_image = Image.open(img_path)
            text_orig = pytesseract.image_to_string(original_image)
            time_orig = time.time() - start_time_orig
        except Exception as e:
            print(f"  Error on original image: {e}")
            text_orig = f"<ERROR: {e}>"
            time_orig = -1.0

        print(f"  Original OCR finished in {time_orig:.4f} seconds.")

        # --- Processed OCR ---
        try:
            start_time_proc = time.time()
            processed_image = get_smart_preprocessed_image(str(img_path))
            # Save processed image for inspection
            processed_image.save(processed_png)
            text_proc = pytesseract.image_to_string(processed_image)
            time_proc = time.time() - start_time_proc
        except Exception as e:
            print(f"  Error on processed image: {e}")
            text_proc = f"<ERROR: {e}>"
            time_proc = -1.0

        print(f"  Processed OCR finished in {time_proc:.4f} seconds.")

        # Write per-image result file
        try:
            with open(out_txt, 'w', encoding='utf-8') as fh:
                fh.write(f"Image: {img_path}\n")
                fh.write(f"Original OCR time (s): {time_orig:.6f}\n")
                fh.write("Original OCR result:\n")
                fh.write(text_orig.strip() + "\n\n")
                fh.write(f"Processed OCR time (s): {time_proc:.6f}\n")
                fh.write("Processed OCR result:\n")
                fh.write(text_proc.strip() + "\n")
        except Exception as e:
            print(f"  Error writing result file {out_txt}: {e}")

        # prepare compare row data
        faster = 'n/a'
        if time_orig >= 0 and time_proc >= 0:
            if abs(time_orig - time_proc) < 1e-6:
                faster = 'equal'
            elif time_orig < time_proc:
                faster = 'original'
            else:
                faster = 'processed'

        compare_rows.append((str(img_path), time_orig, time_proc, faster))

    # write compare.txt
    compare_path = Path(RESULTS_DIR) / 'compare.txt'
    try:
        with open(compare_path, 'w', encoding='utf-8') as compfh:
            compfh.write('filename\torig_time_s\tproc_time_s\tfaster\n')
            for row in compare_rows:
                compfh.write(f"{row[0]}\t{row[1]:.6f}\t{row[2]:.6f}\t{row[3]}\n")
        print(f"\nWrote compare summary to: {compare_path}")
    except Exception as e:
        print(f"Error writing compare file: {e}")

if __name__ == "__main__":
    test_tesseract_performance_v2()