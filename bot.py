import os
import logging
import random
import asyncio
from aiogram import Bot, Dispatcher, types, Router
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.markdown import bold
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Check if BOT_TOKEN is provided
if not TOKEN:
    raise ValueError("Error: BOT_TOKEN not found in environment variables.")

# Set up bot, dispatcher, and router
bot = Bot(token=TOKEN)
dp = Dispatcher()  # ✅ Fix: Dispatcher doesn't take bot instance directly
router = Router()
dp.include_router(router)  # ✅ Fix: Attach router to dispatcher

# Logging setup
logging.basicConfig(level=logging.INFO)

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

# Bot command handler
@router.message(commands=['start'])  # ✅ Fix: Use router instead of dp
async def start_command(message: types.Message):
    await message.answer(resources, reply_markup=keyboard)

# Run the bot
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())