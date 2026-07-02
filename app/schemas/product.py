from decimal import Decimal
from datetime import date
from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str
    description: str


class CategoryCreate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    id: int
    created_at: date
    updated_at: date
    model_config = {"from_attributes": True}


class ProductBase(BaseModel):
    name: str
    description: str
    weight: int
    price: Decimal
    minimum_stock: Decimal
    category_id: int


class ProductCreate(ProductBase):
    pass


class ProductRead(ProductBase):
    id: int
    category: CategoryRead
    model_config = {"from_attributes": True}


class StockRead(BaseModel):
    id: int
    product_id: int
    quantity: int
    current_quantity: int
    created_at: date
    updated_at: date
    model_config = {"from_attributes": True}
