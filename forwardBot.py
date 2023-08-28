# #!/usr/bin/env python
# # pylint: disable=unused-argument, wrong-import-position
# # This program is dedicated to the public domain under the CC0 license.

# """
# Basic example for a bot that uses inline keyboards. For an in-depth explanation, check out
#  https://github.com/python-telegram-bot/python-telegram-bot/wiki/InlineKeyboard-Example.
# """
# import logging

# from telegram import __version__ as TG_VER

# try:
#     from telegram import __version_info__
# except ImportError:
#     __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

# if __version_info__ < (20, 0, 0, "alpha", 1):
#     raise RuntimeError(
#         f"This example is not compatible with your current PTB version {TG_VER}. To view the "
#         f"{TG_VER} version of this example, "
#         f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
#     )
# from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
# from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

# # Enable logging
# logging.basicConfig(
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
# )
# # set higher logging level for httpx to avoid all GET and POST requests being logged
# logging.getLogger("httpx").setLevel(logging.WARNING)

# logger = logging.getLogger(__name__)


# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     """Sends a message with three inline buttons attached."""
#     keyboard = [
#         [
#             InlineKeyboardButton("Option 1", callback_data="1"),
#             InlineKeyboardButton("Option 2", callback_data="2"),
#         ],
#         [InlineKeyboardButton("Option 3", callback_data="3")],
#     ]

#     reply_markup = InlineKeyboardMarkup(keyboard)

#     await update.message.reply_text("Please choose:", reply_markup=reply_markup)


# async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     """Parses the CallbackQuery and updates the message text."""
#     query = update.callback_query

#     # CallbackQueries need to be answered, even if no notification to the user is needed
#     # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
#     await query.answer()

#     await query.edit_message_text(text=f"Selected option: {query.data}")


# async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     """Displays info on how to use the bot."""
#     await update.message.reply_text("Use /start to test this bot.")


# def main() -> None:
#     """Run the bot."""
#     # Create the Application and pass it your bot's token.
#     application = Application.builder().token("6625229731:AAE1tVY77K8mugzLpA33K522xtyeG1jz2Tw").build()

#     application.add_handler(CommandHandler("start", start))
#     application.add_handler(CallbackQueryHandler(button))
#     application.add_handler(CommandHandler("help", help_command))

#     # Run the bot until the user presses Ctrl-C
#     application.run_polling(allowed_updates=Update.ALL_TYPES)


# if __name__ == "__main__":
#     main()


























import asyncio
from telethon import TelegramClient,types,utils
from telethon.tl.types import InputMessageID
from telethon import TelegramClient

import logging
from telegram import Update,InlineKeyboardMarkup,InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes,CallbackContext,CallbackQueryHandler

# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     level=logging.INFO
# )

# api_id = '28724355'
# api_hash = 'fd857a24c1bb7731db12c1aa20b942a8'
# source_channel = '@MAX1SERIES432'
# destination_channel = 'https://t.me/+aqP9Tj_Ce3pjZWRl'


async def start(update: Update, context: CallbackContext):
    await main(update,context)
    # await context.bot.send_message(chat_id=update.effective_chat.id, text="Provide me your app id value by command (eg /id 789897)")
    

async def id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['api_id'] = context.args
    await context.bot.send_message(chat_id=update.effective_chat.id, text="provide me your app hash value by command (eg /hash jksdkfj8fg8fg789gf78)")

async def hash(update: Update, context: CallbackContext):
    context.user_data['api_hash'] = context.args
    await forward(update,context)

async def forward(update: Update, context: CallbackContext):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="we are connecting....!")
    await main(update,context)

async def source_channel_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = []
    async for dialog in client.iter_dialogs():
        if(dialog.is_channel):
            channel=[]
            # print(dialog)
            # print(f'id: {dialog.id} title: {dialog.title} entity_id: {dialog.entity.id}')
            string = str(dialog.entity.id)
            channel.append(InlineKeyboardButton(dialog.title, callback_data= string+'$'+str('s_s')))
            keyboard.append(channel)
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Store the chat ID and message ID in user_data
    context.user_data['update'] = update
    await update.message.reply_text("Please select source channel:", reply_markup=reply_markup)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Please select source channel from above the list")


async def destination_channel_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    update = context.user_data.get('update')
    keyboard = []
    async for dialog in client.iter_dialogs():
        if(dialog.is_channel and dialog.entity.creator):
            channel=[]
            # print(dialog)
            # print(f'id: {dialog.id} title: {dialog.title} entity_id: {dialog.entity.id}')
            string = str(dialog.entity.id)
            channel.append(InlineKeyboardButton(dialog.title, callback_data= string+'$'+str('s_d')))
            keyboard.append(channel)
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Please select destination channel:", reply_markup=reply_markup) 
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Please select destination channel from above the list")
    
    
async def selected_source_channel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    data =  query.data.split("$")
    entity = await client.get_entity(int(data[0]))
    title = entity.title
    context.user_data['source_channel'] = entity.id
    await query.answer()
    await query.edit_message_text(text=f"---Source channel is selected from the list---")

    # await context.bot.send_message(chat_id=update.effective_chat.id, text="Thanks for starting!", reply_to_message_id=query.message.id)

    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Selected Source channel: {title}")
    # client.iter_messages(chat_id=update.effective_chat.id, offset_id=query.message.id, reverse=True)

    await destination_channel_list(update, context)


async def selected_destination_channel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    data =  query.data.split("$")
    entity = await client.get_entity(int(data[0]))
    title = entity.title
    # Store the chat ID and message ID in user_data
    context.user_data['source_chat_id'] = query.message.chat.id
    context.user_data['source_message_id'] = query.message.message_id
    context.user_data['destination_channel'] = entity.id
    await query.answer()
    await query.edit_message_text(text=f"---Destination channel is selected from the list---")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Selected destination channel: {title}")
    await forward_videos(context)
    

async def forward_videos(context: CallbackContext):
    source_channel = context.user_data.get('source_channel', 'Not found')
    destination_channel = context.user_data.get('destination_channel', 'Not found')
    update = context.user_data.get('update')
    # Now you can use all client methods listed below, like for example...
    await client.send_message('me', 'Hello to myself! how are youuuu')
    print ('source: ',source_channel,'Destination: ',destination_channel)
    
    async for s_message in client.iter_messages(source_channel,limit=2):
        # print(utils.get_display_name(message.sender), message.message)
        print(s_message.media and isinstance(s_message.media, types.MessageMediaDocument) and s_message.media.document.mime_type.startswith('video'))
        if s_message.media and isinstance(s_message.media, types.MessageMediaDocument) and s_message.media.document.mime_type.startswith('video'):
            try:
                # client.forward_messages(chat, message.id, source_channel)
                await client.forward_messages(destination_channel,s_message.id,source_channel)
                print(f"Forwarded video: {s_message.id}")
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Forwarded video: {s_message.id}")
            except Exception as e:
                print(f"Error forwarding video: {s_message.id} - {e}")


async def main(update: Update, context: CallbackContext):
    api_id = context.user_data.get('api_id', 'Not found')
    api_hash = context.user_data.get('api_hash', 'Not found')
    phone='+919723118547'
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Connecting to your account. Please wait.')
    global client 
    client = TelegramClient('session_name', api_id[0], api_hash[0]).start()
    # await client.connect()
    # sent= await client.send_code_request(phone)
    # print(sent)
    # # client.sign_in(phone)  # send code
    # password='please@123'
    # code = input('enter code: ')
    # await client.sign_in(phone, code)
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Your account connected with BOT')

    await source_channel_list(update ,context)


if __name__ == '__main__':
    application = ApplicationBuilder().token('6625229731:AAE1tVY77K8mugzLpA33K522xtyeG1jz2Tw').build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    start_handler = CommandHandler('id',id)
    application.add_handler(start_handler)

    start_handler = CommandHandler('hash', hash)
    application.add_handler(start_handler)

    application.add_handler(CallbackQueryHandler(selected_source_channel,pattern=".+\$s_s$"))
    application.add_handler(CallbackQueryHandler(selected_destination_channel,pattern=".+\$s_d$"))
    

    start_handler = CommandHandler('forward', forward)
    application.add_handler(start_handler)
    application.run_polling()



# Message(channel_chat_created=False, chat=Chat(first_name='happy', id=796990499, type=<ChatType.PRIVATE>), date=datetime.datetime(2023, 8, 25, 11, 54, 1, tzinfo=<UTC>), delete_chat_photo=False, entities=(MessageEntity(length=5, offset=0, type=<MessageEntityType.BOT_COMMAND>),), from_user=User(first_name='happy', id=796990499, is_bot=False, language_code='en'), group_chat_created=False, message_id=902, supergroup_chat_created=False, text='/hash fd857a24c1bb7731db12c1aa20b94a8')


# Update(callback_query=CallbackQuery(chat_instance='7667753033814613731', data='1249130371$s_s', from_user=User(first_name='happy', id=796990499, is_bot=False, language_code='en'), id='3423048129364733427', message=Message(channel_chat_created=False, chat=Chat(first_name='happy', id=796990499, type=<ChatType.PRIVATE>), date=datetime.datetime(2023, 8, 25, 11, 54, 3, tzinfo=<UTC>), delete_chat_photo=False, from_user=User(first_name='Ahead', id=6625229731, is_bot=True, username='MyAheadBot'), group_chat_created=False, message_id=906, reply_markup=InlineKeyboardMarkup(inline_keyboard=((InlineKeyboardButton(callback_data='1249130371$s_s', text='Vincenzo Hindi Drama 480p & 720p'),), (InlineKeyboardButton(callback_data='1782970145$s_s', text='Turkish Korean Drama Hindi'),), (InlineKeyboardButton(callback_data='1478159110$s_s', text='GATE CSE'),), (InlineKeyboardButton(callback_data='1812532059$s_s', text='Loot Darbar'),))), supergroup_chat_created=False, text='Please select source channel:')), update_id=618925704)