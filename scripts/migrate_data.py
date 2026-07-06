"""
Script de migración de datos: Django PostgreSQL → FastAPI PostgreSQL

Uso:
    python scripts/migrate_data.py \
        --source "postgresql://user:pass@host:port/django_db" \
        --target "postgresql://user:pass@host:port/fastapi_db"

El script asume que el target ya tiene el schema aplicado (alembic upgrade head).
Hace una migración tabla por tabla respetando el orden de FKs.
Al final imprime un reporte de validación con conteo de filas.
"""
import argparse
import sys
from datetime import date, datetime
from decimal import Decimal

import psycopg2
import psycopg2.extras


def connect(dsn: str):
    return psycopg2.connect(dsn, cursor_factory=psycopg2.extras.RealDictCursor)


def validate(src_cur, tgt_cur, table: str) -> tuple[int, int]:
    src_cur.execute(f"SELECT COUNT(*) AS n FROM {table}")
    src_n = src_cur.fetchone()["n"]
    tgt_cur.execute(f"SELECT COUNT(*) AS n FROM {table}")
    tgt_n = tgt_cur.fetchone()["n"]
    return src_n, tgt_n


def migrate_users(src_cur, tgt_cur):
    src_cur.execute("""
        SELECT id, username, email, first_name, last_name, password,
               is_active, is_staff, phone, address, avatar, birthday
        FROM users
    """)
    rows = src_cur.fetchall()
    for r in rows:
        tgt_cur.execute("""
            INSERT INTO users (id, username, email, first_name, last_name, password,
                               is_active, is_staff, phone, address, avatar, birthday)
            VALUES (%(id)s, %(username)s, %(email)s, %(first_name)s, %(last_name)s,
                    %(password)s, %(is_active)s, %(is_staff)s, %(phone)s, %(address)s,
                    %(avatar)s, %(birthday)s)
            ON CONFLICT (id) DO NOTHING
        """, dict(r))
    return len(rows)


def migrate_categories(src_cur, tgt_cur):
    src_cur.execute("SELECT id, name, description, created_at, updated_at FROM categories")
    rows = src_cur.fetchall()
    for r in rows:
        tgt_cur.execute("""
            INSERT INTO categories (id, name, description, created_at, updated_at)
            VALUES (%(id)s, %(name)s, %(description)s, %(created_at)s, %(updated_at)s)
            ON CONFLICT (id) DO NOTHING
        """, dict(r))
    return len(rows)


def migrate_products(src_cur, tgt_cur):
    src_cur.execute("""
        SELECT id, category_id, name, description, weight, price, minimum_stock
        FROM products
    """)
    rows = src_cur.fetchall()
    for r in rows:
        tgt_cur.execute("""
            INSERT INTO products (id, category_id, name, description, weight, price, minimum_stock)
            VALUES (%(id)s, %(category_id)s, %(name)s, %(description)s,
                    %(weight)s, %(price)s, %(minimum_stock)s)
            ON CONFLICT (id) DO NOTHING
        """, dict(r))
    return len(rows)


def migrate_history_prices(src_cur, tgt_cur):
    src_cur.execute("SELECT id, product_id, price, created_at FROM history_prices")
    rows = src_cur.fetchall()
    for r in rows:
        tgt_cur.execute("""
            INSERT INTO history_prices (id, product_id, price, created_at)
            VALUES (%(id)s, %(product_id)s, %(price)s, %(created_at)s)
            ON CONFLICT (id) DO NOTHING
        """, dict(r))
    return len(rows)



def migrate_sales(src_cur, tgt_cur):
    """
    Django: Sale.product es M2M (sale_products). Se toma el primer producto.
    """
    src_cur.execute("""
        SELECT s.id, s.seller_id,
               sp.product_id
        FROM sales s
        LEFT JOIN sales_sale_products sp ON sp.sale_id = s.id
    """)
    rows = src_cur.fetchall()
    migrated = 0
    for r in rows:
        if not r["product_id"]:
            print(f"  WARN: sale id={r['id']} sin producto, omitido")
            continue
        tgt_cur.execute("""
            INSERT INTO sales (id, seller_id, product_id)
            VALUES (%(id)s, %(seller_id)s, %(product_id)s)
            ON CONFLICT (id) DO NOTHING
        """, dict(r))
        migrated += 1
    return migrated


def migrate_sale_details(src_cur, tgt_cur):
    src_cur.execute("""
        SELECT id, sale_id, quantity, total, unit_price, payment_method,
               created_at, updated_at
        FROM sales_details
    """)
    rows = src_cur.fetchall()
    for r in rows:
        tgt_cur.execute("""
            INSERT INTO sales_details (id, sale_id, quantity, total, unit_price,
                                       payment_method, created_at, updated_at)
            VALUES (%(id)s, %(sale_id)s, %(quantity)s, %(total)s, %(unit_price)s,
                    %(payment_method)s, %(created_at)s, %(updated_at)s)
            ON CONFLICT (id) DO NOTHING
        """, dict(r))
    return len(rows)


def migrate_shipments(src_cur, tgt_cur):
    src_cur.execute("""
        SELECT id, sale_id, departament, city, shipment_cost, status, description, created_at
        FROM shipments
    """)
    rows = src_cur.fetchall()
    for r in rows:
        tgt_cur.execute("""
            INSERT INTO shipments (id, sale_id, departament, city, shipment_cost,
                                   status, description, created_at)
            VALUES (%(id)s, %(sale_id)s, %(departament)s, %(city)s, %(shipment_cost)s,
                    %(status)s, %(description)s, %(created_at)s)
            ON CONFLICT (id) DO NOTHING
        """, dict(r))
    return len(rows)


def reset_sequences(tgt_cur):
    """Sincroniza las secuencias de autoincremento tras inserción con IDs explícitos."""
    for table, col in [
        ("categories", "id"), ("products", "id"), ("history_prices", "id"),
        ("sales", "id"), ("sales_details", "id"), ("shipments", "id"),
    ]:
        tgt_cur.execute(f"""
            SELECT setval(
                pg_get_serial_sequence('{table}', '{col}'),
                COALESCE((SELECT MAX({col}) FROM {table}), 1)
            )
        """)


def main():
    parser = argparse.ArgumentParser(description="Migrate data from Django DB to FastAPI DB")
    parser.add_argument("--source", required=True, help="Source (Django) DSN")
    parser.add_argument("--target", required=True, help="Target (FastAPI) DSN")
    args = parser.parse_args()

    print("Connecting to source and target databases...")
    src = connect(args.source)
    tgt = connect(args.target)
    src_cur = src.cursor()
    tgt_cur = tgt.cursor()

    steps = [
        ("users", migrate_users),
        ("categories", migrate_categories),
        ("products", migrate_products),
        ("history_prices", migrate_history_prices),
        ("sales", migrate_sales),
        ("sales_details", migrate_sale_details),
        ("shipments", migrate_shipments),
    ]

    print("\n--- Migrating ---")
    for table, fn in steps:
        count = fn(src_cur, tgt_cur)
        tgt.commit()
        print(f"  {table}: {count} rows migrated")

    print("\n--- Resetting sequences ---")
    reset_sequences(tgt_cur)
    tgt.commit()

    print("\n--- Validation ---")
    all_ok = True
    for table, _ in steps:
        src_n, tgt_n = validate(src_cur, tgt_cur, table)
        status = "OK" if src_n == tgt_n else "MISMATCH"
        if status != "OK":
            all_ok = False
        print(f"  {table}: source={src_n} target={tgt_n} [{status}]")

    src_cur.close()
    tgt_cur.close()
    src.close()
    tgt.close()

    if not all_ok:
        print("\nValidation FAILED — check mismatches above")
        sys.exit(1)
    print("\nMigration completed successfully.")


if __name__ == "__main__":
    main()
