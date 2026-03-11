from fastapi import APIRouter, Body, Depends, HTTPException
from app.repositories.merchant_repo import MerchantRepository
from app.repositories.webhook_repo import WebhookRepository
from app.schemas.merchant import MerchantCreate
from app.schemas.webhook import WebhookConfigCreate
from app.services.merchant_service import MerchantService
from app.db.session import get_db
from app.services.webhook_service import WebhookService

router = APIRouter(prefix="/merchants")

async def get_merchant_service(db=Depends(get_db)):
    return MerchantService(MerchantRepository(db))

@router.get("/")
async def get_all_merchants(service=Depends(get_merchant_service)):
    return await service.get_all_merchants()

@router.get("/{merchant_id}")
async def get_merchant(merchant_id: int, service=Depends(get_merchant_service)):
    return await service.get_merchant_by_id(merchant_id)

@router.post("/")
async def create_merchant(merchant_data: MerchantCreate, service=Depends(get_merchant_service)):
    return await service.create_merchant(merchant_data)

@router.put("/{merchant_id}")
async def update_merchant(merchant_id: int, merchant_data: MerchantCreate, service=Depends(get_merchant_service)):
    return await service.update_merchant(merchant_id, merchant_data)    

@router.post("/get_merchant_by_email")
async def get_merchant_by_email(email: str = Body(...), service=Depends(get_merchant_service)):
    merchant = await service.get_merchant_by_email(email)
    if not merchant:
        raise HTTPException(status_code=401, detail="Invalid Email")
    return {"secret_key": merchant.secret_key}


async def get_webhook_service(db=Depends(get_db)):
    return WebhookService(WebhookRepository(db))

@router.post("/{merchant_id}/webhook")
async def set_webhook(merchant_id: int, webhook_data: WebhookConfigCreate, service=Depends(get_webhook_service)):
    return await service.webhook_repo.create_webhook_config(
        merchant_id=merchant_id,
        url=webhook_data.url,
        secret=webhook_data.secret
    )



