import psycopg2
from breaks import BREAKS
from setup import reset
from graph import app

passed = 0
for i, sql in enumerate(BREAKS, 1):
    reset()
    conn = psycopg2.connect(
        host="localhost", port=5433,
        dbname="prod", user="postgres", password="postgres"
    )
    cur = conn.cursor()
    try:
        cur.execute(sql)
        conn.commit()
    except Exception:
        conn.rollback()
    conn.close()

    try:
        out = app.invoke({})
        if out.get("status") == "pass":
            passed += 1
            print(f"{i} pass")
        else:
            print(f"{i} fail")
    except Exception:
        print(f"{i} fail")

print(f"done: {passed}/{len(BREAKS)}")