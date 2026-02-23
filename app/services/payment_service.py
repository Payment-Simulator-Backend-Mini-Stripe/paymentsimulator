from app.repositories.payment_repo import PaymentRepository
from app.schemas.payment import PaymentStatus


class PaymentService:
    def __init__(self, payment_repo: PaymentRepository):
        self.payment_repo = payment_repo

    async def create_payment(self, payment_data):
        payment_data.status = PaymentStatus.PENDING
        return await self.payment_repo.create_payment(payment_data)
    

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
            