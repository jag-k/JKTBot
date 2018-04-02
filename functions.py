import telegram
from reply_keyboards import flat_keyboard, calculator_keyboard_list
from constants import *
from translate2 import translate
from reply_keyboards import functions


__calculate_symbols__ = flat_keyboard(calculator_keyboard_list)
functions_str = "Выберите функцию:\n ● %s" % '\n ● '.join(functions)


def calculate_function(bot: telegram.bot.Bot, update: telegram.update.Update, user_data: dict):
    message: telegram.message.Message = update.message
    print("Calculate:", message.text, message.from_user)
    text: str = message.text.strip()
    for i in text:
        if i not in __calculate_symbols__:
            return

    answer = "Ответ: %s"
    if len(text) == 1:
        if text != '=':
            user_data['calc'] += text
        else:
            message.reply_text(answer % eval(user_data['calc']))
            user_data['calc'] = ''
            return CALCULATOR
    else:
        message.reply_text(answer % eval(text.strip('=')))
        user_data['calc'] = ''
        return CALCULATOR


def translate_function(bot: telegram.bot.Bot, update: telegram.update.Update, user_data: dict):
    message: telegram.message.Message = update.message
    print("Translate:", message.text, message.from_user)

    tr = translate(message.text, user_data['tr']['to'])
    res = "Перевод (%s): %s" % (tr['lang'], tr['text'])
    print(res)
    message.reply_text(res)
    return TRANSLATE


def edit_lang(*args): pass


def locations(bot: telegram.bot.Bot, update: telegram.update.Update, user_data: dict):
    message: telegram.message.Message = update.message
    print("Locations:", message.location, message.from_user)
    return START
