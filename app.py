import os
import streamlit as st
import requests

API = st.secrets.get("API_URL", os.getenv("API_URL", "http://127.0.0.1:8000")).rstrip("/")

st.set_page_config(page_title="DriftGuard AI", page_icon="🛡️", layout="centered")

st.markdown("# 🛡️ DriftGuard AI")
st.markdown("Self-healing data pipeline — detect, fix, approve. **Night-Guard Flow.**")
st.divider()

if st.button("🔍 Run Check", use_container_width=True):
    with st.spinner("Checking drift..."):
        try:
            r = requests.post(f"{API}/detect", timeout=90)
            r.raise_for_status()
            st.session_state["out"] = r.json()
        except Exception as e:
            st.error(f"API not reachable: {API}. Open API /docs once, check Secrets. ({e})")
            st.stop()

out = st.session_state.get("out")
if out:
    c1, c2, c3 = st.columns(3)
    c1.metric("Prod cols", len(out.get("prod", [])))
    c2.metric("Expected cols", len(out.get("exp", [])))
    c3.metric("Test", out.get("status", "unknown"))

    st.subheader("Drift")
    st.write("Prod:", out.get("prod"))
    st.write("Expected:", out.get("exp"))

    st.subheader("Fix SQL")
    st.code(out.get("sql"), language="sql")

    if out.get("status") == "pass":
        if st.button("✅ Approve and Apply to Prod", use_container_width=True):
            with st.spinner("Applying..."):
                r = requests.post(f"{API}/approve", json={"sql": out["sql"]}, timeout=60).json()
            if r.get("status") == "applied":
                st.success("Applied to prod with backup. Safe.")
                st.balloons()
            else:
                st.error(f"Failed, rolled back: {r}")
    else:
        st.error("Fix failed. Rejected. No change applied.")

st.divider()
st.caption("LangGraph + Groq + Postgres + FastAPI + Streamlit + Slack • 28/30 auto-fixed")