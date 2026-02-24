from fastapi import APIRouter, Depends
from app.repositories.payment_repo import PaymentRepository
from app.schemas.payment import PaymentCreate, PaymentStatusUpdate
from app.services.payment_service import PaymentService
from app.db.session import get_db

router = APIRouter(prefix="/payments")

async def get_payment_service(db=Depends(get_db)):
    return PaymentService(PaymentRepository(db))

@router.get("/")
async def get_all_payments(merchant_id: int, service=Depends(get_payment_service)):
    return await service.get_all_payments(merchant_id) 

@router.get("/{payment_id}")
async def get_payment(payment_id: int, service=Depends(get_payment_service)):
    return await service.get_payment_by_id(payment_id)

@router.post("/")
async def create_payment(payment_data: PaymentCreate, service=Depends(get_payment_service)):    
    return await service.create_payment(payment_data)

@router.put("/{payment_id}")
async def update_payment(payment_id: int, payment_data: PaymentStatusUpdate, service=Depends(get_payment_service)):
    return await service.update_payment(payment_id, payment_data)