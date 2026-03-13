from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.payment_router import router as payment_router
from app.api.merchant_router import router as merchant_router
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.services.payment_service import PaymentService
from app.repositories.payment_repo import PaymentRepository
from app.db.session import AsyncSessionLocal

from fastapi.middleware.cors import CORSMiddleware

async def run_expire_payments():
    async with AsyncSessionLocal() as session:
        payment_repo = PaymentRepository(session)
        payment_service_instance = PaymentService(payment_repo, None)
        await payment_service_instance.expire_pending_payments()
    


@asynccontextmanager
async def lifespan(app: FastAPI):

    scheduler = AsyncIOScheduler()
    scheduler.add_job(func=run_expire_payments, trigger="interval", hours=24)
    scheduler.start()
    yield


app = FastAPI(lifespan=lifespan)    


@app.get("/health")
async def health():
    return {"status": "ok"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(payment_router)
app.include_router(merchant_router)