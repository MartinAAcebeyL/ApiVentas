from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.core.deps import get_current_admin
from app.models.user import User
from app.models.product import Product
from app.models.imports import Import, ImportItem, CityStock

router = APIRouter()


@router.get("/stock/by-city")
async def stock_by_city(
    import_id: int | None = Query(None),
    product_id: int | None = Query(None),
    city: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    q = (
        select(
            CityStock.city,
            CityStock.quantity,
            Product.name.label("product_name"),
            Import.name.label("import_name"),
            ImportItem.id.label("import_item_id"),
            ImportItem.unit_cost,
        )
        .join(ImportItem, CityStock.import_item_id == ImportItem.id)
        .join(Product, ImportItem.product_id == Product.id)
        .join(Import, ImportItem.import_id == Import.id)
    )
    if import_id is not None:
        q = q.where(Import.id == import_id)
    if product_id is not None:
        q = q.where(Product.id == product_id)
    if city is not None:
        q = q.where(CityStock.city == city)

    result = await db.execute(q.order_by(CityStock.city, Product.name))
    return [
        {
            "city": r.city,
            "product_name": r.product_name,
            "import_name": r.import_name,
            "import_item_id": r.import_item_id,
            "quantity": r.quantity,
            "unit_cost": float(r.unit_cost),
        }
        for r in result.all()
    ]
