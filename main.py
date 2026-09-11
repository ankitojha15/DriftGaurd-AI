from fastapi import FastAPI
from pydantic import BaseModel
from graph import app as graph_app
from rollback import backup, restore
from db import get_prod

app = FastAPI(title="DriftGuard AI")

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/detect")
def detect():
    return graph_app.invoke({})

class ApproveIn(BaseModel):
    sql: str

@app.post("/approve")
def approve(body: ApproveIn):
    backup()
    try:
        conn = get_prod()
        cur = conn.cursor()
        cur.execute(body.sql)
        conn.commit()
        conn.close()
        return {"status": "applied"}
    except Exception as e:
        restore()
        return {"status": "failed", "error": str(e)}