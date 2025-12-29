from pydantic import BaseModel

class ReceiptUploadResponse(BaseModel):
    receipt_id: str
    status: str 
    message: str

    
