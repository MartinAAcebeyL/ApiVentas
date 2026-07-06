from fastapi import FastAPI
from app.api.v1.router import api_router
from app.dashboard.routes import router as dashboard_router

app = FastAPI(title="ApiVentas", version="2.1.0")

app.include_router(api_router, prefix="/api/v1")
app.include_router(dashboard_router)


@app.get("/health")
async def health():
    return {"status": "ok"}
