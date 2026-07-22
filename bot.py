import os
import requests
import logging

from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    ContextTypes,
    filters
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENROUTER_KEY = os.getenv("OPENROUTER_KEY")


def ask_ai(text):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": text
            }
        ]
    }

    response = requests.post(
        url,
        headers=headers,
        json=data
    )

    result = response.json()

    return result["choices"][0]["message"]["content"]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Hello! ကျွန်တော် AI Bot ပါ။ မေးချင်တာ မေးနိုင်ပါတယ်။"
    )


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    await update.message.reply_text("⏳ စဉ်းစားနေပါတယ်...")

    try:
        answer = ask_ai(user_text)
        await update.message.reply_text(answer)

    except Exception as e:
        await update.message.reply_text(
            f"Error: {e}"
        )


logging.basicConfig(level=logging.INFO)

app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(
    MessageHandler(filters.COMMAND & filters.Regex("start"), start)
)

app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, chat)
)

print("🤖 AI Bot Running...")

app.run_polling()
