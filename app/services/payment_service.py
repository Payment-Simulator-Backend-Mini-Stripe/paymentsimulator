from fastapi import HTTPException
from app.models.payment import Payment
from app.repositories.payment_repo import PaymentRepository
from app.repositories.merchant_repo import MerchantRepository
from app.schemas import payment
from app.schemas.payment import PaymentStatus
from app.core.config import settings
from app.services.webhook_service import WebhookService
import logging
from app.schemas.merchant import MerchantStatus

logger = logging.getLogger(__name__)

class PaymentService:
    def __init__(self, payment_repo: PaymentRepository, merchant_repo: MerchantRepository, webhook_service: WebhookService):
        self.payment_repo = payment_repo
        self.merchant_repo = merchant_repo
        self.webhook_service = webhook_service

    

    async def create_payment(self, payment_data, payer_id: int, receiver_id: int):
        if not await self.merchant_repo.is_merchant_active(payer_id):
            raise HTTPException(status_code=403, detail="Merchant is not active")
        
        active_payments = await self.payment_repo.count_active_payments(payer_id)
        if active_payments >= settings.MAX_ACTIVE_PAYMENTS_PER_MERCHANT:
            raise HTTPException(status_code=429, detail="Merchant has reached the maximum number of active payments")

        if payment_data.amount > settings.MAX_PAYMENT_AMOUNT:
            raise HTTPException(status_code=400, detail=f"Payment amount exceeds the maximum limit of {settings.MAX_PAYMENT_AMOUNT}")
        new_payment = Payment(
            amount=payment_data.amount,
            status=PaymentStatus.PENDING,
            payer_id=payer_id,
            receiver_id=receiver_id
        )
        try:
            created_payment = await self.payment_repo.create_payment(new_payment)
            return created_payment
        except Exception as e:
            if new_payment.id:
                await self.payment_repo.update_payment_status(new_payment.id, PaymentStatus.FAILED)
            raise HTTPException(status_code=500, detail="Failed to create payment")
        
    async def refund_payment(self, payment_id: int):
        payment = await self.get_payment_by_id(payment_id)
        if payment is None:
            raise HTTPException(status_code=404, detail="Payment not found")
        if payment.status != PaymentStatus.APPROVED:
            raise HTTPException(status_code=400, detail="Only approved payments can be refunded")
        try:
            updated_payment = await self.payment_repo.update_payment_status(payment_id, PaymentStatus.REFUNDED)
            await self.webhook_service.send_webhook(updated_payment)
            return updated_payment
        except Exception as e:
            raise HTTPException(status_code=500, detail="Failed to refund payment")
        

        
    async def get_payment_by_id(self, payment_id):
        return await self.payment_repo.get_payment_by_id(payment_id)

    async def get_all_payments(self, merchant_id: int):
        return await self.payment_repo.get_all_payments(merchant_id)

    async def update_payment(self, payment_id: int, new_status: PaymentStatus):
        payment = await self.get_payment_by_id(payment_id)
        if payment is None:
            return None
        payment.status = new_status
        try:
            updated_payment = await self.payment_repo.update_payment_status(payment_id, new_status)
            await self.webhook_service.send_webhook(updated_payment)
            return updated_payment
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
                

    async def expire_pending_payments(self):
        pending_payments = await self.payment_repo.get_pending_payments()

        for payment in pending_payments:
            try:
                updated_payment = await self.payment_repo.update_payment_status(
                    payment.id,
                    PaymentStatus.FAILED
                )

                await self.webhook_service.send_webhook(updated_payment)    

            except Exception as e:
                logger.error(f"Failed to expire payment {payment.id}: {e}")
            

    async def process_payment(self, payment_id: int):
        payment = await self.get_payment_by_id(payment_id)
        if payment is None:
            return
        payer = await self.merchant_repo.get_merchant_by_id(payment.payer_id)
        if payer is None or payer.status != MerchantStatus.ACTIVE:
            await self.payment_repo.update_payment_status(payment_id, PaymentStatus.FAILED)
            return
        if payment.amount > settings.MAX_PAYMENT_AMOUNT:
            await self.payment_repo.update_payment_status(payment_id, PaymentStatus.FAILED)
            return
        if payer.wallet < payment.amount:
            await self.payment_repo.update_payment_status(payment_id, PaymentStatus.FAILED)
            return
        receiver = await self.merchant_repo.get_merchant_by_id(payment.receiver_id)
        await self.merchant_repo.update_wallet(payment.payer_id, payer.wallet - payment.amount)
        await self.merchant_repo.update_wallet(payment.receiver_id, receiver.wallet + payment.amount)
        await self.payment_repo.update_payment_status(payment_id, PaymentStatus.APPROVED)
        await self.webhook_service.send_webhook(payment)
        

    