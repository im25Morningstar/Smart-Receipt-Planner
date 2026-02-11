# app/services/receipt_processing.py

import uuid
from datetime import datetime

from app.ml.ocr.ocr_reader import extract_text
from app.ml.ocr.text_cleaning import extract_text_lines, normalize_text
from app.ml.ocr.extract_entities import extract_entities

from app.ml.receipt_validator import predict_receipt
from app.ml.expense_classifier.inference import predict_expense


def process_receipt(image_path, receipt_model, expense_tokenizer, expense_model, expense_id2label, device):
    """
    Full end-to-end pipeline:
      1. Validate receipt
      2. Run OCR
      3. Normalize text
      4. Extract vendor, date, total
      5. Categorize expense
      6. Produce final summary
    """

    # 1. Receipt validation
    receipt_check = predict_receipt(image_path, receipt_model, device)
    if receipt_check["label"] != "receipt":
        return {"error": "Not a receipt", "confidence": receipt_check["confidence"]}

    # 2. OCR
    raw_results = extract_text(image_path)
    raw_lines = extract_text_lines(raw_results)

    # 3. Normalize
    normalized_lines = normalize_text(raw_lines)

    # 4. Entities
    entities = extract_entities(normalized_lines)

    # 5. Expense category
    category_result = predict_expense(
        " ".join(normalized_lines),
        expense_tokenizer,
        expense_model,
        expense_id2label,
        device
    )

    # 6. Final result
    return {
        "receipt_id": str(uuid.uuid4()),
        "vendor": entities["vendor"],
        "date": entities["date"],
        "total": entities["total"],
        "category": category_result["label"],
        "raw_text": raw_lines,
        "normalized_text": normalized_lines,
        "receipt_confidence": receipt_check["confidence"],
        "category_confidence": category_result["confidence"],
        "processed_at": datetime.now().isoformat()
    }
