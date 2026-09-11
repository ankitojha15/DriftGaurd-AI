from db import get_prod, get_sandbox

def run_test(sql, port, db):
    conn = get_prod() if db == "prod" else get_sandbox()
    cur = conn.cursor()
    try:
        cur.execute(sql)
        if sql.strip().upper().startswith("SELECT"):
            rows = cur.fetchall()
            print(f"rows: {len(rows)}")
        else:
            print("ddl ok")
        conn.rollback()
        return "pass"
    except Exception as e:
        conn.rollback()
        print(e)
        return "fail"
    finally:
        conn.close()

if __name__ == "__main__":
    FIX = "SELECT customer_id AS cust_id, id, price FROM orders;"
    print(run_test(FIX, 5433, "prod"))
