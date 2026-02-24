from fastapi import APIRouter, Depends
from app.repositories.merchant_repo import MerchantRepository
from app.schemas.merchant import MerchantCreate
from app.services.merchant_service import MerchantService
from app.db.session import get_db

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

@router.put("/")
async def update_merchant(merchant_data: MerchantCreate, service=Depends(get_merchant_service)):
    return await service.update_merchant(merchant_data)    