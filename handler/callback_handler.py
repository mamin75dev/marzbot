from telegram import Update
from telegram.ext import ContextTypes
from repo.config_repo import ConfigRepo
from repo.request_repo import RequestRepo
from models.request_model import Request
from repo.db import db
from marzban.marzban import Marzban
import uuid


class CallbackHandler:
    def __init__(self):
        pass

    @classmethod
    async def handle(cls, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        data = query.data

        if data.__contains__("approve"):
            await cls.approve_request(update, context)
        elif data.__contains__("reject"):
            await cls.reject_request(query, context)
        elif data.__contains__("config"):
            await cls.choose_plan(update)

    @classmethod
    async def approve_request(cls, update, context):
        request_id = update.callback_query.data.split("-")[1]
        db.cursor.execute(f"UPDATE requests SET status = 'approved' WHERE id = {request_id}")
        db.connection.commit()
        data = db.select(f"SELECT * FROM requests WHERE id={request_id}")
        req = data[-1] if data else None
        if req is None:
            await update.callback_query.answer()
            await update.callback_query.edit_message_text("خطا در عملیات: درخواست یافت نشد")
        else:
            conf = db.select(f"SELECT * FROM configs WHERE id = {req['config_id']}")
            # ساخت کانفیگ
            subscription = Marzban.create_user(
                f"CtsBot-{update.effective_user.id}",
                str(uuid.uuid4()),
                

            )
            chat_id = req['chat_id']

            await context.bot.send_message(
                chat_id=chat_id,
                text=f"",
            )

    @classmethod
    async def reject_request(cls, query, context):
        request_id = query.data.split("-")[1]
        db.cursor.execute(f"UPDATE requests SET status = 'rejected' WHERE id = {request_id}")
        db.connection.commit()
        data = db.select(f"SELECT * FROM requests WHERE id={request_id}")
        req = data[-1] if data else None
        if req is None:
            await query.answer()
            await query.edit_message_text("خطا در عملیات: درخواست یافت نشد")
        else:
            chat_id = req['chat_id']
            await context.bot.send_message(
                chat_id=chat_id,
                text="درخواست شما توسط مدیر سامانه رد شد!",
            )

    @classmethod
    async def choose_plan(cls, update):
        query = update.callback_query
        config_id = query.data.split("-")[1]
        conf = ConfigRepo.get_config_by_id(int(config_id))

        if conf is None:
            await update.message.reply_text("انتخاب اشتباه")

        request = Request(0, update.effective_user.id, conf['id'], "requested", "", "", update.effective_chat.id)
        RequestRepo.insert_request(request)

        text = f"پلن انتخاب شده:\nاکانت {conf['fa_users_count']}, {conf['fa_expire_time']}, {conf['fa_capacity']}\n\nقیمت سرویس: {conf['price']} تومان"
        text += f"\n\n\nشماره کارت:\n6219861901925783\nبه نام سید علیرضا اینانلو\n\nممنونیم که ما رو انتخاب کردید🙏\nتمام تلاش تیم ما ارائه کیفیت بالا و جلب رضایت شماست 🌺"

        await query.answer()

        await query.edit_message_text(text)