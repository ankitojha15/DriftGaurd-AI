from db import get_prod

def get_conn(port, db):
    return get_prod()

def backup():
    conn = get_conn(5433, "prod")
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS orders_backup;")
    cur.execute("CREATE TABLE orders_backup AS SELECT * FROM orders;")
    conn.commit()
    conn.close()
    print("backup done")

def restore():
    conn = get_conn(5433, "prod")
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS orders;")
    cur.execute("CREATE TABLE orders AS SELECT * FROM orders_backup;")
    conn.commit()
    conn.close()
    print("rollback done")

if __name__ == "__main__":
    backup()