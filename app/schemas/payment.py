import enum
from pydantic import BaseModel
from datetime import datetime

class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    FAILED = "failed"
    REFUNDED = "refunded"
    
class PaymentCreate(BaseModel):
    amount: int


class PaymentResponse(BaseModel):
    merchant_id: int
    id: int
    amount: int
    created_at: datetime
    status: PaymentStatus