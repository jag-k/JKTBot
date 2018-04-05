import telegram
from reply_keyboards import flat_keyboard, calculator_keyboard_list
from translate2 import translate, get_support_langs
from reply_keyboards import functions
from yandex_map_api import *
from smart_transport import *


__calculate_symbols__ = flat_keyboard(calculator_keyboard_list)
functions_str = "Выберите функцию:\n ● %s" % '\n ● '.join(functions)


# CALCULATOR

def calculate_function(bot: telegram.bot.Bot, update: telegram.update.Update, user_data: dict):
    message = update.message
    if message.text == "/cancel":
        return START
    print("Calculate:", message.text, message.from_user)
    text = message.text.strip()
    for i in text:
        if i not in __calculate_symbols__:
            return

    answer_str = "Ответ: %s"
    if len(text) == 1:
        if text != '=':
            user_data['calc'] += text
        else:
            answer = float(eval(user_data['calc']))
            answer = int(answer) if answer.is_integer() else answer

            message.reply_text(answer_str % answer)
            user_data['calc'] = ''
            return CALCULATOR
    else:
        answer = float(eval(text.strip('=')))
        answer = int(answer) if answer.is_integer() else answer

        message.reply_text(answer_str % answer)
        user_data['calc'] = ''
        return CALCULATOR


# TRANSLATE

def translate_function(bot: telegram.bot.Bot, update: telegram.update.Update, user_data: dict):
    message = update.message
    print("Translate:", message.text, message.from_user)

    tr = translate(message.text, user_data['tr']['to'])
    res = "Перевод (%s): %s" % (tr['lang'], tr['text'])
    print(res)
    message.reply_text(res)
    return TRANSLATE


def edit_lang(bot: telegram.bot.Bot, update: telegram.update.Update, user_data: dict):
    message = update.message
    args = list(map(lambda x: x.lower(), message.text.split()[1:]))
    support_langs = get_support_langs(UI)

    if support_langs:
        support_langs = support_langs['langs']
    else:
        return edit_lang(bot, update, user_data)

    support_lang_str = "\n  ● ".join("%s: %s" % (lang, support_langs[lang]) for lang in support_langs)

    help = "Пожалуйста, повторите попытку введя /edit_lang *язык* " \
           "(например: /edit_lang ru ИЛИ /edit_lang en (регистр языка не учитывается))" \
           "\n\nПоддерживаемые языки:\n  ● " + support_lang_str

    if not args or len(args) > 1:
        message.reply_text("Вы не ввели язык для перевода или ввели не правильно. " + help)
        return

    if args[0] not in support_langs:
        message.reply_text("Такого языка нет. " + help)
        return

    user_data['tr']['to'] = args[0]
    message.reply_text("Язык на который переводить: %s (%s)" % (support_langs[args[0]], args[0]))
    return


# SMART_TRANSPORT

def get_locations(bot: telegram.bot.Bot, update: telegram.update.Update, user_data: dict):
    message: telegram.message.Message = update.message
    print("Locations:", message.location, message.text, message.from_user)
    if message.location:
        locations = message.location['longitude'], message.location['latitude']
    else:
        try:
            locations = get_coord(message.text)
        except Exception as err:
            print(ERROR_STRING % (type(err).__name__, err))
            message.reply_text("Возможно, Вы ввели неправильный адрес, пожалуйста, попробуйте ещё раз")
            return
    user_data["stop"] = get_nearest_stop(*locations)
    stop = user_data['stop']
    pprint(stop)
    try:
        url = URLS[STATIC] + '?l=sat,skl&z=16&pt=' + create_point(stop['lng'], stop['lat'], "comma", '', '')
        text = "Ближайшая к Вам остановка это \"%s\" (%s)" % (stop['name'], stop['descr'])
        message.reply_photo(url, text)
    except Exception as err:
        print(ERROR_STRING % (type(err).__name__, err), err.args)
        message.reply_text("Упс... Что-то пошло не так, пожалуйста, повторите попытку)")
    return SMART_TRANSPORT


def test_smart_transport(function_index: int, message: telegram.message.Message, user_data: dict):
    if function_index == SMART_TRANSPORT:
        if not user_data['stop']:
            message.reply_text("Вы пока не устанавливали свою локацию. Сделайте это прямо сейчас")
            return GET_LOCATION
    return function_index
