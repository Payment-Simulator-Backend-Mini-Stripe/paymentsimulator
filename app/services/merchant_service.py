from app.repositories.merchant_repo import MerchantRepository
from app.schemas.merchant import MerchantCreate, MerchantUpdate
import secrets


class MerchantService:
    def __init__(self, merchant_repo: MerchantRepository):
        self.merchant_repo = merchant_repo

    async def create_merchant(self, merchant_data: MerchantCreate):
            merchant_data.secret_key = secrets.token_hex(32)
            return await self.merchant_repo.create_merchant(merchant_data)

    async def get_merchant_by_id(self, merchant_id):
         return await self.merchant_repo.get_merchant_by_id(merchant_id)
    
    async def get_all_merchants(self):
        return await self.merchant_repo.get_all_merchants()
    
    async def delete_merchant(self, merchant_id):
        return await self.merchant_repo.delete_merchant(merchant_id)
    
    async def update_merchant(self, merchant_id: int, merchant_data: MerchantUpdate):
         merchant = await self.get_merchant_by_id(merchant_id)
         if merchant is None:
             return None
            merchant.name = merchant_data.name
            merchant.address = merchant_data.address
            merchant.phone = merchant_data.phone
            merchant.registered_at = merchant_data.registered_at
            merchant.status = merchant_data.status
            return await self.merchant_repo.update_merchant(merchant_id, merchant)
        
    
        




