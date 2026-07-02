from fastapi import APIRouter
from app.api.v1.endpoints import auth, sales, reports, users

api_router = APIRouter()

api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(sales.router, tags=["sales"])
api_router.include_router(reports.router, tags=["reports"])
api_router.include_router(users.router, tags=["users"])
