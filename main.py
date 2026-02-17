import os
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

MESSAGES = [
    "🚀 2026 is your year. Stop procrastinating and take action now.",
    "🔥 Focus beats motivation. Stay disciplined.",
    "💡 Your future self depends on what you do today.",
    "🧠 Positive mindset + action = success.",
    "⏳ Time is moving. Are you moving with it?",
]

async def send_reminder(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=context.job.chat_id,
        text=random.choice(MESSAGES),
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("▶ Start", callback_data="start")],
        [InlineKeyboardButton("▶ Continue", callback_data="continue")],
    ]

    await update.message.reply_text(
        "Choose an option:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    chat_id = query.message.chat_id

    # Prevent duplicate jobs
    current_jobs = context.job_queue.get_jobs_by_name(str(chat_id))
    if current_jobs:
        await query.message.reply_text(
            "⚡ Motivation is already running. Stay focused!"
        )
        return

    context.job_queue.run_repeating(
        send_reminder,
        interval=1800,  # 30 minutes
        first=0,
        chat_id=chat_id,
        name=str(chat_id),
    )

    await query.message.reply_text(
        "✅ Motivation started.\nStay focused on your 2026 goals."
    )

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    app.run_polling()

if __name__ == "__main__":
    main()
