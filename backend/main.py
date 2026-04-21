from fastapi import FastAPI
from dotenv import load_dotenv
import os, httpx
from datetime import datetime, timezone
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
ALERT_MINUTES = int(os.getenv("ALERT_MINUTES", "60"))

async def check_alert():
    if last_ping is None:
        return
    now = datetime.now(timezone.utc)
    minutes_since = (now - last_ping).total_seconds() / 60
    if minutes_since >= ALERT_MINUTES:
        async with httpx.AsyncClient() as client:
            await client.post(
                f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                json={
                    "chat_id": TELEGRAM_CHAT_ID,
                    "text": f"⚠️ Kein Check-in seit {int(minutes_since)} Minuten!"
                }
            )

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_alert, "interval", minutes=5)
    scheduler.start()
    yield
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)

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
                "text": "Alles gut ❤️"
            }
        )

    return {"status": "ok", "timestamp": last_ping.isoformat()}

@app.get("/status")
def status():
    if last_ping is None:
        return {"last_ping": None, "minutes_since_ping": None}

    now = datetime.now(timezone.utc)
    minutes_since = (now - last_ping).total_seconds() / 60

    return {
        "last_ping": last_ping.isoformat(),
        "minutes_since_ping": round(minutes_since, 1),
        "alert_threshold_minutes": ALERT_MINUTES,
    }
