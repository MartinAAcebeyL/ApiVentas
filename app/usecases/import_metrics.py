from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.models.imports import Import, ImportItem, CityStock
from app.models.sale import Sale, SaleDetail
from app.models.product import Product
from app.models.user import User
from app.usecases.import_costs import compute_investment
from app.schemas.imports import (
    ImportMetrics, ImportSummary, ItemMetrics, SaleSummary,
)


class ImportMetricsUseCase:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def _recovered_by_import(self, import_id: int) -> Decimal:
        """Ventas acumuladas del lote: solo precio de venta, sin envío al cliente."""
        result = await self.db.execute(
            select(func.coalesce(func.sum(SaleDetail.total), 0))
            .join(Sale, SaleDetail.sale_id == Sale.id)
            .join(ImportItem, Sale.import_item_id == ImportItem.id)
            .where(ImportItem.import_id == import_id)
        )
        return Decimal(result.scalar_one())

    async def summary(self, imp: Import) -> ImportSummary:
        investment = compute_investment(
            [i.purchase_cost for i in imp.items], imp.shipping_cost
        )
        recovered = await self._recovered_by_import(imp.id)
        remaining = investment - recovered
        pct = float(recovered / investment * 100) if investment else 0.0
        return ImportSummary(
            id=imp.id,
            name=imp.name,
            created_at=imp.created_at,
            investment=investment,
            recovered=recovered,
            remaining_to_recover=remaining,
            recovery_pct=round(pct, 2),
        )

    async def metrics(self, import_id: int) -> ImportMetrics | None:
        result = await self.db.execute(
            select(Import)
            .where(Import.id == import_id)
            .options(
                selectinload(Import.items).selectinload(ImportItem.city_stocks),
                selectinload(Import.items).selectinload(ImportItem.product),
            )
        )
        imp = result.scalar_one_or_none()
        if not imp:
            return None

        summary = await self.summary(imp)

        items_metrics: list[ItemMetrics] = []
        for item in imp.items:
            sold_result = await self.db.execute(
                select(
                    func.coalesce(func.sum(SaleDetail.quantity), 0),
                    func.coalesce(func.sum(SaleDetail.total), 0),
                )
                .join(Sale, SaleDetail.sale_id == Sale.id)
                .where(Sale.import_item_id == item.id)
            )
            qty_sold, revenue = sold_result.one()
            remaining_by_city = {cs.city: cs.quantity for cs in item.city_stocks}
            avg_price = (Decimal(revenue) / qty_sold) if qty_sold else None
            items_metrics.append(ItemMetrics(
                import_item_id=item.id,
                product_name=item.product.name,
                quantity_bought=item.quantity,
                quantity_sold=qty_sold,
                quantity_remaining=sum(remaining_by_city.values()),
                remaining_by_city=remaining_by_city,
                unit_cost=item.unit_cost,
                avg_sale_price=avg_price,
                profit_per_unit=(avg_price - item.unit_cost) if avg_price is not None else None,
            ))

        sales_result = await self.db.execute(
            select(SaleDetail, Sale, Product.name, User.username)
            .join(Sale, SaleDetail.sale_id == Sale.id)
            .join(ImportItem, Sale.import_item_id == ImportItem.id)
            .join(Product, ImportItem.product_id == Product.id)
            .join(User, Sale.seller_id == User.id)
            .where(ImportItem.import_id == import_id)
            .order_by(SaleDetail.created_at.desc())
        )
        sales = [
            SaleSummary(
                date=r.SaleDetail.created_at,
                seller=r.username,
                product_name=r.name,
                city=r.Sale.city,
                quantity=r.SaleDetail.quantity,
                unit_price=r.SaleDetail.unit_price,
                total=r.SaleDetail.total,
            )
            for r in sales_result.all()
        ]

        return ImportMetrics(
            import_id=imp.id,
            name=imp.name,
            investment=summary.investment,
            recovered=summary.recovered,
            remaining_to_recover=summary.remaining_to_recover,
            recovery_pct=summary.recovery_pct,
            items=items_metrics,
            sales=sales,
        )
