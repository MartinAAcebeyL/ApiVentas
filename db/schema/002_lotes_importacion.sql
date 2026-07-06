-- 002_lotes_importacion.sql — lotes de importación, stock por ciudad
-- Reemplaza el stock global (tabla stocks) por stock por lote+ciudad.

CREATE TABLE imports (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    shipping_cost NUMERIC(10,2) NOT NULL DEFAULT 0,
    notes TEXT,
    created_at DATE NOT NULL
);

CREATE TABLE import_items (
    id SERIAL PRIMARY KEY,
    import_id INTEGER NOT NULL REFERENCES imports(id) ON DELETE CASCADE,
    product_id INTEGER NOT NULL REFERENCES products(id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    purchase_cost NUMERIC(10,2) NOT NULL,
    unit_cost NUMERIC(10,4) NOT NULL
);

CREATE TABLE city_stocks (
    id SERIAL PRIMARY KEY,
    import_item_id INTEGER NOT NULL REFERENCES import_items(id) ON DELETE CASCADE,
    city VARCHAR(255) NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity >= 0),
    UNIQUE (import_item_id, city)
);

-- Las ventas ahora descuentan de un ítem de lote en una ciudad.
-- Nullable: las ventas históricas no tienen lote.
ALTER TABLE sales ADD COLUMN import_item_id INTEGER REFERENCES import_items(id);
ALTER TABLE sales ADD COLUMN city VARCHAR(255);

-- El stock global se retira; si existe la tabla vieja, eliminarla.
DROP TABLE IF EXISTS stocks;
