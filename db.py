import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

PROD_URL = os.getenv("NEON_PROD_URL")
SANDBOX_URL = os.getenv("NEON_SANDBOX_URL")

def get_prod():
    if PROD_URL:
        return psycopg2.connect(PROD_URL)
    return psycopg2.connect(
        host="localhost", port=5433,
        dbname="prod", user="postgres", password="postgres"
    )

def get_sandbox():
    if SANDBOX_URL:
        return psycopg2.connect(SANDBOX_URL)
    return psycopg2.connect(
        host="localhost", port=5434,
        dbname="sandbox", user="postgres", password="postgres"
    )