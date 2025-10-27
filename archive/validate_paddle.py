import time
from paddleocr import PaddleOCR
from PIL import Image

# --- Configuration ---
IMAGE_PATH = 'test.png'  # Use your most challenging image
# ---------------------

def test_paddle_performance():
    """
    Loads the PaddleOCR model, runs inference, and prints results.
    """
    print(f"--- Running PaddleOCR on '{IMAGE_PATH}' ---")

    # 1. Initialize the Reader
    # This will download models on the first run.
    # We explicitly set use_gpu=False.
    print("Loading PaddleOCR model (this may take a moment on first run)...")
    start_load = time.time()
    ocr = None
    # Try the common/older constructor first, then fall back to newer signatures.
    try:
        ocr = PaddleOCR(use_textline_orientation=True, lang='en')
        print(f"--- Model loaded in {time.time() - start_load:.4f} seconds (constructor: use_textline_orientation + use_gpu) ---")
    except Exception as e:
        # Some installs don't accept `use_gpu` or `use_textline_orientation`. Try fallbacks.
        print(f"Constructor with (use_textline_orientation, use_gpu) failed: {e}")
        try:
            # newer versions may use `use_textline_orientation` instead of `use_angle_cls`, and may not accept use_gpu
            ocr = PaddleOCR(use_textline_orientation=True, lang='en')
            print(f"--- Model loaded in {time.time() - start_load:.4f} seconds (constructor: use_textline_orientation) ---")
        except Exception as e2:
            print(f"Fallback constructor with use_textline_orientation failed: {e2}")
            try:
                # final fallback: minimal args
                ocr = PaddleOCR(lang='en')
                print(f"--- Model loaded in {time.time() - start_load:.4f} seconds (constructor: lang only) ---")
            except Exception as e3:
                print(f"Error initializing PaddleOCR with fallbacks: {e3}")
                return
    except Exception as e:
        print(f"Error initializing PaddleOCR: {e}")
        return

    # 2. Run the OCR process
    print("\nRunning OCR...")
    start_ocr = time.time()
    
    # PaddleOCR's 'ocr' method handles detection and recognition
    result = ocr.predict(IMAGE_PATH, cls=True)
    
    ocr_time = time.time() - start_ocr
    print(f"--- OCR Finished in {ocr_time:.4f} seconds ---")

    # 3. Analyze and Print Results
    if not result or not result[0]:
        print("No text found.")
        return

    print("\n--- Extracted Text ---")
    
    full_text = []
    # Paddle's result is a nested list. result[0] contains the lines.
    for line in result[0]:
        # line[1] contains (text, confidence)
        text = line[1][0]
        confidence = line[1][1]
        print(f"  Text: \"{text}\" (Confidence: {confidence*100:.2f}%)")
        full_text.append(text)

    # 4. Show the final clipboard-ready text
    # We join with a newline for multi-line text, which is smarter
    clipboard_text = '\n'.join(full_text)
    print("\n--- Final Joined Text (ready for clipboard) ---")
    print(clipboard_text)

if __name__ == "__main__":
    test_paddle_performance()