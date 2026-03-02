from fastapi import Header, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.repositories.merchant_repo import MerchantRepository

async def get_current_merchant(x_api_key: str = Header(...), db: AsyncSession = Depends(get_db)):
    merchant_repo = MerchantRepository(db)
    merchant = await merchant_repo.get_merchant_by_secret_key(x_api_key)
    
    if not merchant:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    
    return merchant