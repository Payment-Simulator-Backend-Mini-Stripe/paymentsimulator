from app.repositories.merchant_repo import MerchantRepository
from app.schemas.merchant import MerchantCreate, MerchantUpdate
from app.models.merchant import Merchant
import secrets


class MerchantService:
    def __init__(self, merchant_repo: MerchantRepository):
        self.merchant_repo = merchant_repo

    async def create_merchant(self, merchant_data: MerchantCreate):
        new_merchant = Merchant(
            name_store=merchant_data.name_store,
            address=merchant_data.address,
            email=merchant_data.email,
            status=merchant_data.status,
            secret_key=secrets.token_hex(32)
        )
        return await self.merchant_repo.create_merchant(new_merchant)

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

        merchant.name_store = merchant_data.name_store
        merchant.address = merchant_data.address
        merchant.email = merchant_data.email
        merchant.status = merchant_data.status


        await self.merchant_repo.session.commit()
        await self.merchant_repo.session.refresh(merchant)
        return merchant
        
    
        




