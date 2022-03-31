import telebot
from telebot.handler_backends import StatesGroup, State

from bot import db_utils
from bot.const import *
from base.settings import BOT_TOKEN
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None)


class UserState(StatesGroup):
    # Just name variables differently
    language = State() # creating instances of State class is enough from now
    contact = State()
    main_menu = State()
    menu_lavash = State()

# class UserState:
#     start = 0
#     language = 1
#     contact = 2
#     verification = 3
#     main_menu = 4
#     personal = 5
#     personal_deposit_source = 7
#     personal_deposit_currency = 8
#     personal_deposit_bank = 9
#     personal_deposit_mobile = 10
#     personal_credit_type = 11


def check_user(chat_id, tg_user_id):
    user = db_utils.get_user(chat_id)
    if not user:
        db_utils.create_user(chat_id)
        send_welcome(chat_id)
        ask_language(chat_id)
    elif not user.lang:
        ask_language(chat_id)
        print("telshirish_language")
    elif not user.contact_number:
        ask_contact(chat_id, user.lang)
        print('telshirish_nomerni')


def send_welcome(chat_id):
    bot.send_message(chat_id, 'Assalomu Alekum')


def ask_language(chat_id):
    rkm = ReplyKeyboardMarkup(True)
    rkm.add(UZBEK, RUSSIA)
    print('tilni tanlang')
    bot.send_message(chat_id, ASK_LANGUAGE, reply_markup=rkm)
    bot.set_state(chat_id, UserState.language)
    print("UserState.language")


def ask_contact(chat_id, lang):
    print("contacht")
    bsg = ASK_CONTACT_BUTTON[lang]
    rkm = ReplyKeyboardMarkup(True).add(KeyboardButton(bsg, request_contact=True))
    bot.set_state(chat_id, UserState.contact)
    print('state_contact')
    bot.send_message(chat_id, ASK_PHONE_NUMBER[lang], reply_markup=rkm)







   # irk = InlineKeyboardMarkup()
   #  id_ = message.from_user.id
   #  irk.add(InlineKeyboardButton("💠 CLICK****3844",callback_data='1'))

def send_error_lang(chat_id, lang):
    bot.send_message(chat_id, ASK_LANGUAGE)


def send_error_phone(chat_id, lang):
    bot.send_message(chat_id, ASK_PHONE_NUMBER[lang])


# def contact_state(chat_id):
#     print("MENU_STATE")
#     bot.set_state(chat_id, UserState.main_menu)


