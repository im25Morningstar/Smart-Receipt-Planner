from fastapi import APIRouter, UploadFile, File
import shutil
import uuid
import os

from app.services.receipt_services import validate_receipt_image

router = APIRouter()
from app.schemas.receipt import ReceiptValidationResponse

@router.post(
    "/receipt/validate",
    response_model=ReceiptValidationResponse
)

def validate_receipt(file: UploadFile = File(...)):
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)

    temp_path = f"{temp_dir}/{uuid.uuid4()}_{file.filename}"

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        result = validate_receipt_image(temp_path)
    finally:
        os.remove(temp_path)

    return result

