from telegram import Update
from telegram.ext import ContextTypes
from repo.config_repo import ConfigRepo
from repo.request_repo import RequestRepo
from models.request_model import Request
from repo.db import db
from marzban.manager import Marzban
import uuid
from helpers.bytes import gigabyte_to_byte
from helpers.duration import days_to_seconds
from helpers.qr_code import QrCodeHelper
from datetime import datetime, timedelta


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
            conf = (db.select(f"SELECT * FROM configs WHERE id = {req['config_id']}"))[-1]
            if conf is not None:
                username = f"CtsBot-{update.effective_user.id}"
                user_id = str(uuid.uuid4())
                # subscription = Marzban.create_user(
                #     username,
                #     user_id,
                #     gigabyte_to_byte(conf['capacity']),
                #     days_to_seconds(conf['expire_time_in_days'])
                # )
                subscription = "https://api.cactusplants.org/sub/Q3RzMTAwMywxNzI2NzQwODQ5hqFdFM2_WJ"
                service_query = f"insert into services (request_id, expires_in, subscription_link, service_username, service_userid) values (%s, %s, %s, %s, %s)"
                now = datetime.now()

                days_to_add = conf['expire_time_in_days']
                future_date = now + timedelta(days=days_to_add)
                values = (req['id'], future_date, subscription, username, user_id)
                db.insert(service_query, values)

                chat_id = req['chat_id']

                text = f"پرداخت با موفقیت انجام شد.\n\nبا تشکر از خرید شما،\nسرویس فعال شده:  {conf['fa_users_count']}, {conf['fa_expire_time']}, {conf['fa_capacity']}\n\nلینک اتصال:\n{subscription}\n\nهمچنین برای اتصال میتوانید QR کد بالا را در اپلیکیشن خود اسکن کنید."
                filename = f"{username}_conf-{conf['id']}"
                await QrCodeHelper.generate_qr_from_subscription(subscription, filename)

                await context.bot.send_photo(
                    chat_id=chat_id,
                    caption=text,
                    photo=f"subscriptions/{filename}.png"
                )

            await update.callback_query.answer()

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
            await query.answer()

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