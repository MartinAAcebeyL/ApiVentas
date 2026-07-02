from decimal import Decimal
from datetime import date
import uuid
from sqlalchemy import String, Integer, Numeric, ForeignKey, Date, Text, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base
import enum


class PaymentMethod(str, enum.Enum):
    cash = "cash"
    qr = "qr"
    transfer = "transfer"


class ShipmentStatus(str, enum.Enum):
    pending = "pending"
    in_transit = "in_transit"
    delivered = "delivered"


class Departament(str, enum.Enum):
    la_paz = "La Paz"
    cochabamba = "Cochabamba"
    santa_cruz = "Santa Cruz"
    oruro = "Oruro"
    potosi = "Potosi"
    tarija = "Tarija"
    beni = "Beni"
    pando = "Pando"
    chuquisaca = "Chuquisaca"


class Sale(Base):
    __tablename__ = "sales"

    id: Mapped[int] = mapped_column(primary_key=True)
    seller_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)

    seller: Mapped["User"] = relationship("User", back_populates="sales")  # noqa: F821
    product: Mapped["Product"] = relationship("Product")  # noqa: F821
    detail: Mapped["SaleDetail"] = relationship("SaleDetail", back_populates="sale", uselist=False)
    shipment: Mapped["Shipment | None"] = relationship("Shipment", back_populates="sale", uselist=False)


class SaleDetail(Base):
    __tablename__ = "sales_details"

    id: Mapped[int] = mapped_column(primary_key=True)
    sale_id: Mapped[int] = mapped_column(ForeignKey("sales.id"), unique=True, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    total: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    payment_method: Mapped[PaymentMethod] = mapped_column(SAEnum(PaymentMethod), nullable=False)
    created_at: Mapped[date] = mapped_column(Date, nullable=False)
    updated_at: Mapped[date] = mapped_column(Date, nullable=False)

    sale: Mapped["Sale"] = relationship("Sale", back_populates="detail")


class Shipment(Base):
    __tablename__ = "shipments"

    id: Mapped[int] = mapped_column(primary_key=True)
    sale_id: Mapped[int] = mapped_column(ForeignKey("sales.id"), unique=True, nullable=False)
    departament: Mapped[Departament] = mapped_column(SAEnum(Departament), nullable=False)
    city: Mapped[str] = mapped_column(String(255), default="Sucre", nullable=False)
    shipment_cost: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    status: Mapped[ShipmentStatus] = mapped_column(SAEnum(ShipmentStatus), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[date] = mapped_column(Date, nullable=False)

    sale: Mapped["Sale"] = relationship("Sale", back_populates="shipment")
