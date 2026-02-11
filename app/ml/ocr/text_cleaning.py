# app/ml/ocr/text_cleaning.py

import re

def extract_text_lines(results):
    """
    Extracts only text (ignores bounding boxes & confidence).
    results = EasyOCR output
    """
    lines = [item[1] for item in results]
    return lines


def normalize_text(lines):
    """
    Cleans a list of lines:
      - lowercases
      - removes stray characters
      - trims whitespace
      - normalizes OCR mistakes
    """

    normalized = []
    for line in lines:
        text = line.lower().strip()

        # Replace common OCR mistakes
        text = text.replace("o0", "00").replace("o.", "0.")

        # collapse multiple spaces
        text = re.sub(r"\s+", " ", text)

        # remove junk characters
        text = re.sub(r"[^a-z0-9 .:/#,-]", "", text)

        if text:
            normalized.append(text)

    return normalized
