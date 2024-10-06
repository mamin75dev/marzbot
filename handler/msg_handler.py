from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from handler.vpn_handler import VpnHandler
from helpers.helper import Helper
from repo.request_repo import RequestRepo
from repo.db import db


class MsgHandler:
    def __init__(self):
        pass

    @classmethod
    async def handle_text(cls, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text
        if text == "خرید سرویس":
            await VpnHandler.buy_service(update)
        elif text == "تست رایگان":
            await VpnHandler.free_test(update)

    @classmethod
    async def handle_photo(cls, update: Update, context: ContextTypes.DEFAULT_TYPE):
        photo = await update.message.photo[-1].get_file()

        user_req = RequestRepo.find_request_by_user_id(update.effective_user.id)
        if user_req is None or user_req['status'] != "requested":
            await update.message.reply_text("شما درخواست باز ندارید")
        else:
            text = f"یک درخواست جدید از طرف {update.effective_user.id} ثبت شده است.\n"
            button = [
                [InlineKeyboardButton("تایید", callback_data=f"approve-{user_req['id']}")],
                [InlineKeyboardButton("رد", callback_data=f"reject-{user_req['id']}")]
            ]
            update_query=f"UPDATE requests SET req_msg_for_admin = '{text}', receipt_image='{photo.file_id}', status='paid' WHERE id = {user_req['id']}"
            db.cursor.execute(update_query)
            db.connection.commit()
            reply_markup = InlineKeyboardMarkup(button)
            await context.bot.send_photo(Helper.get_owner_chat_id(), caption=text, photo=photo.file_id, reply_markup=reply_markup)
            await update.message.reply_text("از پرداخت شما متشکریم\nپرداختی شما در صف بررسی قرار گرفت.\n\nبعد از تایید توسط مدیر اطلاعات سرویس شما به صورت خودکار ارسال میشود.")
