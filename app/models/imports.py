from decimal import Decimal
from datetime import date
from sqlalchemy import String, Text, Integer, Numeric, ForeignKey, Date, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Import(Base):
    """Lote de importación: agrupa productos comprados juntos y reparte el envío."""
    __tablename__ = "imports"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    shipping_cost: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=0)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[date] = mapped_column(Date, nullable=False)

    items: Mapped[list["ImportItem"]] = relationship(
        "ImportItem", back_populates="import_", cascade="all, delete-orphan"
    )


class ImportItem(Base):
    __tablename__ = "import_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    import_id: Mapped[int] = mapped_column(ForeignKey("imports.id", ondelete="CASCADE"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    purchase_cost: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    unit_cost: Mapped[Decimal] = mapped_column(Numeric(10, 4), nullable=False)

    import_: Mapped["Import"] = relationship("Import", back_populates="items")
    product: Mapped["Product"] = relationship("Product")  # noqa: F821
    city_stocks: Mapped[list["CityStock"]] = relationship(
        "CityStock", back_populates="import_item", cascade="all, delete-orphan"
    )


class CityStock(Base):
    __tablename__ = "city_stocks"
    __table_args__ = (UniqueConstraint("import_item_id", "city"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    import_item_id: Mapped[int] = mapped_column(
        ForeignKey("import_items.id", ondelete="CASCADE"), nullable=False
    )
    city: Mapped[str] = mapped_column(String(255), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    import_item: Mapped["ImportItem"] = relationship("ImportItem", back_populates="city_stocks")
