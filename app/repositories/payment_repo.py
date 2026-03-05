from app.models.payment import Payment
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.schemas.payment import PaymentStatus
from datetime import datetime, timedelta


class PaymentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_payment(self, payment_data: Payment):
        self.session.add(payment_data)
        await self.session.commit()
        await self.session.refresh(payment_data)
        return payment_data
    
    async def get_payment_by_id(self, payment_id: int):
        result = await self.session.execute(select(Payment).where(Payment.id == payment_id))
        return result.scalars().first()
    
    async def get_all_payments(self, merchant_id: int):
        result = await self.session.execute(select(Payment).where(Payment.merchant_id == merchant_id))
        return result.scalars().all()
    
    async def update_payment_status(self, payment_id: int, new_status: PaymentStatus):
        payment = await self.get_payment_by_id(payment_id)
        if payment is None:
            return None
        payment.status = new_status
        await self.session.commit()
        await self.session.refresh(payment)
        return payment
    
    async def count_active_payments(self, merchant_id: int):
        result = await self.session.execute(
           select(func.count()).select_from(Payment).where(
               Payment.merchant_id == merchant_id, Payment.status.in_(
                   [PaymentStatus.PENDING, PaymentStatus.APPROVED]))    
        )
        return result.scalar()



    async def get_pending_payments(self):
        result = await self.session.execute(select(Payment).where(Payment.created_at <= datetime.utcnow() - timedelta(hours=24), Payment.status == PaymentStatus.PENDING))
        return result.scalars().all()