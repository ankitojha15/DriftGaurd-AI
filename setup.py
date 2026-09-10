import psycopg2

def get(port, db):
    return psycopg2.connect(
        host="localhost", port=port,
        dbname=db, user="postgres", password="postgres"
    )

TABLE = """
CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    cust_id INT,
    price FLOAT
);
"""

DATA = "INSERT INTO orders (cust_id, price) VALUES (1, 19.99), (2, 29.99), (3, 39.99);"

for port, db in [(5433, "prod"), (5434, "sandbox")]:
    conn = get(port, db)
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS orders;")
    cur.execute(TABLE)
    cur.execute(DATA)
    conn.commit()
    conn.close()
    print(db, "ready")