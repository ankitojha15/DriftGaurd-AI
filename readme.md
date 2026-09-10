# DriftGuard AI — Self-Healing Data Pipeline

ETL pipelines break at 2am on schema drift. DriftGuard detects drift, drafts a fix with Groq, tests it on a Sandbox Postgres copy, asks a human to approve, then applies with rollback.

## Stack
- **LangGraph** — orchestrates detect -> draft -> test -> approve -> apply
- **Groq `llama-3.3-70b-versatile` (free)** — drafts only the fix SQL, not the full ETL
- **Postgres x2 (Docker)** — `prod:5433` (real), `sandbox:5434` (test copy)
- **psycopg2** — Python to Postgres connector
- **Streamlit** — human approve / reject UI
- **Pydantic + python-dotenv** — structured output + safe API key

No full LangChain, no HuggingFace, no Airflow — kept simple and debuggable.

## Quickstart
```bash
source denv/bin/activate
pip install -r requirements.txt
docker compose up -d