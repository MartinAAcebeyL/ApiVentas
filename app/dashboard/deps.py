import uuid
from fastapi import Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.core.security import decode_token
from app.models.user import User

COOKIE_NAME = "access_token"


def _redirect_to_login() -> HTTPException:
    return HTTPException(status_code=303, headers={"Location": "/dashboard/login"})


async def get_dashboard_user(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> User:
    token = request.cookies.get(COOKIE_NAME)
    if not token:
        raise _redirect_to_login()
    payload = decode_token(token)
    user_id = payload.get("sub")
    if not user_id or payload.get("type") != "access":
        raise _redirect_to_login()
    result = await db.execute(select(User).where(User.id == uuid.UUID(user_id)))
    user = result.scalar_one_or_none()
    if not user or not user.is_active or not user.is_staff:
        raise _redirect_to_login()
    return user
