from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.sale import Sale, SaleDetail
from app.models.product import Product, Category, Stock


class CreateGraphicReportUseCase:
    def __init__(self, db: AsyncSession, start_date: date, end_date: date):
        self.db = db
        self.start_date = start_date
        self.end_date = end_date

    async def get_sales_over_time(self) -> list[dict]:
        result = await self.db.execute(
            select(SaleDetail.created_at, func.sum(SaleDetail.total).label("total"))
            .where(SaleDetail.created_at.between(self.start_date, self.end_date))
            .group_by(SaleDetail.created_at)
            .order_by(SaleDetail.created_at)
        )
        return [{"date": str(r.created_at), "total": float(r.total)} for r in result.all()]

    async def get_sales_by_categories(self) -> list[dict]:
        result = await self.db.execute(
            select(
                Category.name.label("category"),
                func.sum(SaleDetail.total).label("total"),
                func.count(SaleDetail.id).label("count"),
            )
            .join(Sale, SaleDetail.sale_id == Sale.id)
            .join(Product, Sale.product_id == Product.id)
            .join(Category, Product.category_id == Category.id)
            .where(SaleDetail.created_at.between(self.start_date, self.end_date))
            .group_by(Category.name)
        )
        return [{"category": r.category, "total": float(r.total), "count": r.count} for r in result.all()]

    async def get_sales_by_products(self) -> list[dict]:
        result = await self.db.execute(
            select(
                Product.name.label("product"),
                func.sum(SaleDetail.total).label("total"),
                func.count(SaleDetail.id).label("count"),
            )
            .join(Sale, SaleDetail.sale_id == Sale.id)
            .join(Product, Sale.product_id == Product.id)
            .where(SaleDetail.created_at.between(self.start_date, self.end_date))
            .group_by(Product.name)
        )
        return [{"product": r.product, "total": float(r.total), "count": r.count} for r in result.all()]

    async def count_payment_method_usage(self) -> list[dict]:
        result = await self.db.execute(
            select(SaleDetail.payment_method, func.count(SaleDetail.id).label("count"))
            .where(SaleDetail.created_at.between(self.start_date, self.end_date))
            .group_by(SaleDetail.payment_method)
        )
        return [{"method": r.payment_method, "count": r.count} for r in result.all()]
