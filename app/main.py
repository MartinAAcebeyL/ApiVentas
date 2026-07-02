from fastapi import FastAPI
from app.api.v1.router import api_router

app = FastAPI(title="ApiVentas", version="2.0.0")

app.include_router(api_router, prefix="/api/v1")


@app.get("/health")
async def health():
    return {"status": "ok"}
