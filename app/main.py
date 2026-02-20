from fastapi import FastAPI

app = FastAPI(title="payment-simulator", description="A payment simulator API", version="0.1.0")

@app.get("/health")
async def health():
    return {"status": "ok"}