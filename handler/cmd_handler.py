from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import  ContextTypes
from repo.user_repo import UserRepo
from repo.db import db


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    if update.effective_user.is_bot:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="شما بات هستید! خدمات به شما ارائه نمیشود!",
        )

    message = "سلام، من ربات کاکتوس وی پی ان هستم!"
    button = [
        [
            KeyboardButton("خرید سرویس"),
        ],
        [
            KeyboardButton("سرویس های من"),
            KeyboardButton("حساب من"),
        ],
        [
            KeyboardButton("تست رایگان"),
        ],
        [
            KeyboardButton("راهنمای اتصال"),
            KeyboardButton("پشتیبانی"),
            KeyboardButton("لینک کانال تلگرام"),
        ],
    ]
    user_exists = db.select(f"select * from users where id = {user.id}")
    if user_exists is None:
        UserRepo.insert_user(user.id, user.first_name, user.last_name)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message,
        reply_markup=ReplyKeyboardMarkup(button, one_time_keyboard=True)
    )

# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     """Send a message with a button that opens a the web app."""
#     await update.message.reply_text(
#         "Please press the button below to choose a color via the WebApp.",
#         reply_markup=ReplyKeyboardMarkup.from_button(
#             KeyboardButton(
#                 text="Open the color picker!",
#                 web_app=WebAppInfo(url="http://localhost:8888/bot/webappbot.html"),
#             )
#         ),
#     )