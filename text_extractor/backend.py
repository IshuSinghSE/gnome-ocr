"""
OCR Backend Engine

Handles image preprocessing and OCR using RapidOCR with ONNX runtime.
Includes smart dark-mode detection and inversion for optimal OCR results.
"""

import cv2
import numpy as np
from rapidocr_onnxruntime import RapidOCR
from typing import Tuple, Optional, List


def get_clean_image(image_path: str) -> np.ndarray:
    """
    Loads an image and applies smart-invert heuristic to ensure
    it's black-on-white for the OCR engine.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Grayscale numpy array optimized for OCR
        
    Raises:
        FileNotFoundError: If image cannot be read
    """
    img = cv2.imread(str(image_path))
    if img is None:
        raise FileNotFoundError(f"Could not read image: {image_path}")
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Calculate mean brightness
    mean_intensity = np.mean(gray)
    
    # Heuristic: If mean is < 127, it's probably dark mode
    if mean_intensity < 127:
        # Invert the image to make it black-on-white
        clean_image = cv2.bitwise_not(gray)
    else:
        clean_image = gray
        
    return clean_image


def extract_text_conf(item) -> Tuple[Optional[str], Optional[float]]:
    """
    Robustly extract text and confidence from various RapidOCR result formats.
    
    Args:
        item: A result item from RapidOCR (can be tuple, list, or nested structure)
        
    Returns:
        Tuple of (text, confidence) or (None, None) if extraction fails
    """
    if item is None:
        return (None, None)
        
    if isinstance(item, (list, tuple)):
        # Format: (box, (text, confidence))
        if len(item) == 2:
            _, second = item
            if isinstance(second, (list, tuple)) and len(second) == 2:
                return (second[0], second[1])
            return (second, None)
            
        # Format: (box, text, confidence)
        if len(item) == 3:
            _, text, conf = item
            return (text, conf)
            
        # Deeper nested: search for first str and a numeric
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


def extract_text_from_image(image_path: str, ocr_engine: RapidOCR) -> Tuple[str, List[Tuple[str, float]]]:
    """
    Extracts text from an image using the provided OCR engine.
    
    Args:
        image_path: Path to the image file
        ocr_engine: Initialized RapidOCR instance
        
    Returns:
        Tuple of (joined_text, list_of_(text, confidence)_tuples)
        
    Raises:
        Exception: If OCR processing fails
    """
    # Preprocess the image
    clean_image = get_clean_image(image_path)
    
    # Run OCR on the preprocessed image
    result, elapsed = ocr_engine(clean_image)
    
    if not result:
        return ("", [])
    
    # Extract text and confidence from results
    text_lines = []
    text_conf_pairs = []
    
    for item in result:
        text, confidence = extract_text_conf(item)
        if text is None:
            continue
            
        text_lines.append(text)
        text_conf_pairs.append((text, confidence if confidence is not None else 0.0))
    
    # Join all text with newlines
    full_text = '\n'.join(text_lines)
    
    return (full_text, text_conf_pairs)
