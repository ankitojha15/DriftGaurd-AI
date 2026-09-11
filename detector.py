from db import get_prod, get_sandbox

def get_columns(port, db):
    conn = get_prod() if db == "prod" else get_sandbox()
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

if __name__ == "__main__":
    prod_cols = get_columns(5433, "prod")
    sandbox_cols = get_columns(5434, "sandbox")
    print("prod:", sorted(prod_cols))
    print("sandbox:", sorted(sandbox_cols))
    print("only in prod:", sorted(prod_cols - sandbox_cols))
    print("only in sandbox:", sorted(sandbox_cols - prod_cols))
    print("status: drift found" if prod_cols != sandbox_cols else "status: no drift")