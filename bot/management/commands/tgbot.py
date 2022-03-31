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
        bot.send_message(message.chat.id, INFORMA_ISCORRECT[user.lang], parse_mode='html', reply_markup=rkr)


@bot.message_handler(state=UserState.main_menu)
def main_menu(message):
    user = db_utils.get_user(chat_id=message.chat.id)
    rkm = ReplyKeyboardMarkup(True)
    rkm.add(FUD_LAVASH[user.lang], XOT_DOG[user.lang])
    bot.send_message(message.chat.id, MENU_WELCOME[user.lang], reply_markup=rkm)
    menu_regix(message, user.lang)
    # bot.set_state(message.chat.id, UserState.main_menu)


def menu_lavash(chat_id, lang):
    user = db_utils.get_user(chat_id)
    ikm = InlineKeyboardMarkup()
    rkm = ReplyKeyboardMarkup(True, row_width=1)
    photo3 = open('/home/zk/Downloads/photo_2022-03-31_11-43-21.jpg', 'rb')
    ikm.row_width = 2
    ikm.add(InlineKeyboardButton('15 000', callback_data='1'), InlineKeyboardButton('20 000', callback_data='2'))
    rkm.add('Karzinka', 'Orqaga')
    bot.send_photo(chat_id, photo3, ASKE_LAVASH[user.lang], reply_markup=ikm)
    bot.send_message(chat_id, '1', reply_markup=rkm)


# menu tanlanganligini korsatadi
def menu_regix(message, lang):
    print('REgix')
    if message.text == FUD_LAVASH[lang]:
        print('LAVASH TANLANDI')
        menu_lavash(message.chat.id, lang)
    elif message.text == XOT_DOG[lang]:
        print('HOD_DOG TANLANDi')
    else:
        print('ALiMARDON')


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    user = db_utils.get_user(call.from_user.id)
    if call.data == '1':
        bot.answer_callback_query(call.id, ADD_KARZINKA_LAVASH_1[user.lang])
    elif call.data == '2':
        bot.answer_callback_query(call.id, ADD_KARZINKA_LAVASH_2[user.lang])


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