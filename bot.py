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
    raise ValueError("Error: BOT_TOKEN not found in environment variables!")

# Set up bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Logging setup
logging.basicConfig(level=logging.INFO)

# Data stored directly in the script
resources = f"""
📚 {bold("Free Learning Resources")}:
🔹 [MDN Web Docs](https://developer.mozilla.org/en-US/)
🔹 [freeCodeCamp](https://www.freecodecamp.org/)
🔹 [The Odin Project](https://www.theodinproject.com/)
🔹 [Eloquent JavaScript](https://eloquentjavascript.net/)
🔹 [Full Stack Open](https://fullstackopen.com/en/)
"""

jobs = [
    "🔹 Frontend Developer - https://example.com/job1",
    "🔹 Backend Developer - https://example.com/job2",
    "🔹 Full Stack Developer - https://example.com/job3",
    "🔹 UI/UX Designer - https://example.com/job4",
    "🔹 Web Developer Intern - https://example.com/job5",
]

project_ideas = [
    "🔹 Build a Portfolio Website",
    "🔹 Create a To-Do List App",
    "🔹 Develop a Weather App using APIs",
    "🔹 Make a Blogging Platform",
    "🔹 Create a Simple E-commerce Store",
]

quizzes = [
    {"question": "What does HTML stand for?", "options": ["Hyper Text Markup Language", "High Tech Modern Language", "Home Tool Markup Language"], "answer": "Hyper Text Markup Language"},
    {"question": "Which CSS property controls text size?", "options": ["font-size", "text-size", "size"], "answer": "font-size"},
    {"question": "What does JS stand for?", "options": ["Java Syntax", "JavaScript", "Just Style"], "answer": "JavaScript"},
]

daily_tips = [
    "💡 Tip: Always write semantic HTML for better SEO & accessibility.",
    "💡 Tip: Use CSS Flexbox & Grid for responsive layouts.",
    "💡 Tip: Learn Git & GitHub to manage your projects easily.",
    "💡 Tip: Keep your JavaScript code clean by following DRY (Don't Repeat Yourself).",
    "💡 Tip: Optimize images to improve website loading speed.",
]

# Start command
@dp.message(commands=["start"])
async def send_welcome(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📚 Free Resources", callback_data="resources")],
        [InlineKeyboardButton(text="📝 Quizzes", callback_data="quizzes")],
        [InlineKeyboardButton(text="💡 Project Ideas", callback_data="projects")],
        [InlineKeyboardButton(text="📄 Resume Tips", callback_data="resume")],
        [InlineKeyboardButton(text="🎯 Job Updates", callback_data="jobs")],
        [InlineKeyboardButton(text="💡 Daily Coding Tips", callback_data="tips")],
    ])
    await message.answer("🚀 Welcome to Web Dev Bot!\nChoose an option:", reply_markup=keyboard)

# Callback handlers
@dp.callback_query(lambda c: c.data == "resources")
async def send_resources(callback_query: types.CallbackQuery):
    try:
        await callback_query.message.answer(resources, parse_mode="Markdown")
    except Exception as e:
        logging.error(f"Error sending resources: {e}")

@dp.callback_query(lambda c: c.data == "jobs")
async def job_updates(callback_query: types.CallbackQuery):
    try:
        await callback_query.message.answer("\n".join(jobs))
    except Exception as e:
        logging.error(f"Error sending job updates: {e}")

@dp.callback_query(lambda c: c.data == "projects")
async def project_suggestions(callback_query: types.CallbackQuery):
    try:
        await callback_query.message.answer("💡 Project Idea: " + random.choice(project_ideas))
    except Exception as e:
        logging.error(f"Error sending project ideas: {e}")

@dp.callback_query(lambda c: c.data == "quizzes")
async def start_quiz(callback_query: types.CallbackQuery):
    try:
        quiz = random.choice(quizzes
