import os
import logging
import random
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Check if BOT_TOKEN is provided
if not TOKEN:
    raise ValueError("Error: BOT_TOKEN not found in environment variables!")

# Set up bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Logging setup
logging.basicConfig(level=logging.INFO)

# Data stored directly in the script
resources = """
📚 **Free Learning Resources**:
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
@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton("📚 Free Resources", callback_data="resources"),
        InlineKeyboardButton("📝 Quizzes", callback_data="quizzes"),
        InlineKeyboardButton("💡 Project Ideas", callback_data="projects"),
        InlineKeyboardButton("📄 Resume Tips", callback_data="resume"),
        InlineKeyboardButton("🎯 Job Updates", callback_data="jobs"),
        InlineKeyboardButton("💡 Daily Coding Tips", callback_data="tips"),
    ]
    keyboard.add(*buttons)
    await message.answer("🚀 Welcome to Web Dev Bot!\nChoose an option:", reply_markup=keyboard)

# Callback handlers
@dp.callback_query_handler(lambda c: c.data == "resources")
async def send_resources(callback_query: types.CallbackQuery):
    try:
        await bot.send_message(callback_query.from_user.id, resources, parse_mode="Markdown")
    except Exception as e:
        logging.error(f"Error sending resources: {e}")

@dp.callback_query_handler(lambda c: c.data == "jobs")
async def job_updates(callback_query: types.CallbackQuery):
    try:
        await bot.send_message(callback_query.from_user.id, "\n".join(jobs))
    except Exception as e:
        logging.error(f"Error sending job updates: {e}")

@dp.callback_query_handler(lambda c: c.data == "projects")
async def project_suggestions(callback_query: types.CallbackQuery):
    try:
        await bot.send_message(callback_query.from_user.id, "💡 Project Idea: " + random.choice(project_ideas))
    except Exception as e:
        logging.error(f"Error sending project ideas: {e}")

@dp.callback_query_handler(lambda c: c.data == "quizzes")
async def start_quiz(callback_query: types.CallbackQuery):
    try:
        quiz = random.choice(quizzes)
        options_markup = InlineKeyboardMarkup()
        for option in quiz["options"]:
            options_markup.add(InlineKeyboardButton(option, callback_data=f"quiz_{option}"))
        await bot.send_message(callback_query.from_user.id, quiz["question"], reply_markup=options_markup)
    except Exception as e:
        logging.error(f"Error sending quiz: {e}")

@dp.callback_query_handler(lambda c: c.data.startswith("quiz_"))
async def check_quiz_answer(callback_query: types.CallbackQuery):
    try:
        selected_option = callback_query.data[5:]
        question = next(q for q in quizzes if selected_option in q["options"])
        
        if selected_option == question["answer"]:
            response = "✅ Correct answer!"
        else:
            response = f"❌ Wrong answer! Correct answer: {question['answer']}"
        
        await bot.send_message(callback_query.from_user.id, response)
    except Exception as e:
        logging.error(f"Error checking quiz answer: {e}")

@dp.callback_query_handler(lambda c: c.data == "tips")
async def send_daily_tip(callback_query: types.CallbackQuery):
    try:
        await bot.send_message(callback_query.from_user.id, random.choice(daily_tips))
    except Exception as e:
        logging.error(f"Error sending daily tip: {e}")

# Start bot
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
