-- 001_initial.sql — esquema base (aplicar manualmente: psql -f 001_initial.sql)

CREATE TABLE users (
    id UUID PRIMARY KEY,
    username VARCHAR(150) NOT NULL UNIQUE,
    email VARCHAR(254) NOT NULL UNIQUE,
    first_name VARCHAR(150) NOT NULL DEFAULT '',
    last_name VARCHAR(150) NOT NULL DEFAULT '',
    password VARCHAR(128) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_staff BOOLEAN NOT NULL DEFAULT FALSE,
    phone VARCHAR(20),
    address VARCHAR(200),
    avatar VARCHAR(255),
    birthday DATE
);

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    created_at DATE NOT NULL,
    updated_at DATE NOT NULL
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    category_id INTEGER NOT NULL REFERENCES categories(id),
    name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    weight INTEGER NOT NULL,
    price NUMERIC(10,2) NOT NULL,
    minimum_stock NUMERIC(3,0) NOT NULL
);

CREATE TABLE history_prices (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(id),
    price NUMERIC(10,2) NOT NULL,
    created_at DATE NOT NULL
);

CREATE TYPE paymentmethod AS ENUM ('cash', 'qr', 'transfer');
CREATE TYPE shipmentstatus AS ENUM ('pending', 'in_transit', 'delivered');
CREATE TYPE departament AS ENUM (
    'La Paz', 'Cochabamba', 'Santa Cruz', 'Oruro', 'Potosi',
    'Tarija', 'Beni', 'Pando', 'Chuquisaca'
);

CREATE TABLE sales (
    id SERIAL PRIMARY KEY,
    seller_id UUID NOT NULL REFERENCES users(id),
    product_id INTEGER NOT NULL REFERENCES products(id)
);

CREATE TABLE sales_details (
    id SERIAL PRIMARY KEY,
    sale_id INTEGER NOT NULL UNIQUE REFERENCES sales(id),
    quantity INTEGER NOT NULL,
    total NUMERIC(10,2) NOT NULL,
    unit_price NUMERIC(10,2) NOT NULL,
    payment_method paymentmethod NOT NULL,
    created_at DATE NOT NULL,
    updated_at DATE NOT NULL
);

CREATE TABLE shipments (
    id SERIAL PRIMARY KEY,
    sale_id INTEGER NOT NULL UNIQUE REFERENCES sales(id),
    departament departament NOT NULL,
    city VARCHAR(255) NOT NULL DEFAULT 'Sucre',
    shipment_cost NUMERIC(10,2) NOT NULL,
    status shipmentstatus NOT NULL,
    description TEXT,
    created_at DATE NOT NULL
);
