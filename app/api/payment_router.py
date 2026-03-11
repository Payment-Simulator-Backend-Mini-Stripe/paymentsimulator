from fastapi import APIRouter, Depends
from app.repositories.payment_repo import PaymentRepository
from app.repositories.webhook_repo import WebhookRepository
from app.schemas.payment import PaymentCreate, PaymentStatusUpdate
from app.services.payment_service import PaymentService
from app.db.session import get_db
from app.core.authentication import get_current_merchant
from app.repositories.merchant_repo import MerchantRepository
from app.services.webhook_service import WebhookService


router = APIRouter(prefix="/payments", dependencies=[Depends(get_current_merchant)])

async def get_payment_service(db=Depends(get_db)):
    return PaymentService(PaymentRepository(db), MerchantRepository(db), WebhookService(WebhookRepository(db)))


@router.get("/")
async def get_all_payments(merchant_id: int, service=Depends(get_payment_service)):
    return await service.get_all_payments(merchant_id) 

@router.get("/{payment_id}")
async def get_payment(payment_id: int, service=Depends(get_payment_service)):
    return await service.get_payment_by_id(payment_id)

@router.post("/")
async def create_payment(payment_data: PaymentCreate, merchant=Depends(get_current_merchant), service=Depends(get_payment_service)):    
    return await service.create_payment(payment_data, merchant.id)

@router.put("/{payment_id}")
async def update_payment(payment_id: int, payment_data: PaymentStatusUpdate, service=Depends(get_payment_service)):
    return await service.update_payment(payment_id, payment_data.status)

@router.post("/{payment_id}/refund", status_code=200)
async def refund_payment(
    payment_id: int,
    service=Depends(get_payment_service),
    merchant=Depends(get_current_merchant)
):
    return await service.refund_payment(payment_id)