import enum

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class MerchantCreate(BaseModel):
    name_store: str
    address: str
    email: EmailStr
    status: str
    wallet: float
        
class MerchantStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


    
class MerchantResponse(BaseModel):
    id: int
    name_store : str
    email: EmailStr
    registered_at: datetime
    model_config = {"from_attributes": True}
    wallet: float


class MerchantCreatedResponse(BaseModel):
    id: int
    name_store : str
    email: EmailStr
    registered_at: datetime
    wallet: float
    api_key: str
    model_config = {"from_attributes": True}

class MerchantUpdate(BaseModel):
    name_store: Optional[str] = None
    address: Optional[str] = None
    email: Optional[EmailStr] = None
    status: Optional[str] = None
    wallet: Optional[float] = None

            