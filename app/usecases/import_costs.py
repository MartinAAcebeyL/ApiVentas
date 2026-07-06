"""Cálculo de costos de lote.

Regla del negocio: el envío del lote se reparte en partes iguales entre los
tipos de producto (no por unidades ni por valor), y el costo unitario sale de:

    unit_cost = (purchase_cost + shipping_cost / n_items) / quantity
"""
from decimal import Decimal, ROUND_HALF_UP

UNIT_COST_PLACES = Decimal("0.0001")


def compute_unit_cost(
    purchase_cost: Decimal, shipping_cost: Decimal, n_items: int, quantity: int
) -> Decimal:
    if n_items <= 0:
        raise ValueError("n_items debe ser mayor a 0")
    if quantity <= 0:
        raise ValueError("quantity debe ser mayor a 0")
    shipping_share = Decimal(shipping_cost) / n_items
    total = Decimal(purchase_cost) + shipping_share
    return (total / quantity).quantize(UNIT_COST_PLACES, rounding=ROUND_HALF_UP)


def compute_investment(purchase_costs: list[Decimal], shipping_cost: Decimal) -> Decimal:
    return sum(purchase_costs, Decimal("0")) + Decimal(shipping_cost)
