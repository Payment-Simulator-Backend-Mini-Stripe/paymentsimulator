from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class MerchantCreate(BaseModel):
    name_store: str
    address: str
    email: EmailStr
    status: str
        

    
class MerchantResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime


class MerchantCreatedResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime
    api_key: str

class MerchantUpdate(BaseModel):
    name_store: Optional[str] = None
    address: Optional[str] = None
    email: Optional[EmailStr] = None
    status: Optional[str] = None
    
    
            