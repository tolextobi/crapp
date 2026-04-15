from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
ALERT_MINUTES = int(os.getenv("ALERT_MINUTES", "60"))

app = FastAPI()

@app.get("/")
def root():
    return {"status": "CRApp Backend läuft ✅"}