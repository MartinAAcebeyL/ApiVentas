from decimal import Decimal
from datetime import date
from pydantic import BaseModel, Field, model_validator


class CityDistribution(BaseModel):
    city: str
    quantity: int = Field(gt=0)


class ImportItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)
    purchase_cost: Decimal = Field(ge=0)
    distribution: list[CityDistribution]

    @model_validator(mode="after")
    def distribution_matches_quantity(self):
        total = sum(d.quantity for d in self.distribution)
        if total != self.quantity:
            raise ValueError(
                f"la distribución por ciudades suma {total}, debe sumar {self.quantity}"
            )
        return self


class ImportCreate(BaseModel):
    name: str
    shipping_cost: Decimal = Field(ge=0, default=Decimal("0"))
    notes: str | None = None
    items: list[ImportItemCreate] = Field(min_length=1)


class ImportUpdate(BaseModel):
    name: str | None = None
    shipping_cost: Decimal | None = Field(ge=0, default=None)
    notes: str | None = None


class CityStockRead(BaseModel):
    city: str
    quantity: int
    model_config = {"from_attributes": True}


class ImportItemRead(BaseModel):
    id: int
    product_id: int
    product_name: str | None = None
    quantity: int
    purchase_cost: Decimal
    unit_cost: Decimal
    city_stocks: list[CityStockRead] = []
    model_config = {"from_attributes": True}


class ImportRead(BaseModel):
    id: int
    name: str
    shipping_cost: Decimal
    notes: str | None
    created_at: date
    items: list[ImportItemRead] = []
    model_config = {"from_attributes": True}


class ImportSummary(BaseModel):
    id: int
    name: str
    created_at: date
    investment: Decimal
    recovered: Decimal
    remaining_to_recover: Decimal
    recovery_pct: float


class ItemMetrics(BaseModel):
    import_item_id: int
    product_name: str
    quantity_bought: int
    quantity_sold: int
    quantity_remaining: int
    remaining_by_city: dict[str, int]
    unit_cost: Decimal
    avg_sale_price: Decimal | None
    profit_per_unit: Decimal | None


class SaleSummary(BaseModel):
    date: date
    seller: str
    product_name: str
    city: str | None
    quantity: int
    unit_price: Decimal
    total: Decimal


class ImportMetrics(BaseModel):
    import_id: int
    name: str
    investment: Decimal
    recovered: Decimal
    remaining_to_recover: Decimal
    recovery_pct: float
    items: list[ItemMetrics]
    sales: list[SaleSummary]
