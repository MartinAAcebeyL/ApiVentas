from decimal import Decimal
import pytest
from pydantic import ValidationError

from app.schemas.imports import ImportCreate, ImportItemCreate, CityDistribution


def _item(quantity=100, distribution=None):
    return ImportItemCreate(
        product_id=1,
        quantity=quantity,
        purchase_cost=Decimal("1000"),
        distribution=distribution or [CityDistribution(city="Sucre", quantity=quantity)],
    )


class TestDistributionValidation:
    def test_distribucion_valida(self):
        item = _item(100, [
            CityDistribution(city="Sucre", quantity=60),
            CityDistribution(city="La Paz", quantity=40),
        ])
        assert item.quantity == 100

    def test_distribucion_no_suma_la_cantidad(self):
        with pytest.raises(ValidationError, match="debe sumar"):
            _item(100, [CityDistribution(city="Sucre", quantity=50)])

    def test_distribucion_excede_la_cantidad(self):
        with pytest.raises(ValidationError, match="debe sumar"):
            _item(100, [
                CityDistribution(city="Sucre", quantity=80),
                CityDistribution(city="La Paz", quantity=40),
            ])

    def test_cantidad_por_ciudad_debe_ser_positiva(self):
        with pytest.raises(ValidationError):
            CityDistribution(city="Sucre", quantity=0)


class TestImportCreate:
    def test_lote_requiere_al_menos_un_item(self):
        with pytest.raises(ValidationError):
            ImportCreate(name="Lote vacío", shipping_cost=Decimal("0"), items=[])

    def test_envio_no_negativo(self):
        with pytest.raises(ValidationError):
            ImportCreate(name="Lote", shipping_cost=Decimal("-1"), items=[_item()])
