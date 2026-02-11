# app/ml/ocr/ocr_reader.py

import easyocr

# Load EasyOCR reader once at startup
reader = easyocr.Reader(['en'], gpu=False)

def extract_text(image_path: str):
    """
    Runs OCR on the image and returns raw EasyOCR results.
    
    Output format:
    [
      [bbox, text, confidence],
      ...
    ]
    """
    results = reader.readtext(image_path)
    return results
