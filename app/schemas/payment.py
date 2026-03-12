import enum
from pydantic import BaseModel
from datetime import datetime

class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    FAILED = "failed"
    REFUNDED = "refunded"
    
class PaymentStatusUpdate(BaseModel):
    status: PaymentStatus
    
class PaymentCreate(BaseModel):
    amount: int
    payer_id: int
    receiver_id: int
    
class PaymentResponse(BaseModel):
    id: int
    amount: int
    created_at: datetime
    status: PaymentStatus
    payer_id: int
    receiver_id: int
    model_config: dict = {"from_attributes": True}