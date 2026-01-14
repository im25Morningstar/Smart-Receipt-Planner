from pydantic import BaseModel

class ReceiptValidationResponse(BaseModel):
    label: str
    confidence: float

