import os
import random
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
# FLASK WEB SERVER (برای Render)
# =====================================

app_web = Flask(__name__)


@app_web.route('/')
def home():
    return "RP Dice Bot is Alive!"


def run_flask():
    port = int(os.environ.get('PORT', 8080))
    app_web.run(
        host='0.0.0.0',
        port=port
    )


# =====================================
# TOKEN
# =====================================

TOKEN = ""


# ====7709501876:AAHhWo4tVOA1_bHhF1OGkGKYFajA8Obr1MA=================================
# کاربران فعال
# =====================================

active_users = {}


# =====================================
# بررسی ادمین
# =====================================

async def is_admin(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    member = await update.effective_chat.get_member(
        update.effective_user.id
    )

    return member.status in [
        "administrator",
        "creator",
        "owner"
    ]


# =====================================
# چیدمان دکمه‌ها
# =====================================

def get_keyboard():

    keyboard = [

        [
            "🔴𝑅𝑂𝐿𝐿³🟢",
            "🌀𝑀𝐷/𝑆𝑀🐦‍🔥"
        ],

        [
            "🛡𝑆𝑈𝑃𝑅 𝐷𝐹🛡",
            "🗡𝑆𝑈𝑃𝑅 𝐾𝐴𝑇𝐴𝑁𝐴🗡"
        ],

        [
            "⛓𝑆𝐸𝐴𝐿",
            "🗡𝐾𝐴𝑇𝐴𝑁𝐴🗡"
        ],

        [
            "🛡𝐷𝐹 𝐾𝐴𝑇𝐴𝑁𝐴/𝑇𝐴𝐼𝐽𝑈🛡",
            "💪𝑇𝐴𝐼𝐽𝑈𝑇𝑆𝑈💪"
        ],

        [
            "🦾𝑇𝐴𝐼𝑌𝑈𝑇𝑆𝑈🦾"
        ]
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        selective=True
    )


# =====================================
# بررسی فعال بودن کاربر
# =====================================

def is_user_active(chat_id, user_id):

    return active_users.get(
        (chat_id, user_id),
        False
    )


# =====================================
# /ON
# =====================================

async def bot_on(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if update.effective_chat.type == "private":
        return

    if not await is_admin(update, context):
        return

    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    active_users[
        (chat_id, user_id)
    ] = True

    await update.message.reply_text(
        "✅ 𝐁𝐎𝐓 𝐎𝐍",
        reply_markup=get_keyboard()
    )


# =====================================
# /OFF
# =====================================

async def bot_off(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if update.effective_chat.type == "private":
        return

    if not await is_admin(update, context):
        return

    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    active_users.pop(
        (chat_id, user_id),
        None
    )

    await update.message.reply_text(
        "❌ 𝐁𝐎𝐓 𝐎𝐅𝐅",
        reply_markup=ReplyKeyboardRemove(
            selective=True
        )
    )


# =====================================
# /START
# =====================================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "برای فعال کردن منو از /on استفاده کنید."
    )


# =====================================
# تبدیل عدد به فونت
# =====================================

def fancy_number(number):

    return str(number).translate(
        str.maketrans(
            "0123456789",
            "𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵"
        )
    )


# =====================================
# ساخت یک رول
#
# 75٪ مثبت
# 20٪ منفی
# 5٪ صفر
#
# مثبت‌های پایین هم شانس خوبی دارند
# =====================================

def make_roll():

    chance = random.random()

    # =================================
    # مثبت
    # =================================

    if chance < 0.75:

        result = random.choices(
            [
                1, 2, 3, 4, 5,
                6, 7, 8, 9
            ],
            weights=[
                10, 11, 11, 10, 10,
                9, 8, 7, 6
            ],
            k=1
        )[0]

        red = random.randint(
            1,
            10 - result
        )

        green = red + result

        return red, green, result


    # =================================
    # منفی
    # =================================

    elif chance < 0.95:

        result = random.choices(
            [
                -1, -2, -3, -4, -5,
                -6, -7, -8, -9
            ],
            weights=[
                10, 10, 9, 8, 7,
                6, 5, 4, 3
            ],
            k=1
        )[0]

        green = random.randint(
            1,
            10 + result
        )

        red = green - result

        return red, green, result


    # =================================
    # صفر
    # =================================

    else:

        number = random.randint(
            1,
            10
        )

        return number, number, 0


# =====================================
# ROLL
# =====================================

async def roll_action(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    # دو رول
    red1, green1, result1 = make_roll()

    red2, green2, result2 = make_roll()


    # =================================
    # رول اول
    # =================================

    if result1 > 0:

        line1 = (
            f"𝗥𝗢𝗟𝗟 𝟭 "
            f"🔴-{fancy_number(red1)}"
        )

        line2 = (
            f"                         "
            f"= 🟢+{fancy_number(green1)}"
        )


    elif result1 < 0:

        line1 = (
            f"𝗥𝗢𝗟𝗟 𝟭 "
            f"🟢-{fancy_number(green1)}"
        )

        line2 = (
            f"                         "
            f"= 🔴+{fancy_number(red1)}"
        )


    else:

        line1 = (
            f"𝗥𝗢𝗟𝗟 𝟭 "
            f"🟢{fancy_number(green1)}"
        )

        line2 = (
            f"                         "
            f"= 🔴{fancy_number
