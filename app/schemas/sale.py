from decimal import Decimal
from datetime import date
from pydantic import BaseModel, Field
from app.models.sale import PaymentMethod, ShipmentStatus, Departament


class ShipmentCreate(BaseModel):
    departament: Departament
    city: str = "Sucre"
    shipment_cost: Decimal = Field(ge=0)
    description: str | None = None


class SaleCreate(BaseModel):
    import_item_id: int
    city: str
    quantity: int = Field(gt=0)
    unit_price: Decimal = Field(gt=0)
    payment_method: PaymentMethod = PaymentMethod.cash
    shipment: ShipmentCreate | None = None


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
    import_item_id: int | None
    city: str | None
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
