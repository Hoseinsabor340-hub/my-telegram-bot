import os
import asyncio
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ساخت وب‌سرور کوچک برای راضی نگه‌داشتن Render
app_web = Flask('')

@app_web.route('/')
def home():
    return "Bot is running!"

def run_flask():
    port = int(os.environ.get('PORT', 8080))
    app_web.run(host='0.0.0.0', port=port)

# کدهای ربات تلگرام
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("فعال هستم!")

if __name__ == '__main__':
    # روشن کردن وب‌سرور در پس‌زمینه
    Thread(target=run_flask).start()

    # توکن واقعی خودت رو اینجا بگذار
    TOKEN = '7709501876:AAHhWo4tVOA1_bHhF1OGkGKYFajA8Obr1MA'

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    
    print("...ربات با موفقیت روشن شد")
    app.run_polling()
