from fastapi import FastAPI
from app.api.payment_router import router as payment_router
from app.api.merchant_router import router as merchant_router
app = FastAPI(title="payment-simulator", description="A payment simulator API", version="0.1.0")

@app.get("/health")
async def health():
    return {"status": "ok"}

app.include_router(payment_router)
app.include_router(merchant_router)