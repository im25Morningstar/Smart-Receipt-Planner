import torch
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification
import json
import os

def load_expense_model(model_path: str, device: torch.device):
    """
    Load the expense classifier model with correct label mappings.
    """

    # Load tokenizer
    tokenizer = DistilBertTokenizerFast.from_pretrained(model_path)

    # Load id2label from label_map.json (your corrected version)
    with open(os.path.join(model_path, "label_map.json"), "r") as f:
        id2label = json.load(f)

    # Derive label2id (reverse mapping)
    label2id = {v: int(k) for k, v in id2label.items()}

    # Load model with correct mappings
    model = DistilBertForSequenceClassification.from_pretrained(
        model_path,
        id2label={int(k): v for k, v in id2label.items()},
        label2id=label2id
    )

    model.to(device)
    model.eval()

    return tokenizer, model, id2label


def predict_expense(text: str, tokenizer, model, id2label, device: torch.device):
    """
    Run prediction on a single expense text.
    """

    enc = tokenizer(
        text,
        truncation=True,
        padding="max_length",
        max_length=32,
        return_tensors="pt"
    )

    enc = {k: v.to(device) for k, v in enc.items()}

    with torch.no_grad():
        outputs = model(**enc)
        logits = outputs.logits
        probs = torch.softmax(logits, dim=1)
        pred_idx = torch.argmax(probs).item()

    return {
        "label": id2label[str(pred_idx)],
        "confidence": float(probs[0][pred_idx])
    }
