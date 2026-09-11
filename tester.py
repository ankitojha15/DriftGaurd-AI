import psycopg2

def run_test(sql, port, db):
    conn = psycopg2.connect(
        host="localhost", port=port,
        dbname=db, user="postgres", password="postgres"
    )
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
