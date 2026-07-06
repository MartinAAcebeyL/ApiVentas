from decimal import Decimal
import pytest

from app.usecases.import_costs import compute_unit_cost, compute_investment


class TestComputeUnitCost:
    def test_ejemplo_del_negocio(self):
        # Lote con 3 tipos de producto, envío 300 → cada tipo absorbe 100.
        # Relojes: costo 3000 + 100 = 3100, 100 unidades → 31 Bs/u
        assert compute_unit_cost(Decimal("3000"), Decimal("300"), 3, 100) == Decimal("31.0000")

    def test_un_solo_producto_absorbe_todo_el_envio(self):
        assert compute_unit_cost(Decimal("500"), Decimal("100"), 1, 10) == Decimal("60.0000")

    def test_sin_envio(self):
        assert compute_unit_cost(Decimal("250"), Decimal("0"), 2, 10) == Decimal("25.0000")

    def test_redondeo_half_up_a_4_decimales(self):
        # (100 + 0) / 3 = 33.3333...
        assert compute_unit_cost(Decimal("100"), Decimal("0"), 1, 3) == Decimal("33.3333")
        # (100 + 50/2) / 6 = 125/6 = 20.83333... → 20.8333
        assert compute_unit_cost(Decimal("100"), Decimal("50"), 2, 6) == Decimal("20.8333")

    def test_quantity_cero_invalida(self):
        with pytest.raises(ValueError):
            compute_unit_cost(Decimal("100"), Decimal("0"), 1, 0)

    def test_n_items_cero_invalido(self):
        with pytest.raises(ValueError):
            compute_unit_cost(Decimal("100"), Decimal("0"), 0, 10)


class TestComputeInvestment:
    def test_suma_costos_mas_envio(self):
        assert compute_investment(
            [Decimal("3000"), Decimal("1500")], Decimal("300")
        ) == Decimal("4800")

    def test_sin_items(self):
        assert compute_investment([], Decimal("100")) == Decimal("100")
