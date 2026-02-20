from pydantic import BaseModel, EmailStr
from datetime import datetime

class MerchantCreate(BaseModel):
    name: str
    email: EmailStr
        

    
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