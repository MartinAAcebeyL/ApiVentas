from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.core.deps import get_current_admin
from app.models.user import User
from app.models.product import Product, Stock
from app.models.sale import Sale, SaleDetail
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
    # Verificar que el producto existe
    product_result = await db.execute(select(Product).where(Product.id == payload.product_id))
    product = product_result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Obtener stock del producto
    stock_result = await db.execute(select(Stock).where(Stock.product_id == payload.product_id))
    stock = stock_result.scalar_one_or_none()
    if not stock or stock.current_quantity < payload.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    # Decrementar stock
    stock.current_quantity -= payload.quantity
    stock.updated_at = date.today()

    # Crear Sale
    sale = Sale(seller_id=current_user.id, product_id=payload.product_id)
    db.add(sale)
    await db.flush()  # obtener sale.id sin cerrar transacción

    # Crear SaleDetail
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
    await db.commit()
    await db.refresh(sale)

    # Alerta de stock mínimo (equivalente al signal check_minimum_stock de Django)
    if stock.current_quantity <= product.minimum_stock:
        send_email(
            subject=f"Stock mínimo alcanzado: {product.name}",
            message=(
                f"El producto '{product.name}' ha alcanzado el stock mínimo.\n"
                f"Stock actual: {stock.current_quantity} | Mínimo: {product.minimum_stock}"
            ),
            to_emails=STOCK_ALERT_EMAILS,
        )

    return sale
