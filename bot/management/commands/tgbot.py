import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from users.models import User
from bot .method import *
from bot.const import *
from telebot import custom_filters
from base.settings import BOT_TOKEN
bot = telebot.TeleBot(token=BOT_TOKEN)


@bot.message_handler(commands=['del'])
def command_help(message):
    chat_id = message.from_user.id
    user = User.objects.get(chat_id=chat_id).delete()
    bot.send_message(chat_id, 'Deleted', reply_markup=ReplyKeyboardRemove())


@bot.message_handler(commands=['start'])
def start(message):
    check_user(message.chat.id, message.from_user.id)


@bot.message_handler(state=UserState.language)
def language_handler(message):
    print('state_language')
    user = db_utils.get_user(message.chat.id)
    if message.text == UZBEK:
        print("uz")
        db_utils.ask_user_language(user, UZ)
        ask_contact(message.chat.id, user.lang)
    elif message.text == RUSSIA:
        print('ru')
        db_utils.ask_user_language(user, RU)
        ask_contact(message.chat.id, user.lang)
    else:
        send_error_lang(message.chat.id, UZ)


@bot.message_handler(state=UserState.contact)
def contact_akc(message):
    user = db_utils.get_user(message.chat.id)
    ask_contact(message.chat.id, user.lang)


@bot.message_handler(content_types=['contact'])
def contact_handler(message):
    user = db_utils.get_user(message.chat.id)
    phone_num = message.contact.phone_number
    if not user.contact_number:
        rkr = ReplyKeyboardRemove(True)
        db_utils.ask_user_contact(user, phone_num)
        bot.set_state(message.from_user.id, UserState.main_menu, message.chat.id)
        bot.send_message(message.chat.id, "Ma'lumotlar to'g'ri kiritildimi\n<strong>ha</strong> yoki <strong>yoq</strong>", parse_mode='html', reply_markup=rkr)


@bot.message_handler(state=UserState.main_menu)
def main_menu(message):
    user = db_utils.get_user(chat_id=message.chat.id)
    rkm = ReplyKeyboardMarkup(True)
    rkm.add(FUD_LAVASH[user.lang], XOT_DOG[user.lang])
    bot.send_message(message.chat.id, MENU_WELCOME[user.lang], reply_markup=rkm)


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.IsDigitFilter())

bot.infinity_polling(skip_pending=True)
# def ask_contact(chat_id, lang, message):
#     if lang == UZ:
#         msg = const.ASK_PHONE_NUMBER.get(UZ)
#     elif lang == RU:
#         msg = const.ASK_PHONE_NUMBER.get(RU)
#     if lang == UZ:
#         bsg = const.SEND_PHONE_NUM_BTN.get(UZ)
#     elif lang == RU:
#         bsg = const.SEND_PHONE_NUM_BTN.get(RU)
#
#     rkm = ReplyKeyboardMarkup(True).add(KeyboardButton(bsg, request_contact=True))
#     bot.send_message(chat_id, msg,  reply_markup=rkm, parse_mode='HTML')
#     contact_handler(message)