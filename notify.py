import os
import requests
from dotenv import load_dotenv

load_dotenv()

def ping(text):
    url = os.getenv("SLACK_URL")
    if not url:
        print("no slack url")
        return
    requests.post(url, json={"text": text}, timeout=15)
    print("sent to slack")

if __name__ == "__main__":
    ping("DriftGuard test: drift found, open Streamlit to approve")