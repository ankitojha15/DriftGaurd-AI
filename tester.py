import psycopg2

FIX = "SELECT customer_id AS cust_id, id, price FROM orders;"

conn = psycopg2.connect(
    host="localhost", port=5433,
    dbname="prod", user="postgres", password="postgres"
)
cur = conn.cursor()

try:
    cur.execute(FIX)
    rows = cur.fetchall()
    print(f"rows: {len(rows)}")
    print("status: pass")
except Exception as e:
    print("status: fail")
    print(e)
finally:
    conn.close()