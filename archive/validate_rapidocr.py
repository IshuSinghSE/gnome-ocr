import time
from rapidocr_onnxruntime import RapidOCR
from PIL import Image

# --- Configuration ---
IMAGE_PATH = 'test.png'  # Use your most challenging image
# ---------------------

def test_rapidocr_performance():
    """
    Loads the RapidOCR (ONNX) model, runs inference, and prints results.
    """
    print(f"--- Running RapidOCR (ONNX) on '{IMAGE_PATH}' ---")

    # 1. Initialize the Reader
    # This will download the lightweight ONNX models on the first run.
    print("Loading RapidOCR models (this may take a moment)...")
    start_load = time.time()
    try:
        # We can specify which models to use. 
        # 'ch_PP-OCRv3' is a good, fast, multilingual model.
        ocr = RapidOCR()
        print(f"--- Models loaded in {time.time() - start_load:.4f} seconds ---")
    except Exception as e:
        print(f"Error initializing RapidOCR: {e}")
        return

    # 2. Run the OCR process
    print("\nRunning OCR...")
    start_ocr = time.time()

    # RapidOCR can take the file path directly
    result, elapsed = ocr(IMAGE_PATH)

    ocr_time = time.time() - start_ocr

    # Note: 'elapsed' may be a single float or a list/tuple of timings
    def fmt_elapsed(e):
        try:
            return f"{float(e):.4f}s"
        except Exception:
            return str(e)

    if isinstance(elapsed, (list, tuple)):
        try:
            el_str = ", ".join(fmt_elapsed(x) for x in elapsed)
        except Exception:
            el_str = str(elapsed)
    else:
        el_str = fmt_elapsed(elapsed)

    print(f"--- OCR Finished in {ocr_time:.4f} seconds (Inference: {el_str}) ---")

    # 3. Analyze and Print Results
    if not result:
        print("No text found.")
        return

    print("\n--- Extracted Text ---")

    full_text = []
    # Result can have varying formats depending on model version. Handle common cases:
    # - (box, (text, confidence))
    # - (box, text, confidence)
    # - nested lists where elements contain the above
    def extract_text_conf(item):
        # Try to pull out (text, confidence) from an item
        # Returns (text:str, confidence:float|None)
        if item is None:
            return (None, None)
        if isinstance(item, (list, tuple)):
            # case: (box, (text, conf)) or (box, text, conf)
            if len(item) == 2:
                _, second = item
                if isinstance(second, (list, tuple)) and len(second) == 2:
                    return (second[0], second[1])
                # second might be text string
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
        # fallback: if it's a dict or other type, stringify
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

    # 4. Show the final clipboard-ready text
    clipboard_text = '\n'.join(full_text)
    print("\n--- Final Joined Text (ready for clipboard) ---")
    print(clipboard_text)

if __name__ == "__main__":
    test_rapidocr_performance()
