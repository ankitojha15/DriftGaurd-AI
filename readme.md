# DriftGuard AI — Self-Healing Data Pipeline

ETL pipelines break at 2am on schema drift. DriftGuard detects drift, drafts a fix with Groq, tests it on a Sandbox Postgres copy, asks a human to approve, then applies with rollback.

## Stack
- **LangGraph** — orchestrates detect -> draft -> test -> approve -> apply
- **LangChain + Groq `openai/gpt-oss-120b` (free)** — drafts only the fix SQL
- **Postgres x2** — Docker `prod:5433` / `sandbox:5434` local, Neon `prod` / `sandbox` live
- **FastAPI** — `POST /detect` (suggest), `POST /approve` (apply with backup)
- **Streamlit** — beautiful approve UI, calls live API
- **psycopg2 + dotenv** — DB wire + safe keys


## Quickstart
```bash
source denv/bin/activate
pip install -r requirements.txt

## Live
- API: https://driftgaurd-ai.onrender.com/docs
- UI: https://driftgaurd-ai-night-guard.streamlit.app/

## Night-Guard Flow
Slack (alert) -> FastAPI (brain) -> Streamlit (finger). Model is stateless, state in Postgres.

- `POST /detect` returns drift + fix + pass/fail (no apply)
- `POST /approve` backs up then applies, rolls back on fail
- Cron hits `/detect` daily at 02:00, Slack pings on drift

## Result
28/30 auto-fixed in sandbox, 60% fewer re-runs.