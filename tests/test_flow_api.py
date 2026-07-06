"""Test de integración del flujo lote → venta → métricas.

Requiere Postgres con el esquema aplicado (db/schema/*.sql):
    docker run -d --rm --name apiventas_test_db -e POSTGRES_PASSWORD=test \
        -e POSTGRES_DB=apiventas_test -p 55432:5432 postgres:16-alpine

Se salta automáticamente si TEST_DATABASE_URL no está definida.
"""
import os
import uuid
from datetime import date
from decimal import Decimal

import pytest

TEST_DB = os.environ.get(
    "TEST_DATABASE_URL",
    "postgresql+asyncpg://postgres:test@localhost:55432/apiventas_test",
)
os.environ.setdefault("DATABASE_URL", TEST_DB)
os.environ.setdefault("SECRET_KEY", "test-secret")

import httpx  # noqa: E402
from sqlalchemy import text  # noqa: E402

from app.main import app  # noqa: E402
from app.db.session import AsyncSessionLocal, engine  # noqa: E402
from app.core.deps import get_current_admin  # noqa: E402
from app.models.user import User  # noqa: E402
from app.models.product import Category, Product  # noqa: E402


@pytest.fixture
async def db_ready():
    # El engine global queda ligado al event loop del test anterior; renovarlo
    await engine.dispose()
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
    except Exception:
        pytest.skip("Postgres de prueba no disponible")
    yield
    # limpieza total entre tests
    async with engine.begin() as conn:
        await conn.execute(text(
            "TRUNCATE shipments, sales_details, sales, city_stocks, import_items, "
            "imports, history_prices, products, categories, users CASCADE"
        ))
    await engine.dispose()


@pytest.fixture
async def seed(db_ready):
    async with AsyncSessionLocal() as db:
        user = User(
            id=uuid.uuid4(), username="admin", email="a@a.com",
            password="x", is_staff=True,
        )
        cat = Category(name="Accesorios", description="-", created_at=date.today(), updated_at=date.today())
        db.add_all([user, cat])
        await db.flush()
        p1 = Product(category_id=cat.id, name="Reloj", description="-", weight=1,
                     price=Decimal("100"), minimum_stock=Decimal("2"))
        p2 = Product(category_id=cat.id, name="Manilla", description="-", weight=1,
                     price=Decimal("30"), minimum_stock=Decimal("2"))
        db.add_all([p1, p2])
        await db.commit()
        yield {"user": user, "p1_id": p1.id, "p2_id": p2.id}


@pytest.fixture
async def client(seed):
    app.dependency_overrides[get_current_admin] = lambda: seed["user"]
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()


def _lote_payload(p1_id, p2_id):
    return {
        "name": "Lote test",
        "shipping_cost": "200",
        "items": [
            {
                "product_id": p1_id, "quantity": 10, "purchase_cost": "900",
                "distribution": [{"city": "Sucre", "quantity": 6}, {"city": "La Paz", "quantity": 4}],
            },
            {
                "product_id": p2_id, "quantity": 20, "purchase_cost": "300",
                "distribution": [{"city": "Sucre", "quantity": 20}],
            },
        ],
    }


async def test_flujo_completo(client, seed):
    # 1. Crear lote — unit_cost: relojes (900+100)/10 = 100; manillas (300+100)/20 = 20
    r = await client.post("/api/v1/imports/", json=_lote_payload(seed["p1_id"], seed["p2_id"]))
    assert r.status_code == 201, r.text
    lote = r.json()
    reloj_item = next(i for i in lote["items"] if i["product_id"] == seed["p1_id"])
    manilla_item = next(i for i in lote["items"] if i["product_id"] == seed["p2_id"])
    assert Decimal(reloj_item["unit_cost"]) == Decimal("100.0000")
    assert Decimal(manilla_item["unit_cost"]) == Decimal("20.0000")

    # 2. Vender 2 relojes en Sucre a 150
    r = await client.post("/api/v1/sales/", json={
        "import_item_id": reloj_item["id"], "city": "Sucre",
        "quantity": 2, "unit_price": "150",
    })
    assert r.status_code == 201, r.text

    # 3. Stock insuficiente en La Paz (hay 4)
    r = await client.post("/api/v1/sales/", json={
        "import_item_id": reloj_item["id"], "city": "La Paz",
        "quantity": 5, "unit_price": "150",
    })
    assert r.status_code == 400
    assert "Stock insuficiente" in r.json()["detail"]

    # 4. Ciudad sin registro de stock
    r = await client.post("/api/v1/sales/", json={
        "import_item_id": manilla_item["id"], "city": "La Paz",
        "quantity": 1, "unit_price": "50",
    })
    assert r.status_code == 404

    # 5. Métricas: inversión 900+300+200 = 1400; recuperado 300 (2×150, sin envío)
    r = await client.get(f"/api/v1/imports/{lote['id']}/metrics")
    assert r.status_code == 200
    m = r.json()
    assert Decimal(m["investment"]) == Decimal("1400")
    assert Decimal(m["recovered"]) == Decimal("300")
    assert Decimal(m["remaining_to_recover"]) == Decimal("1100")

    reloj_m = next(i for i in m["items"] if i["product_name"] == "Reloj")
    assert reloj_m["quantity_sold"] == 2
    assert reloj_m["quantity_remaining"] == 8
    assert reloj_m["remaining_by_city"] == {"Sucre": 4, "La Paz": 4}
    assert Decimal(reloj_m["profit_per_unit"]) == Decimal("50")  # 150 - 100

    assert len(m["sales"]) == 1
    assert m["sales"][0]["seller"] == "admin"

    # 6. Stock por ciudad
    r = await client.get("/api/v1/stock/by-city", params={"city": "Sucre"})
    assert r.status_code == 200
    rows = r.json()
    assert {row["product_name"]: row["quantity"] for row in rows} == {"Reloj": 4, "Manilla": 20}


async def test_distribucion_invalida(client, seed):
    payload = _lote_payload(seed["p1_id"], seed["p2_id"])
    payload["items"][0]["distribution"] = [{"city": "Sucre", "quantity": 3}]  # no suma 10
    r = await client.post("/api/v1/imports/", json=payload)
    assert r.status_code == 422
