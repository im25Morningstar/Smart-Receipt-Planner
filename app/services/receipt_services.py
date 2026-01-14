import torch
from app.ml.receipt_validator import load_receipt_model, predict_receipt

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
MODEL_PATH = "models/receipt_validator_resnet18.pth"

model = load_receipt_model(MODEL_PATH, DEVICE)

CONFIDENCE_THRESHOLD = 0.80


def validate_receipt_image(image_path: str):
    result = predict_receipt(
        image_path=image_path,
        model=model,
        device=DEVICE
    )

    label = result["label"]
    confidence = result["confidence"]

    if label == "receipt" and confidence < CONFIDENCE_THRESHOLD:
        return {
            "label": "uncertain",
            "confidence": confidence
        }

    return result
