from datetime import date
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from app.db.session import get_db
from app.core.deps import get_current_admin
from app.models.user import User
from app.models.sale import Sale, SaleDetail
from app.models.product import Product, Category
from app.schemas.sale import ShowSaleRead
from app.usecases.sales_by_user import GetSalesByUser

router = APIRouter()


@router.get("/sales/filter", response_model=list[ShowSaleRead])
async def filter_sales(
    sort: Optional[str] = Query("ASC", pattern="^(ASC|DESC)$"),
    categories: Optional[list[int]] = Query(None),
    start_date: Optional[date] = Query(None),
    finish_date: Optional[date] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    q = (
        select(SaleDetail, Product.name.label("product_name"), Category.name.label("category_name"))
        .join(Sale, SaleDetail.sale_id == Sale.id)
        .join(Product, Sale.product_id == Product.id)
        .join(Category, Product.category_id == Category.id)
        .where(Sale.seller_id == current_user.id)
    )

    if categories:
        q = q.where(Product.category_id.in_(categories))
    if start_date:
        q = q.where(SaleDetail.created_at >= start_date)
    if finish_date:
        q = q.where(SaleDetail.created_at <= finish_date)

    q = q.order_by(Category.name.asc() if sort == "ASC" else Category.name.desc())

    result = await db.execute(q)
    rows = result.all()

    return [
        ShowSaleRead(
            quantity=r.SaleDetail.quantity,
            total=r.SaleDetail.total,
            unit_price=r.SaleDetail.unit_price,
            payment_method=r.SaleDetail.payment_method,
            created_at=r.SaleDetail.created_at,
            updated_at=r.SaleDetail.updated_at,
            product_name=r.product_name,
            category_name=r.category_name,
        )
        for r in rows
    ]


@router.get("/users/me/sales")
async def me_sales(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    uc = GetSalesByUser(db)
    return await uc.get_sales_by_seller(current_user.id)
