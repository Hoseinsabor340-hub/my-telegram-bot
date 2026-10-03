import os
import asyncio
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# وب‌سرور برای زنده نگه‌داشتن سرویس در Render
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

def run_flask():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# دستور start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("فعال هستم!")

def main():
    # روشن کردن وب‌سرور در پس‌زمینه
    Thread(target=run_flask, daemon=True).start()

    # توکن ربات خودت رو دقیقاً جای عبارت زیر بگذار
    TOKEN = '7709501876:AAHhWo4tVOA1_bHhF1OGkGKYFajA8Obr1MA'

    # ساخت و اجرای ربات
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))

    print("Bot is starting...")
    application.run_polling()

if __name__ == '__main__':
    main()
