import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler, ConversationHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import logging
from typing import List
from datetime import date, timedelta

TOKEN = "331899805:AAHU61WT4VwI6BjhmNsypUXoTnor7xdk75I"
updater = Updater(token=TOKEN)
# bot = telegram.Bot(token="331899805:AAHU61WT4VwI6BjhmNsypUXoTnor7xdk75I")
# print(bot.getMe())
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def build_menu(buttons: List,
               n_cols: int,
               header_buttons: List = None,
               footer_buttons: List = None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


def start(bot, update):
    chat_id = update.message.chat_id
    print(chat_id)
    bot.sendMessage(chat_id=chat_id, text="I'm a bot, please talk to me!")


def juju(bot, update):
    chat_id = update.message.chat_id
    print(chat_id)
    custom_keyboard = [['top-left', 'top-right'],
                       ['bottom-left', 'bottom-right']]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    bot.sendMessage(chat_id=chat_id,
                    text="Custom Keyboard Test",
                    reply_markup=reply_markup)
    # bot.sendMessage(chat_id=chat_id, text="I'm a bot, please talk to me!")


def juju2(bot, update):
    chat_id = update.message.chat_id
    print("juju2", chat_id)
    button_list = [
        InlineKeyboardButton("col 1", "a"),
        InlineKeyboardButton("col 2", "b"),
        InlineKeyboardButton("row 2", "c")
    ]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
    bot.send_message(chat_id=chat_id, text="A two-column menu", reply_markup=reply_markup)

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('juju', juju))
dispatcher.add_handler(CommandHandler('juju2', juju2))
FIRST, SECOND = range(2)


def juju3(bot, update):
    print("juju3")
    keyboard = []
    for i in range(10):
        day = date.today() + timedelta(days=i)
        day_str = day.strftime("%Y-%m-%d")
        keyboard.append([InlineKeyboardButton(day_str, callback_data=day_str)])
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        u"Select a date",
        reply_markup=reply_markup
    )
    return FIRST


def first(bot, update):
    print("first")
    query = update.callback_query
    print(query.data)
    keyboard = [
        [InlineKeyboardButton(u"Next", callback_data=str(SECOND))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=u"First CallbackQueryHandler, Press next"
    )

    reply_markup = InlineKeyboardMarkup(keyboard)

    bot.edit_message_reply_markup(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        reply_markup=reply_markup
    )
    return SECOND


def second(bot, update):
    query = update.callback_query
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=u"Second CallbackQueryHandler"
    )
    return

updater = Updater(TOKEN)

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('juju3', juju3)],
    states={
        FIRST: [CallbackQueryHandler(first)],
        SECOND: [CallbackQueryHandler(second)]
    },
    fallbacks=[CommandHandler('juju3', juju3)]
)

updater.dispatcher.add_handler(conv_handler)
print("start")
updater.start_polling()


