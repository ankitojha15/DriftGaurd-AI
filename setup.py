from db import get_prod, get_sandbox

TABLE = """
CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    cust_id INT,
    price FLOAT
);
"""

DATA = "INSERT INTO orders (cust_id, price) VALUES (1, 19.99), (2, 29.99), (3, 39.99);"

def get(port, db):
    return get_prod() if db == "prod" else get_sandbox()

def reset():
    for port, db in [(5433, "prod"), (5434, "sandbox")]:
        conn = get(port, db)
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS orders;")
        cur.execute("DROP TABLE IF EXISTS orders_v2;")
        cur.execute("DROP TABLE IF EXISTS orders_backup;")
        cur.execute(TABLE)
        cur.execute(DATA)
        conn.commit()
        conn.close()
        print(db, "ready")

if __name__ == "__main__":
    reset()