import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.sale import Sale, SaleDetail
from app.models.product import Product, Category


class GetSalesByUser:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_sales_by_seller(self, seller_id: uuid.UUID) -> list[dict]:
        result = await self.db.execute(
            select(
                Category.name.label("category_name"),
                func.sum(SaleDetail.total).label("sales"),
                func.sum(SaleDetail.quantity).label("quantity"),
                func.max(SaleDetail.created_at).label("last_sale_date"),
                Product.name.label("product_name"),
                SaleDetail.created_at,
                SaleDetail.quantity.label("qty"),
            )
            .join(Sale, SaleDetail.sale_id == Sale.id)
            .join(Product, Sale.product_id == Product.id)
            .join(Category, Product.category_id == Category.id)
            .where(Sale.seller_id == seller_id)
            .group_by(Category.name, Product.name, SaleDetail.created_at, SaleDetail.quantity)
            .order_by(Category.name)
        )
        rows = result.all()

        categories: dict[str, dict] = {}
        for r in rows:
            cat = r.category_name
            if cat not in categories:
                categories[cat] = {
                    "category_name": cat,
                    "sales": 0.0,
                    "quantity": 0,
                    "last_sale_date": None,
                    "data_sales": {},
                }
            categories[cat]["sales"] += float(r.sales or 0)
            categories[cat]["quantity"] += r.quantity or 0
            if r.last_sale_date and (
                categories[cat]["last_sale_date"] is None
                or r.last_sale_date > categories[cat]["last_sale_date"]
            ):
                categories[cat]["last_sale_date"] = str(r.last_sale_date)

            product = r.product_name
            if product not in categories[cat]["data_sales"]:
                categories[cat]["data_sales"][product] = []
            categories[cat]["data_sales"][product].append(
                {"sale_date": str(r.created_at), "quantity_sold": r.qty}
            )

        return list(categories.values())
