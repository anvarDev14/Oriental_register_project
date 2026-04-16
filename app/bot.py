import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]

# ── Bot egasining ismi — .env faylda OWNER_NAME ni to'ldiring ──
OWNER_NAME = os.getenv("OWNER_NAME", "Noma'lum")

# ── Bank ma'lumotlari — .env faylda to'ldiring ──
BANK_ACCOUNT = os.getenv("BANK_ACCOUNT", "")
BANK_NAME    = os.getenv("BANK_NAME", "")
BANK_MFO     = os.getenv("BANK_MFO", "")

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)
dp = Dispatcher(storage=MemoryStorage())
