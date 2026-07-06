## Stack

FastAPI + SQLAlchemy 2.0 async + PostgreSQL. El proyecto vive en la raíz — no hay subcarpetas de apps Django.

**Sin migraciones automáticas:** el esquema se administra con scripts SQL planos en `db/schema/` aplicados manualmente a la BD (decisión del dueño del proyecto — no reintroducir Alembic).

## Dominio: lotes de importación

- `Import` (lote) agrupa productos comprados juntos; el envío del lote se reparte en partes iguales entre tipos de producto.
- `unit_cost = (purchase_cost + shipping_cost/n_items) / quantity` — calculado en `app/usecases/import_costs.py`, guardado fijo en `ImportItem`.
- Stock por ciudad (`CityStock`); cada venta descuenta de ítem+ciudad. No existe stock global (el modelo `Stock` fue eliminado).
- Recuperación de inversión = ventas del lote (solo precio, sin envío al cliente) vs inversión (costos + envío del lote).
- Spec completo: `docs/superpowers/specs/2026-07-06-lotes-importacion-design.md`

## Arranque local

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # editar credenciales
psql "$DATABASE_URL" -f db/schema/001_initial.sql   # y 002, en orden
uvicorn app.main:app --reload
```

## Estructura

```
app/
  api/v1/endpoints/   # auth.py, sales.py, reports.py, users.py, imports.py, stock.py
  core/               # config.py, security.py, deps.py
  dashboard/          # routes.py, deps.py (cookie JWT), templates/ (Jinja2)
  db/                 # base.py, session.py
  models/             # user.py, product.py, sale.py, imports.py
  schemas/            # product.py, user.py, sale.py, imports.py
  usecases/           # import_costs.py, import_metrics.py, graphic_report.py, sales_by_user.py
  utils/              # email.py
  templates/          # sales_report.html (Jinja2, para PDF)
db/schema/            # scripts SQL del esquema (aplicar manualmente)
scripts/              # migrate_data.py (Django → FastAPI)
tests/                # unit (costos, schemas) + integración (requiere Postgres)
```

## Tests

```bash
pytest tests/test_import_costs.py tests/test_import_schemas.py   # sin DB
# integración: Postgres en :55432 con esquema aplicado (ver README)
```

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
- graphify is installed in `.venv` — activate it first: `source .venv/bin/activate`
