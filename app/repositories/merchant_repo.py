from app.models.merchant import Merchant
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

class MerchantRepository:
    def __init__ (self, session: AsyncSession):
        self.session = session

    async def get_all_merchants(self):
        result = await self.session.execute(select(Merchant))
        return result.scalars().all()
    
    async def get_merchant_by_id(self, merchant_id: int):
        result = await self.session.execute(select(Merchant).where(Merchant.id == merchant_id))
        return result.scalars().first()
    

    async def create_merchant(self, merchant: Merchant):
        self.session.add(merchant)
        await self.session.commit()
        await self.session.refresh(merchant)
        return merchant

    async def update_merchant(self, merchant: Merchant, merchant_id: int):
        result = await self.session.execute(select(Merchant).where(Merchant.id == merchant_id))
        existing_merchant = result.scalars().first()
        
        if existing_merchant is None:
            return None
        
        existing_merchant.name_store = merchant.name_store
        existing_merchant.address = merchant.address
        existing_merchant.email = merchant.email
        existing_merchant.status = merchant.status
        
        await self.session.commit()
        await self.session.refresh(existing_merchant)
        return existing_merchant
    

    async def delete_merchant(self, merchant_id: int):
        result = await self.session.execute(select(Merchant).where(Merchant.id == merchant_id))
        existing_merchant = result.scalars().first()
        
        if existing_merchant is None:
            return None
        
        await self.session.delete(existing_merchant)
        await self.session.commit()
        return existing_merchant