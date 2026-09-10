import psycopg2

def check(port, db):
    conn = psycopg2.connect(
        host="localhost",
        port=port,
        dbname=db,
        user="postgres",
        password="postgres"
    )
    cur = conn.cursor()
    cur.execute("SELECT 1;")
    print(db, "OK:", cur.fetchone())
    conn.close()

check(5433, "prod")
check(5434, "sandbox")