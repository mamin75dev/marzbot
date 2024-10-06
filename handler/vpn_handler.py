from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from configs import Config


class VpnHandler:
    def __init__(self):
        pass

    @classmethod
    async def buy_service(cls, update: Update):
        configs = Config.get_configs()
        button = []
        for conf in configs:
            text = f"{conf['fa_users_count']}, {conf['fa_expire_time']}, {conf['fa_capacity']}"
            button.append([InlineKeyboardButton(text, callback_data=f"config-{conf['id']}")])

        reply_markup = InlineKeyboardMarkup(button)

        await update.message.reply_text("لطفا پلن مورد نظر خود را انتخاب کنید:", reply_markup=reply_markup)

    @classmethod
    async def free_test(cls, update: Update):
        pass

    @classmethod
    async def service_details(cls, config: int):
        message = ""

        return message
