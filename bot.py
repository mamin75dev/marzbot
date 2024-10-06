from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from handler.cmd_handler import start
from handler.msg_handler import MsgHandler
from handler.callback_handler import CallbackHandler


class Bot:
    def __init__(self):
        pass

    def run_bot(self):
        application = ApplicationBuilder().token('').build()


        start_handler = CommandHandler('start', start)
        msg_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, MsgHandler.handle_text)
        media_handler = MessageHandler(filters.PHOTO & ~filters.COMMAND, MsgHandler.handle_photo)

        application.add_handler(CallbackQueryHandler(CallbackHandler.handle))
        application.add_handler(start_handler)
        application.add_handler(msg_handler)
        application.add_handler(media_handler)

        application.run_polling()
