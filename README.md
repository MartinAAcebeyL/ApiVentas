# ApiVentas — FastAPI

API para registro de ventas y generación de reportes PDF, migrada de Django REST Framework a **FastAPI + SQLAlchemy 2.0 async + Alembic**.

## Requisitos previos

- Docker
- Docker Compose

## Instalación y arranque

```bash
# 1. Clona el repositorio
git clone https://github.com/MartinAAcebeyL/ApiVentas.git
cd ApiVentas/fastapi_app

# 2. Crea tu archivo .env
cp .env.example .env
# Edita .env con tus credenciales

# 3. Levanta los servicios
docker compose up --build

# La API queda disponible en http://localhost:8000
# Documentación interactiva: http://localhost:8000/docs
```

## Migraciones de base de datos

```bash
# Dentro del contenedor
docker compose exec app alembic upgrade head

# O local (con el venv activo y DATABASE_URL en .env)
alembic upgrade head
```

## Endpoints principales

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/health` | Healthcheck |
| POST | `/api/v1/users/` | Registro de vendedor |
| POST | `/api/v1/auth/login` | Login (devuelve JWT) |
| POST | `/api/v1/auth/refresh` | Renovar access token |
| POST | `/api/v1/sales/` | Crear venta |
| GET | `/api/v1/sales/reports/graphic?period=&per=` | Reporte gráfico |
| GET | `/api/v1/sales/reports/pdf?start_date=&end_date=` | Reporte PDF |
| GET | `/api/v1/sales/filter` | Filtrar ventas |
| GET | `/api/v1/users/me/sales` | Ventas del vendedor actual |

## Migración de datos desde Django

Si tenés datos en la base de datos de Django y querés migrarlos:

```bash
# 1. Asegúrate de que el target ya tiene el schema (alembic upgrade head)
# 2. Ejecuta el script de migración
python scripts/migrate_data.py \
    --source "postgresql://user:pass@host:port/django_db" \
    --target "postgresql://user:pass@host:port/fastapi_db"
```

El script migra todas las tablas en orden de dependencias y valida conteo de filas al final.

## Stack

- **FastAPI** 0.115 + **Uvicorn**
- **SQLAlchemy** 2.0 async + **Alembic**
- **PostgreSQL** 16
- **Pydantic** v2
- **JWT** via python-jose
- **PDF** via xhtml2pdf + Jinja2
