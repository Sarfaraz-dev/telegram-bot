import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.markdown import bold
from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn

# Load environment variables
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Check if BOT_TOKEN is provided
if not TOKEN:
    raise ValueError("Error: BOT_TOKEN not found in environment variables.")

# Set up bot, dispatcher, and router
bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

# Logging setup
logging.basicConfig(level=logging.INFO)

# FastAPI app to prevent Render "No open ports detected" issue
app = FastAPI()

@app.get("/")
def home():
    return {"status": "Bot is running!"}

# Data stored directly in the script
resources = f"""
📚 {bold("Free Learning Resources")}:
🔹 [MDN Web Docs](https://developer.mozilla.org/en-US/)
🔹 [freeCodeCamp](https://www.freecodecamp.org/)
🔹 [The Odin Project](https://www.theodinproject.com/)
🔹 [Eloquent JavaScript](https://eloquentjavascript.net/)
"""

# ✅ Fix: Correct Inline Keyboard
keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🔗 MDN Web Docs", url="https://developer.mozilla.org/en-US/")],
    [InlineKeyboardButton(text="🎓 freeCodeCamp", url="https://www.freecodecamp.org/")],
    [InlineKeyboardButton(text="📖 The Odin Project", url="https://www.theodinproject.com/")],
    [InlineKeyboardButton(text="📘 Eloquent JavaScript", url="https://eloquentjavascript.net/")]
])

# ✅ Fix: Correct command handler syntax for aiogram v3
@router.message(Command("start"))  
async def start_command(message: types.Message):
    await message.answer(resources, reply_markup=keyboard)

# Run the bot
async def start_bot():
    await dp.start_polling(bot)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(start_bot())  # Start bot polling in background
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8080)))  # Start FastAPI server