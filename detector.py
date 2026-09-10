import psycopg2

def get_columns(port, db):
    conn = psycopg2.connect(
        host="localhost", port=port,
        dbname=db, user="postgres", password="postgres"
    )
    cur = conn.cursor()
    cur.execute("""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = 'orders'
        ORDER BY column_name;
    """)
    cols = {r[0] for r in cur.fetchall()}
    conn.close()
    return cols

prod_cols = get_columns(5433, "prod")
sandbox_cols = get_columns(5434, "sandbox")

print("prod:", sorted(prod_cols))
print("sandbox:", sorted(sandbox_cols))
print("only in prod:", sorted(prod_cols - sandbox_cols))
print("only in sandbox:", sorted(sandbox_cols - prod_cols))

if prod_cols == sandbox_cols:
    print("status: no drift")
else:
    print("status: drift found")