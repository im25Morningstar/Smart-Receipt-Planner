import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image


def load_receipt_model(model_path: str, device: torch.device):
    model = models.resnet18(pretrained=False)

    num_features = model.fc.in_features
    model.fc = nn.Linear(num_features, 2)

    model.load_state_dict(torch.load(model_path, map_location=device))

    model = model.to(device)
    model.eval()   

    return model


def get_inference_transform():
    return transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])

def predict_receipt(image_path, model, device):
    transform = get_inference_transform()

    image = Image.open(image_path).convert("RGB")
    image = transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        outputs = model(image)
        probs = torch.softmax(outputs, dim=1)
        confidence, pred = torch.max(probs, dim=1)

    label_map = {0: "not_receipt", 1: "receipt"}

    return {
        "label": label_map[pred.item()],
        "confidence": float(confidence.item())
    }

