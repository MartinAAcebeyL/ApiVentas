from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.db.session import get_db
from app.core.deps import get_current_admin
from app.models.user import User
from app.models.product import Product
from app.models.imports import ImportItem, CityStock
from app.models.sale import Sale, SaleDetail, Shipment, ShipmentStatus
from app.schemas.sale import SaleCreate, SaleRead
from app.utils.email import send_email

router = APIRouter()

STOCK_ALERT_EMAILS = ["martinaacbyl2000@gmail.com", "alexysdenka@gmail.com"]


@router.post("/sales/", response_model=SaleRead, status_code=status.HTTP_201_CREATED)
async def create_sale(
    payload: SaleCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    item_result = await db.execute(
        select(ImportItem).where(ImportItem.id == payload.import_item_id)
    )
    item = item_result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Ítem de lote no encontrado")

    stock_result = await db.execute(
        select(CityStock).where(
            CityStock.import_item_id == item.id, CityStock.city == payload.city
        )
    )
    city_stock = stock_result.scalar_one_or_none()
    if not city_stock:
        raise HTTPException(
            status_code=404,
            detail=f"No hay registro de stock para este ítem en {payload.city}",
        )
    if city_stock.quantity < payload.quantity:
        raise HTTPException(
            status_code=400,
            detail=f"Stock insuficiente en {payload.city}: disponible {city_stock.quantity}, pedido {payload.quantity}",
        )

    city_stock.quantity -= payload.quantity

    sale = Sale(
        seller_id=current_user.id,
        product_id=item.product_id,
        import_item_id=item.id,
        city=payload.city,
    )
    db.add(sale)
    await db.flush()

    detail = SaleDetail(
        sale_id=sale.id,
        quantity=payload.quantity,
        unit_price=payload.unit_price,
        total=payload.unit_price * payload.quantity,
        payment_method=payload.payment_method,
        created_at=date.today(),
        updated_at=date.today(),
    )
    db.add(detail)

    if payload.shipment:
        db.add(Shipment(
            sale_id=sale.id,
            departament=payload.shipment.departament,
            city=payload.shipment.city,
            shipment_cost=payload.shipment.shipment_cost,
            status=ShipmentStatus.pending,
            description=payload.shipment.description,
            created_at=date.today(),
        ))

    await db.commit()
    await db.refresh(sale)

    # Alerta de stock mínimo: total restante del producto en todos los lotes/ciudades
    product = (
        await db.execute(select(Product).where(Product.id == item.product_id))
    ).scalar_one()
    total_remaining = (
        await db.execute(
            select(func.coalesce(func.sum(CityStock.quantity), 0))
            .join(ImportItem, CityStock.import_item_id == ImportItem.id)
            .where(ImportItem.product_id == product.id)
        )
    ).scalar_one()
    if total_remaining <= product.minimum_stock:
        send_email(
            subject=f"Stock mínimo alcanzado: {product.name}",
            message=(
                f"El producto '{product.name}' ha alcanzado el stock mínimo.\n"
                f"Stock total restante: {total_remaining} | Mínimo: {product.minimum_stock}"
            ),
            to_emails=STOCK_ALERT_EMAILS,
        )

    return SaleRead(
        id=sale.id,
        seller_id=str(sale.seller_id),
        product_id=sale.product_id,
        import_item_id=sale.import_item_id,
        city=sale.city,
    )
