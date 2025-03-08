import os
import logging
import random
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.markdown import bold
from dotenv import load_dotenv
import asyncio

# Load environment variables
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Check if BOT_TOKEN is provided
if not TOKEN:
    raise ValueError("Error: BOT_TOKEN not found in environment variables.")

# Set up bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)  # ✅ Fix: Dispatcher needs bot instance

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
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer(resources, reply_markup=keyboard)

# Run the bot
async def main():
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())