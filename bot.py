import os
import logging
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.markdown import bold
from dotenv import load_dotenv
from fastapi import FastAPI
import asyncio

# Load environment variables
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Render ka full HTTPS URL yahan set karein

# Check if BOT_TOKEN is provided
if not TOKEN:
    raise ValueError("Error: BOT_TOKEN not found in environment variables.")

# Set up bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

# Logging setup
logging.basicConfig(level=logging.INFO)

# FastAPI app for webhook
app = FastAPI()

@app.on_event("startup")
async def on_startup():
    """Set webhook when server starts"""
    await bot.set_webhook(WEBHOOK_URL)

@app.on_event("shutdown")
async def on_shutdown():
    """Delete webhook when server shuts down"""
    await bot.delete_webhook()

@app.get("/")
async def home():
    return {"status": "Bot is running!"}

@app.post("/webhook")
async def webhook(update: dict):
    """Handle incoming updates"""
    telegram_update = types.Update(**update)
    await dp.feed_update(bot, telegram_update)
    return {"ok": True}

# Free Learning Resources
resources = f"""
📚 {bold("Free Learning Resources")}:
🔹 [MDN Web Docs](https://developer.mozilla.org/en-US/)
🔹 [freeCodeCamp](https://www.freecodecamp.org/)
🔹 [The Odin Project](https://www.theodinproject.com/)
🔹 [Eloquent JavaScript](https://eloquentjavascript.net/)
"""

# Correct Inline Keyboard
keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🔗 MDN Web Docs", url="https://developer.mozilla.org/en-US/")],
    [InlineKeyboardButton(text="🎓 freeCodeCamp", url="https://www.freecodecamp.org/")],
    [InlineKeyboardButton(text="📖 The Odin Project", url="https://www.theodinproject.com/")],
    [InlineKeyboardButton(text="📘 Eloquent JavaScript", url="https://eloquentjavascript.net/")]
])

@router.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(resources, reply_markup=keyboard)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8080)))