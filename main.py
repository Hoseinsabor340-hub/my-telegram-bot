import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_first_name = update.effective_user.first_name
    await update.message.reply_text(f"سلام {user_first_name} عزیز! خوش اومدی. من یک ربات ۲۴ ساعته فعال هستم! 🤖")

if __name__ == '__main__':
    # توکن رباتت رو بین دو کوتیشن قرار بده
    TOKEN = 'YOUR_BOT_TOKEN_HERE'
    
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    
    print("ربات با موفقیت روشن شد...")
    app.run_polling()
