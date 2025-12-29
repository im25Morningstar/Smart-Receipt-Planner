from fastapi import APIRouter
from app.schemas.receipt import ReceiptUploadResponse
from app.services.receipt_service import create_receipt

router = APIRouter(prefix="/receipts", tags=["receipts"])

@router.post("/upload",response_model=ReceiptUploadResponse)
def upload_receipt():
    result=create_receipt()
    return result

