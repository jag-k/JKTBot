import telegram
from reply_keyboards import flat_keyboard, calculator_keyboard_list
from constants import *


__calculate_symbols__ = flat_keyboard(calculator_keyboard_list)


def calculate_function(bot: telegram.bot.Bot, update: telegram.update.Update, user_data):
    message: telegram.message.Message = update.message
    print(message.text, message.from_user)
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
