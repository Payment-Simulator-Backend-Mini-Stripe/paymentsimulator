from fastapi import HTTPException

from app.models.payment import Payment
from app.repositories.payment_repo import PaymentRepository
from app.repositories.merchant_repo import MerchantRepository
from app.schemas.payment import PaymentStatus
from app.core.config import settings


class PaymentService:
    def __init__(self, payment_repo: PaymentRepository, merchant_repo: MerchantRepository):
        self.payment_repo = payment_repo
        self.merchant_repo = merchant_repo


    async def create_payment(self, payment_data, merchant_id: int):
        if not await self.merchant_repo.is_merchant_active(merchant_id):
            raise HTTPException(status_code=403, detail="Merchant is not active")
        
        active_payments = await self.payment_repo.count_active_payments(merchant_id)
        if active_payments >= settings.MAX_ACTIVE_PAYMENTS_PER_MERCHANT:
            raise HTTPException(status_code=429, detail="Merchant has reached the maximum number of active payments")

        if payment_data.amount > settings.MAX_PAYMENT_AMOUNT:
            raise HTTPException(status_code=400, detail=f"Payment amount exceeds the maximum limit of {settings.MAX_PAYMENT_AMOUNT}")
        new_payment = Payment(
            amount=payment_data.amount,
            status=PaymentStatus.PENDING,
            merchant_id=merchant_id
        )
        try:
            created_payment = await self.payment_repo.create_payment(new_payment)
            return created_payment
        except Exception as e:
            if new_payment.id:
                await self.payment_repo.update_payment_status(new_payment.id, PaymentStatus.FAILED)
            raise HTTPException(status_code=500, detail="Failed to create payment")
        
        
    async def get_payment_by_id(self, payment_id):
        return await self.payment_repo.get_payment_by_id(payment_id)

    async def get_all_payments(self, merchant_id):
        return await self.payment_repo.get_all_payments(merchant_id)
    
    async def update_payment(self, payment_id: int, new_status: PaymentStatus):
            payment = await self.get_payment_by_id(payment_id)
            if payment is None:
                return None
            payment.status = new_status
            return await self.payment_repo.update_payment_status(payment_id, new_status)



    async def expire_pending_payments(self):
            for payment in await self.payment_repo.get_pending_payments():
                 await self.payment_repo.update_payment_status(payment.id, PaymentStatus.FAILED)
            