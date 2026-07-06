# ApiVentas — FastAPI

API + dashboard para registro de ventas por **lotes de importación**: costos unitarios, recuperación de inversión y stock por ciudad. Construida con **FastAPI + SQLAlchemy 2.0 async + PostgreSQL**.

## Requisitos previos

- Docker y Docker Compose

## Instalación y arranque

```bash
git clone https://github.com/MartinAAcebeyL/ApiVentas.git
cd ApiVentas
cp .env.example .env   # editar credenciales
docker compose up --build

# API:       http://localhost:8000/docs
# Dashboard: http://localhost:8000/dashboard
```

## Esquema de base de datos

El proyecto **no ejecuta migraciones**: el esquema se administra directamente en la BD aplicando los scripts de `db/schema/` en orden:

```bash
psql "$DATABASE_URL" -f db/schema/001_initial.sql
psql "$DATABASE_URL" -f db/schema/002_lotes_importacion.sql
```

## Concepto: lotes de importación

Un **lote** agrupa los productos comprados juntos (como una hoja del Excel):

- El **costo de envío del lote** se reparte en partes iguales entre los tipos de producto.
- `costo unitario = (costo_compra + envío/n_tipos) / cantidad` — se calcula y guarda al crear el lote.
- El stock se asigna **por ciudad** al crear el lote; cada venta descuenta de un ítem+ciudad.
- La **recuperación de inversión** compara lo vendido (sin envío al cliente) contra lo invertido.

## Endpoints principales

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/v1/auth/login` | Login (JWT) |
| POST | `/api/v1/imports/` | Crear lote (ítems + reparto por ciudad) |
| GET | `/api/v1/imports/` | Lotes con resumen de recuperación |
| GET | `/api/v1/imports/{id}/metrics` | Métricas completas del lote |
| POST | `/api/v1/sales/` | Registrar venta (descuenta stock de ciudad) |
| GET | `/api/v1/stock/by-city` | Stock por ciudad (filtros: lote, producto, ciudad) |
| GET | `/api/v1/sales/reports/graphic` | Reporte gráfico |
| GET | `/api/v1/sales/reports/pdf` | Reporte PDF |

## Dashboard

Interfaz web servida por la misma app (Jinja2, login con cookie):

- `/dashboard` — lotes con barra de recuperación de inversión
- `/dashboard/imports/{id}` — métricas del lote, stock por ciudad, ventas
- `/dashboard/sales/new` — registrar venta
- `/dashboard/imports/new/form` — registrar lote nuevo

## Tests

```bash
# Unit tests (sin DB)
pytest tests/test_import_costs.py tests/test_import_schemas.py

# Integración (requiere Postgres con esquema aplicado)
docker run -d --rm --name apiventas_test_db -e POSTGRES_PASSWORD=test \
    -e POSTGRES_DB=apiventas_test -p 55432:5432 postgres:16-alpine
# aplicar db/schema/*.sql y luego:
pytest tests/
```

## Stack

- FastAPI + Uvicorn · SQLAlchemy 2.0 async · PostgreSQL 16
- Pydantic v2 · JWT (python-jose) · Jinja2 · xhtml2pdf
