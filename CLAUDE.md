## Stack

FastAPI + SQLAlchemy 2.0 async + Alembic + PostgreSQL. El proyecto vive en la raíz — no hay subcarpetas de apps Django.

## Arranque local

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # editar credenciales
alembic upgrade head
uvicorn app.main:app --reload
```

## Estructura

```
app/
  api/v1/endpoints/   # auth.py, sales.py, reports.py, users.py
  core/               # config.py, security.py, deps.py
  db/                 # base.py, session.py
  models/             # user.py, product.py, sale.py
  schemas/            # product.py, user.py, sale.py
  usecases/           # graphic_report.py, sales_by_user.py
  utils/              # email.py
  templates/          # sales_report.html (Jinja2, para PDF)
alembic/versions/     # migraciones
scripts/              # migrate_data.py (Django → FastAPI)
tests/
```

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
- graphify is installed in `.venv` — activate it first: `source .venv/bin/activate`
