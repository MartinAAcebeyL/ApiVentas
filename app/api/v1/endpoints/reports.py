from datetime import date, timedelta
from io import BytesIO
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from jinja2 import Environment, FileSystemLoader, select_autoescape
from xhtml2pdf import pisa
import os

from app.db.session import get_db
from app.core.deps import get_current_admin
from app.models.user import User
from app.models.sale import Sale, SaleDetail, Shipment
from app.models.product import Product, Category, Stock
from app.usecases.graphic_report import CreateGraphicReportUseCase

router = APIRouter()

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "templates")


def _get_date_minus_period(period: int, per: str) -> date:
    today = date.today()
    if per == "day":
        return today - timedelta(days=period)
    elif per == "month":
        return today - timedelta(days=period * 30)
    elif per == "year":
        return today - timedelta(days=period * 365)
    raise HTTPException(status_code=400, detail="per must be 'day', 'month', or 'year'")


@router.get("/sales/reports/graphic")
async def graphic_report(
    period: int,
    per: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    start_date = _get_date_minus_period(period, per)
    uc = CreateGraphicReportUseCase(db, start_date, date.today())
    return {
        "sales_over_time": await uc.get_sales_over_time(),
        "sales_by_category": await uc.get_sales_by_categories(),
        "sales_by_product": await uc.get_sales_by_products(),
        "count_payment_method_usage": await uc.count_payment_method_usage(),
    }


@router.get("/sales/reports/pdf")
async def pdf_report(
    start_date: date = Query(...),
    end_date: date = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    if start_date > end_date or end_date > date.today():
        raise HTTPException(status_code=400, detail="Invalid date range")

    categories_result = await db.execute(select(Category))
    categories = categories_result.scalars().all()

    total_general = 0.0
    categories_data = []

    for cat in categories:
        # Ventas de esta categoría en el rango
        sales_q = await db.execute(
            select(SaleDetail, Product, Sale, Shipment)
            .join(Sale, SaleDetail.sale_id == Sale.id)
            .join(Product, Sale.product_id == Product.id)
            .outerjoin(Shipment, Shipment.sale_id == Sale.id)
            .where(Product.category_id == cat.id)
            .where(SaleDetail.created_at.between(start_date, end_date))
        )
        rows = sales_q.all()
        if not rows:
            continue

        total_sales = sum(float(r.SaleDetail.total) for r in rows)
        total_shipment = sum(float(r.Shipment.shipment_cost) if r.Shipment else 0 for r in rows)
        total_general += total_sales

        # Stock de esta categoría
        stock_q = await db.execute(
            select(func.sum(Stock.current_quantity), func.sum(Stock.quantity))
            .join(Product, Stock.product_id == Product.id)
            .where(Product.category_id == cat.id)
        )
        stock_row = stock_q.first()

        products_detail = [
            {
                "name": r.Product.name,
                "shipment_dest": r.Shipment.departament if r.Shipment else "N/A",
                "shipment_cost": float(r.Shipment.shipment_cost) if r.Shipment else 0,
                "quantity": r.SaleDetail.quantity,
                "total": float(r.SaleDetail.total),
            }
            for r in rows
        ]

        categories_data.append({
            "name": cat.name,
            "total_sales": total_sales,
            "total_shipment_cost": total_shipment,
            "current_quantity": stock_row[0] or 0,
            "quantity": stock_row[1] or 0,
            "products": products_detail,
        })

    env = Environment(
        loader=FileSystemLoader(TEMPLATES_DIR),
        autoescape=select_autoescape(["html"]),
    )
    template = env.get_template("sales_report.html")
    html = template.render(
        nombre_solicitante=current_user.first_name,
        start_date=str(start_date),
        end_date=str(end_date),
        date=date.today().strftime("%d-%m-%Y"),
        sales=total_general,
        categories=categories_data,
    )

    buf = BytesIO()
    pisa.CreatePDF(html, dest=buf)
    buf.seek(0)
    return StreamingResponse(
        buf,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=sales_report.pdf"},
    )
