import time
import cv2
import numpy as np
from rapidocr_onnxruntime import RapidOCR
from pathlib import Path
import os

# --- Configuration ---
IMAGES_DIR = 'images'  # folder containing images to process
RESULTS_DIR = 'results_rapidocr_cv'  # output directory for per-image results
EXTS = {'.png', '.jpg', '.jpeg', '.tif', '.tiff', '.bmp', '.gif'}
# ---------------------


def get_clean_image(img_path):
    """
    Loads an image and applies the same "smart-invert" heuristic used
    in the single-image script to make the image black-on-white.
    Returns a grayscale numpy array.
    """
    img = cv2.imread(str(img_path))
    if img is None:
        raise FileNotFoundError(f"Could not read image: {img_path}")

    # 1. Grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 2. Calculate mean brightness
    mean_intensity = np.mean(gray)

    print(f"  (Smart-Check: Mean intensity is {mean_intensity:.2f})")

    # 3. Heuristic: If mean is < 127, it's probably dark mode.
    if mean_intensity < 127:
        print("  (Smart-Check: Dark mode detected, inverting image...)")
        clean_image = cv2.bitwise_not(gray)
    else:
        print("  (Smart-Check: Light mode detected, using original.)")
        clean_image = gray

    return clean_image


def fmt_elapsed(elapsed):
    # elapsed may be float or list/tuple
    def fmt(e):
        try:
            return f"{float(e):.4f}s"
        except Exception:
            return str(e)

    if isinstance(elapsed, (list, tuple)):
        return ", ".join(fmt(e) for e in elapsed)
    return fmt(elapsed)


def extract_text_conf(item):
    # Reuse the robust extractor pattern used elsewhere in the repo
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


def run_batch():
    print(f"--- Running RapidOCR (CV batch) on images in '{IMAGES_DIR}' ---")

    p = Path(IMAGES_DIR)
    if not p.exists() or not p.is_dir():
        print(f"ERROR: images dir '{IMAGES_DIR}' not found or not a directory.")
        return

    image_files = [f for f in p.rglob('*') if f.suffix.lower() in EXTS]
    if not image_files:
        print(f"No images found in '{IMAGES_DIR}' with extensions: {sorted(list(EXTS))}")
        return

    Path(RESULTS_DIR).mkdir(parents=True, exist_ok=True)

    # Initialize OCR engine once
    print("Loading RapidOCR models (this may take a moment on first run)...")
    start_load = time.time()
    try:
        ocr_engine = RapidOCR()
        print(f"--- Models loaded in {time.time() - start_load:.4f} seconds ---")
    except Exception as e:
        print(f"Error initializing RapidOCR: {e}")
        return

    compare_rows = []

    for img_path in sorted(image_files):
        print(f"\nProcessing: {img_path}")
        base = img_path.stem
        out_txt = Path(RESULTS_DIR) / f"{base}.txt"
        processed_png = Path(RESULTS_DIR) / f"{base}_processed.png"

        # Pre-process
        try:
            clean_arr = get_clean_image(img_path)
        except Exception as e:
            print(f"  Error pre-processing {img_path}: {e}")
            compare_rows.append((str(img_path), -1.0, "preproc-error"))
            continue

        # OCR
        try:
            start_ocr = time.time()
            result, elapsed = ocr_engine(clean_arr)
            ocr_time = time.time() - start_ocr
        except Exception as e:
            print(f"  Error during OCR for {img_path}: {e}")
            compare_rows.append((str(img_path), -1.0, "ocr-error"))
            continue

        # Save processed image for inspection
        try:
            # ensure single-channel saved as PNG
            cv2.imwrite(str(processed_png), clean_arr)
        except Exception as e:
            print(f"  Warning: couldn't save processed image {processed_png}: {e}")

        # Parse results
        full_text = []
        if result:
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
        else:
            print("  No text found.")

        # Write per-image result file
        try:
            with open(out_txt, 'w', encoding='utf-8') as fh:
                fh.write(f"Image: {img_path}\n")
                fh.write(f"OCR wall time (s): {ocr_time:.6f}\n")
                fh.write(f"Inference elapsed: {fmt_elapsed(elapsed)}\n\n")
                fh.write("OCR result:\n")
                fh.write(("\n".join(full_text).strip() or "<no text>") + "\n")
        except Exception as e:
            print(f"  Error writing result file {out_txt}: {e}")

        compare_rows.append((str(img_path), ocr_time, fmt_elapsed(elapsed)))

    # write compare.txt
    compare_path = Path(RESULTS_DIR) / 'compare.txt'
    try:
        with open(compare_path, 'w', encoding='utf-8') as compfh:
            compfh.write('filename\tocr_wall_time_s\tinference_elapsed\n')
            for row in compare_rows:
                compfh.write(f"{row[0]}\t{row[1]:.6f}\t{row[2]}\n")
        print(f"\nWrote compare summary to: {compare_path}")
    except Exception as e:
        print(f"Error writing compare file: {e}")


if __name__ == '__main__':
    run_batch()
