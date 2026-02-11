# app/ml/ocr/extract_entities.py

import re
from datetime import datetime

def extract_vendor(lines):
    """
    Naive vendor extractor:
    Assumes first alphabetic line is vendor.
    """
    for line in lines:
        if re.search(r"[a-zA-Z]", line):
            return line.title()
    return None


def extract_date(lines):
    """
    Extracts date in formats like:
      - 10 jun 2018
      - 10/06/2018
      - 10-06-18
    """
    date_patterns = [
        r"(\d{1,2} [a-z]{3,9} \d{2,4})",
        r"(\d{1,2}/\d{1,2}/\d{2,4})",
        r"(\d{1,2}-\d{1,2}-\d{2,4})",
    ]

    for line in lines:
        for pattern in date_patterns:
            match = re.search(pattern, line)
            if match:
                text = match.group(1)
                try:
                    return datetime.strptime(text, "%d %b %Y")
                except:
                    try:
                        return datetime.strptime(text, "%d %B %Y")
                    except:
                        pass
    return None


def extract_total(lines):
    """
    Finds the total amount on the bill.
    Looks for the highest value with RM/₹/$ etc.
    """

    money_regex = r"(\d+\.\d{1,2})"
    candidates = []

    for line in lines:
        matches = re.findall(money_regex, line)
        for m in matches:
            try:
                candidates.append(float(m))
            except:
                pass

    if not candidates:
        return None

    return max(candidates)


def extract_entities(lines):
    """
    Unified entity extractor.
    Returns: {vendor, date, total}
    """
    vendor = extract_vendor(lines)
    date = extract_date(lines)
    total = extract_total(lines)

    return {
        "vendor": vendor,
        "date": date,
        "total": total
    }
