from fastapi import FastAPI
from dotenv import load_dotenv
import os, httpx
from datetime import datetime, timezone

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
ALERT_MINUTES = int(os.getenv("ALERT_MINUTES", "60"))

app = FastAPI()

last_ping = None

@app.get("/")
def root():
    return {"status": "CRApp Backend läuft ✅"}

@app.post("/ping")
async def ping():
    global last_ping
    last_ping = datetime.now(timezone.utc)

    async with httpx.AsyncClient() as client:
        await client.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            json={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": "✅ Alles gut ❤️"
            }
        )

    return {"status": "ok", "timestamp": last_ping.isoformat()}
