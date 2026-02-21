from models.payment import Payment
from sqlalchemy.ext.asyncio import AsyncSession


class PaymentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_payment(self, payment_data: Payment):
        self.session.add(payment_data)
        await self.session.commit()
        await self.session.refresh(payment_data)
        return payment_data