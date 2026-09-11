from db import get_prod

conn = get_prod()
cur = conn.cursor()
cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name='orders' ORDER BY 1;")
print("before:", cur.fetchall())
cur.execute("ALTER TABLE orders RENAME COLUMN cust_id TO customer_id;")
conn.commit()
conn.close()
print("prod break done")