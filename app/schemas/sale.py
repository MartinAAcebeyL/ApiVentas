from decimal import Decimal
from datetime import date
from pydantic import BaseModel
from app.models.sale import PaymentMethod, ShipmentStatus, Departament


class SaleCreate(BaseModel):
    product_id: int
    quantity: int
    unit_price: Decimal
    payment_method: PaymentMethod


class SaleDetailRead(BaseModel):
    id: int
    sale_id: int
    quantity: int
    total: Decimal
    unit_price: Decimal
    payment_method: PaymentMethod
    created_at: date
    updated_at: date
    model_config = {"from_attributes": True}


class SaleRead(BaseModel):
    id: int
    seller_id: str
    product_id: int
    detail: SaleDetailRead | None = None
    model_config = {"from_attributes": True}


class ShowSaleRead(BaseModel):
    quantity: int
    total: Decimal
    unit_price: Decimal
    payment_method: PaymentMethod
    created_at: date
    updated_at: date
    product_name: str | None = None
    category_name: str | None = None
    model_config = {"from_attributes": True}
