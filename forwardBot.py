import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

print("heloooooo")
async def start(update: Update, context: CallbackContext):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

if __name__ == '__main__':
    application = ApplicationBuilder().token('6625229731:AAE1tVY77K8mugzLpA33K522xtyeG1jz2Tw').build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)


    application.run_polling()
