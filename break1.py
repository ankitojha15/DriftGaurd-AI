import psycopg2

conn = psycopg2.connect(
    host="localhost", port=5433,
    dbname="prod", user="postgres", password="postgres"
)
cur = conn.cursor()
cur.execute("ALTER TABLE orders RENAME COLUMN cust_id TO customer_id;")
conn.commit()
conn.close()
print("prod break done")