# Lotes de importación: registro de ventas, métricas y stock por ciudad

**Fecha:** 2026-07-06
**Estado:** Aprobado

## Contexto y objetivo

Hoy las ventas se registran en Excel: una hoja por importación (lote). Cada hoja muestra unidades restantes, costo por unidad, cuánto falta para recuperar la inversión y stock por ciudad. Este diseño reemplaza ese flujo con la app FastAPI existente.

El usuario compra lotes que mezclan tipos de producto (ej: relojes y manillas). Conoce el costo de compra de cada tipo; el costo de envío del lote se reparte en partes iguales entre los tipos de producto.

## Modelo de datos

Tres tablas nuevas; se elimina `stocks` (reemplazada por `city_stocks`).

### `imports` (lote)

| Columna | Tipo | Notas |
|---|---|---|
| id | serial PK | |
| name | varchar(255) | ej: "Lote junio 2026" |
| shipping_cost | numeric(10,2) | envío/flete del lote completo |
| notes | text nullable | |
| created_at | date | |

### `import_items` (producto dentro del lote)

| Columna | Tipo | Notas |
|---|---|---|
| id | serial PK | |
| import_id | FK → imports | |
| product_id | FK → products | |
| quantity | integer | unidades compradas |
| purchase_cost | numeric(10,2) | costo total de compra de este tipo |
| unit_cost | numeric(10,4) | calculado y **guardado** al crear |

Cálculo al crear el lote (n_items = cantidad de ítems del lote):

```
unit_cost = (purchase_cost + shipping_cost / n_items) / quantity
```

Se guarda fijo. Si se edita el lote (costos o ítems), se recalcula explícitamente para todos los ítems del lote.

### `city_stocks` (stock restante por ítem y ciudad)

| Columna | Tipo | Notas |
|---|---|---|
| id | serial PK | |
| import_item_id | FK → import_items | |
| city | varchar(255) | |
| quantity | integer | unidades restantes en esa ciudad |

Restricción: única por (import_item_id, city). Al crear el lote, el reparto por ciudades debe sumar exactamente `import_items.quantity`.

### Cambios a `sales`

- Nueva columna `import_item_id` FK → import_items, **nullable** (las ventas históricas no tienen lote).
- Nueva columna `city` varchar(255), nullable por la misma razón.
- `seller_id` se mantiene: se llena con el usuario autenticado que registra la venta.
- `product_id` se mantiene (denormalizado, coincide con el product del ítem).

Cada lote es independiente: el mismo modelo de producto en dos lotes se trackea por separado (stock, costo unitario y recuperación propios).

## Gestión de esquema (sin Alembic)

El proyecto **no ejecuta migraciones**. Los cambios de esquema se entregan como scripts SQL planos en `db/schema/` numerados (`001_imports.sql`, ...). Aplicarlos es responsabilidad de quien administra la base de datos. La app asume que el esquema existe; no hay DDL en arranque ni en deploy. Alembic se retira del proyecto.

## Endpoints

### Lotes

- `POST /api/v1/imports/` — crea lote con ítems y reparto por ciudades en una sola llamada:
  ```json
  {
    "name": "Lote junio",
    "shipping_cost": 500,
    "items": [
      {
        "product_id": 1,
        "quantity": 100,
        "purchase_cost": 3000,
        "distribution": [{"city": "Sucre", "quantity": 60}, {"city": "La Paz", "quantity": 40}]
      }
    ]
  }
  ```
  Valida: distribution suma quantity; calcula y guarda unit_cost de cada ítem. Responde el lote con costos unitarios calculados.
- `GET /api/v1/imports/` — lista con resumen por lote: invertido, recuperado, restante, % recuperado.
- `GET /api/v1/imports/{id}` — detalle: ítems con unit_cost, stock por ciudad.
- `GET /api/v1/imports/{id}/metrics` — métricas completas (ver sección Métricas).
- `PATCH /api/v1/imports/{id}` — editar costos/nombre; recalcula unit_cost de todos los ítems.

### Ventas

- `POST /api/v1/sales/` — reemplaza el flujo actual:
  ```json
  {
    "import_item_id": 5,
    "city": "Sucre",
    "quantity": 2,
    "unit_price": 120,
    "shipment": {"departament": "La Paz", "city": "El Alto", "shipment_cost": 30}
  }
  ```
  - `shipment` opcional.
  - Valida stock en `city_stocks` para ese ítem+ciudad; descuenta.
  - `seller_id` = usuario autenticado.
  - Mantiene la alerta de email por stock mínimo (contra el total restante del producto).

### Stock

- `GET /api/v1/stock/by-city` — stock por ciudad; filtros opcionales `import_id`, `product_id`, `city`.

Los endpoints existentes de reportes (`/sales/reports/*`, `/sales/filter`, `/users/me/sales`) se mantienen; los reportes gráficos y PDF no cambian en esta fase.

## Métricas (paridad con el Excel)

`GET /api/v1/imports/{id}/metrics` responde:

- **Inversión del lote** = Σ purchase_cost + shipping_cost.
- **Recuperado** = Σ (quantity × unit_price) de las ventas de los ítems del lote. **No incluye** el costo de envío al cliente (Shipment queda fuera del cálculo).
- **Falta por recuperar** = inversión − recuperado (y % recuperado).
- Por ítem: unidades compradas, vendidas, **restantes** (total y por ciudad), **costo unitario**, precio promedio de venta, ganancia por unidad (precio promedio − unit_cost).
- Ventas del lote listadas con fecha, vendedor, ciudad, cantidad y precio.

## Dashboard web

Servido por FastAPI + Jinja2 (mismo stack que el PDF; sin framework JS). Requiere login (sesión con el mismo JWT en cookie).

- **`/dashboard`** — lista de lotes con barra de progreso de recuperación.
- **`/dashboard/imports/{id}`** — detalle del lote: las 4 métricas del Excel, tabla de ítems, stock por ciudad, ventas recientes.
- **`/dashboard/sales/new`** — formulario: lote → ítem → ciudad (muestra stock disponible) → cantidad y precio; envío opcional.
- **`/dashboard/imports/new`** — formulario de lote: ítems con costos y reparto por ciudades.

## Manejo de errores

- Venta con stock insuficiente en la ciudad → 400 con stock disponible en el mensaje.
- Reparto por ciudades que no suma la cantidad del ítem → 422.
- Venta sobre ítem inexistente / ciudad sin registro de stock → 404.
- Edición de lote con ventas ya registradas: permitida (recalcula unit_cost), pero la respuesta advierte cuántas ventas existen — las métricas usan siempre el unit_cost vigente.

## Testing

- Unit: cálculo de unit_cost (incluye redondeo con Decimal), validación de distribución, recálculo al editar.
- Integración (pytest + httpx, DB de prueba): crear lote → vender → verificar descuento en city_stocks y métricas de recuperación; venta sin stock; venta con shipment.
- Las ventas históricas (import_item_id null) no rompen los endpoints de reportes existentes.

## Fuera de alcance

- Traslados de stock entre ciudades.
- Criterios de reparto de envío alternativos (por valor/peso) — el diseño deja la puerta abierta pero solo se implementa el reparto en partes iguales.
- Incluir el envío al cliente en la recuperación.
- Frontend con framework JS.
