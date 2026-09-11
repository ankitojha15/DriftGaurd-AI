import streamlit as st
import psycopg2
from graph import app
from rollback import backup, restore

st.title("DriftGuard AI")

if st.button("Run Check"):
    st.session_state["out"] = app.invoke({})

out = st.session_state.get("out")
if out:
    st.write("Prod:", out["prod"])
    st.write("Expected:", out["exp"])
    st.code(out["sql"])
    st.write("Test:", out["status"])

    if out["status"] == "pass":
        if st.button("Approve and Apply to Prod"):
            backup()
            try:
                conn = psycopg2.connect(
                    host="localhost", port=5433,
                    dbname="prod", user="postgres", password="postgres"
                )
                cur = conn.cursor()
                cur.execute(out["sql"])
                conn.commit()
                conn.close()
                st.success("applied to prod")
            except Exception as e:
                restore()
                st.error(f"failed, rolled back: {e}")
    else:
        st.error("fix failed, rejected")