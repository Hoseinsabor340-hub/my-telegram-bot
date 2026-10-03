import os
import random
import asyncio
from flask import Flask
from threading import Thread

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters
)

# =====================================
# FLASK WEB SERVER
# =====================================

app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is active!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# =====================================
# TOKEN
# =====================================

TOKEN = "7709501876:AAHHWo4tVOA1_bHhF10GkGKYFajA80br1MA"

# =====================================
# ACTIVE USERS
# =====================================

active_users = {}

async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        member = await update.effective_chat.get_member(update.effective_user.id)
        return member.status in ["administrator", "creator", "owner"]
    except Exception:
        return False

def get_keyboard():
    keyboard = [
        ["🔴𝑅𝑂𝐿𝐿³🟢", "🌀𝑀𝐷/𝑆𝑀🐦‍🔥"],
        ["🛡𝑆𝑈𝑃𝑅 𝐷𝐹🛡", "🗡𝑆𝑈𝑃𝑅 𝐾𝐴𝑇𝐴𝑁𝐴🗡"],
        ["⛓𝑆𝐸𝐴🇱", "🗡𝐾𝐴𝑇𝐴𝑁𝐴🗡"],
        ["🛡𝐷𝐹 𝐾𝐴𝑇𝐴𝑁𝐴/𝑇𝐴𝐼𝐽𝑈🛡", "💪𝑇𝐴𝐼𝐽𝑈𝑇𝑆𝑈💪"],
        ["🦾𝑇𝐴𝐼𝐽𝑈𝑇𝑆𝑈🦾"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, selective=True)

async def bot_on(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == "private":
        await update.message.reply_text("این دستور فقط در گروه کاربرد دارد.")
        return

    if not await is_admin(update, context):
        await update.message.reply_text("شما ادمین گروه نیستید.")
        return

    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    active_users[(chat_id, user_id)] = True
    await update.message.reply_text("✅ 𝐁𝐎𝐓 𝐎𝐍", reply_markup=get_keyboard())

async def bot_off(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == "private":
        return

    if not await is_admin(update, context):
        return

    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    active_users.pop((chat_id, user_id), None)
    await update.message.reply_text("❌ 𝐁𝐎𝐓 𝐎𝐅𝐅", reply_markup=ReplyKeyboardRemove(selective=True))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! برای فعال کردن دکمه‌ها در گروه، دستور /on را ارسال کنید.")

# =====================================
# ACTIONS
# =====================================

async def roll_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chance = random.random()
    if chance < 0.75:
        result1 = random.randint(1, 9)
        red1 = random.randint(1, 10 - result1)
        green1 = red1 + result1
    elif chance < 0.95:
        result1 = random.randint(-9, -1)
        green1 = random.randint(1, 10 + result1)
        red1 = green1 - result1
    else:
        green1 = random.randint(1, 10)
        red1 = green1

    result2 = random.randint(1, 10)
    response_message = (
        f"𝗥𝗢𝗟𝗟 𝟭 🔴-{red1}\n"
        f"                       = 🟢+{green1}\n"
        f"𝗥𝗢𝗟𝗟 𝟮 🟢+{result2}"
    )
    await update.message.reply_text(response_message)

async def md_sm_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    options = [
        "🌀𝟭𝗠𝗗/𝗦𝗠\n🔋𝟭𝟬𝗕/𝗘𝗡", "🌀𝟮𝗠𝗗/𝗦𝗠\n🔋𝟮𝟬𝗕/𝗘𝗡",
        "🌀𝟯𝗠𝗗/𝗦𝗠\n🔋𝟯𝟬𝗕/𝗘𝗡", "🌀𝟰𝗠𝗗/𝗦𝗠\n🔋𝟰𝟬𝗕/𝗘𝗡",
        "🌀𝟱𝗠𝗗/𝗦𝗠\n🔋𝟱𝟬𝗕/𝗘𝗡", "🌀𝟬𝗠𝗗/𝗦𝗠\n🔋𝟭𝟬𝗕/𝗘𝗡",
        "🌀𝟬𝗠𝗗/𝗦𝗠\n🔋𝟮𝟬𝗕/𝗘𝗡", "🌀𝟬𝗠𝗗/𝗦𝗠\n🔋𝟯𝟬𝗕/𝗘𝗡",
        "🌀𝟬𝗠𝗗/𝗦𝗠\n🔋𝟰𝟬𝗕/𝗘𝗡", "🌀𝟬𝗠𝗗/𝗦𝗠\n🔋𝟱𝟬𝗕/𝗘𝗡",
        "🌀𝟬𝗠𝗗/𝗦𝗠\n🔋𝟬𝗕/𝗘𝗡"
    ]
    await update.message.reply_text(random.choice(options))

async def supr_df_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    options = [
        "🛡𝟭𝗗𝗙\n🔋𝟮𝟬𝗕/𝗘𝗡", "🛡𝟮𝗗𝗙\n🔋𝟯𝟬𝗕/𝗘𝗡",
        "🛡𝟯𝗗𝗙\n🔋𝟰𝟬𝗕/𝗘𝗡", "🛡𝟰𝗗𝗙\n🔋𝟱𝟬𝗕/𝗘𝗡",
        "🛡𝟱𝗗𝗙\n🔋𝟲𝟬𝗕/𝗘𝗡", "🛡𝟬𝗗𝗙\n🔋𝟮𝟬𝗕/𝗘𝗡",
        "🛡𝟬𝗗𝗙\n🔋𝟰𝟬𝗕/𝗘𝗡", "🛡𝟬𝗗𝗙\n🔋𝟱𝟬𝗕/𝗘𝗡",
        "🛡𝟬𝗗𝗙\n🔋𝟲𝟬𝗕/𝗘𝗡", "🛡𝟬𝗗𝗙\n🔋𝟬𝗕/𝗘𝗡"
    ]
    await update.message.reply_text(random.choice(options))

async def supr_katana_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    options = ["🗡𝟮𝟱𝗛𝗣", "🗡𝟯𝟬𝗛𝗣", "🗡𝟯𝟱𝗛𝗣", "🗡𝟰𝟬𝗛𝗣"]
    await update.message.reply_text(random.choice(options))

async def seal_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    options = [
        "⛓𝟭𝗦𝗘𝗔🇱\n🔋𝟭𝟬𝗕/𝗘𝗡", "⛓𝟮𝗦𝗘𝗔🇱\n🔋𝟮𝟬𝗕/𝗘𝗡",
        "⛓𝟯𝗦𝗘𝗔🇱\n🔋𝟯𝟬𝗕/𝗘𝗡", "⛓𝟬𝗦𝗘𝗔🇱\n🔋𝟭𝟬𝗕/𝗘𝗡",
        "⛓𝟬𝗦𝗘𝗔🇱\n🔋𝟮𝟬𝗕/𝗘𝗡", "⛓𝟬𝗦𝗘𝗔🇱\n🔋𝟯𝟬𝗕/𝗘𝗡",
        "⛓𝟬𝗦𝗘𝗔🇱\n🔋𝟬𝗕/𝗘𝗡"
    ]
    await update.message.reply_text(random.choice(options))

async def katana_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    options = [
        "🗡𝟭𝟱𝗛𝗣", "🗡𝟮𝟬𝗛𝗣", "🗡𝟮𝟱𝗛𝗣", "🗡𝟯𝟬𝗛𝗣",
        "🗡𝟯𝟱𝗛𝗣", "🗡𝟰𝟬𝗛𝗣", "🗡𝟰𝟱𝗛𝗣", "🗡𝟰𝟱𝗛𝗣",
        "🗡𝟱𝟬𝗛𝗣", "🗡𝟱𝟱𝗛𝗣", "🗡𝟱𝗛𝗣-", "🗡𝟭𝟬𝗛𝗣-",
        "🗡𝟭𝟱𝗛𝗣-", "🗡𝟮𝟬𝗛𝗣-", "🗡𝟮𝟱𝗛𝗣-"
    ]
    await update.message.reply_text(random.choice(options))

async def df_katana_taiju_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    options = ["🛡𝟭𝗗𝗙", "🛡𝟮𝗗𝗙", "🛡𝟯𝗗𝗙", "🛡𝟰𝗗𝗙", "🛡𝟱𝗗𝗙", "🛡𝟬𝗗𝗙"]
    await update.message.reply_text(random.choice(options))

async def taijutsu_light_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    options = [
        "💪𝟭𝟬𝗛𝗣", "💪𝟭𝟱𝗛𝗣", "💪𝟮𝟬𝗛𝗣", "💪𝟮𝟱𝗛𝗣", "💪𝟯𝟬𝗛𝗣",
        "💪𝟯𝟱𝗛𝗣", "💪𝟰𝟬𝗛𝗣", "💪𝟰𝟱𝗛𝗣", "💪𝟱𝟬𝗛𝗣", "💪𝟬𝗛𝗣"
    ]
    await update.message.reply_text(random.choice(options))

async def taijutsu_heavy_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    options = [
        "🦾𝟮𝟬𝗛𝗣", "🦾𝟮𝟱𝗛𝗣", "🦾𝟯𝟬𝗛𝗣", "🦾𝟯𝟱𝗛𝗣", "🦾𝟰𝟬𝗛𝗣",
        "🦾𝟰𝟱𝗛𝗣", "🦾𝟱𝟬𝗛𝗣", "🦾𝟱𝟱𝗛𝗣", "🦾𝟲𝟬𝗛𝗣", "🦾𝟬𝗛𝗣"
    ]
    await update.message.reply_text(random.choice(options))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    if not active_users.get((chat_id, user_id), False):
        return

    text = update.message.text
    if text == "🔴𝑅𝑂𝐿𝐿³🟢":
        await roll_action(update, context)
    elif text == "🌀𝑀𝐷/𝑆𝑀🐦‍🔥":
        await md_sm_action(update, context)
    elif text == "🛡𝑆𝑈𝑃𝑅 𝐷𝐹🛡":
        await supr_df_action(update, context)
    elif text == "🗡𝑆𝑈𝑃𝑅 𝐾𝐴𝑇𝐴𝑁𝐴🗡":
        await supr_katana_action(update, context)
    elif text == "⛓𝑆𝐸𝐴🇱":
        await seal_action(update, context)
    elif text == "🗡𝐾𝐴𝑇𝐴𝑁𝐴🗡":
        await katana_action(update, context)
    elif text == "🛡𝐷𝐹 𝐾𝐴𝑇𝐴𝑁𝐴/𝑇𝐴𝐼𝐽𝑈🛡":
        await df_katana_taiju_action(update, context)
    elif text == "💪𝑇𝐴𝐼𝐽𝑈𝑇𝑆𝑈💪":
        await taijutsu_light_action(update, context)
    elif text == "🦾𝑇𝐴𝐼𝐽𝑈𝑇𝑆𝑈🦾":
        await taijutsu_heavy_action(update, context)

# =====================================
# MAIN EXECUTION
# =====================================

async def main():
    Thread(target=run_flask, daemon=True).start()
    
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("on", bot_on))
    application.add_handler(CommandHandler("off", bot_off))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    async with application:
        await application.start()
        await application.updater.start_polling(drop_pending_updates=True)
        # نگهداری برنامه در حالت اجرا
        await asyncio.Event().wait()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
