import telegram
from translate2 import translate, get_support_langs
from yandex_map_api import *
from smart_transport import *
from reply_keyboards import *


__calculate_symbols__ = flat_keyboard(calculator_keyboard_list)
functions_str = "Выберите функцию:\n ● %s" % '\n ● '.join(functions)


def cancel(bot: telegram.bot.Bot, update: telegram.update.Update):
    message = update.message
    message.reply_text(functions_str, reply_markup=start_keyboard)
    return START


# CALCULATOR

@oops_error
def calculate_function(bot: telegram.bot.Bot, update: telegram.update.Update, user_data: dict):
    message = update.message
    if message.text == "/cancel":
        return cancel(bot, update)
    print_log("Calculate:", message.text, message.from_user)
    text = message.text.strip()
    for i in text:
        if i not in __calculate_symbols__:
            return

    def calculate(t):
        while t and not t[0].isdigit():
            t = t[1:]

        if len(t) > 80:
            raise SyntaxError

        print_log(t)
        answer = float(eval(t))
        answer = int(answer) if answer.is_integer() else answer

        message.reply_text(answer_str % (t, answer))
        user_data['calc'] = ['']

    answer_str = "Ответ: %s=%s"
    try:
        if len(text) == 1:
            if text != '=':
                if text.isdigit() or text == '.':
                    if user_data['calc'][-1].replace('.', '').isdigit():
                        if len(user_data['calc'][-1].replace('.', '')) < 8 and user_data['calc'][-1].count('.') <= 1:
                            user_data['calc'][-1] += text
                        else:
                            raise SyntaxError
                    else:
                        user_data['calc'].append(text)
                else:
                    if not user_data['calc'][-1].replace('.', '').isdigit():
                        user_data['calc'][-1] = text
                    else:
                        user_data['calc'].append(text)

            else:
                t = ''.join(user_data['calc'])
                return calculate(t)
        else:
            t = text.strip('=')
            return calculate(t)
    except ZeroDivisionError:
        message.reply_text("Похоже, в Ваших вычислениях допущенна ошибка, пожалуйста, повторите попытку)")
        return

    except SyntaxError:
        message.reply_text("Похоже, в Ваших вычислениях допущенна ошибка, пожалуйста, повторите попытку)\n\n"
                           "Скорее всего, Вы пытаетесь ввести число длиной, больше 8 (длина без учёта точки)"
                           " или Вы привысили лимит по колличеству символов (80 символов)")
        return


# TRANSLATE

@oops_error
def translate_function(bot: telegram.bot.Bot, update: telegram.update.Update, user_data: dict):
    message = update.message
    print_log("Translate:", message.text, message.from_user)

    tr = translate(message.text, user_data['tr']['to'])
    res = "Перевод (%s): %s\n\n" \
          "Переведено сервисом «Яндекс.Переводчик» (http://translate.yandex.ru/)" % (tr['lang'], tr['text'])
    print_log(res)
    message.reply_text(res)
    return TRANSLATE


@oops_error
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

@oops_error
def get_locations(bot: telegram.bot.Bot, update: telegram.update.Update, user_data: dict):
    message = update.message
    print_log("Locations:", message.location, message.text, message.from_user)
    if message.location:
        locations = message.location['longitude'], message.location['latitude']
    else:
        try:
            locations = get_coord(message.text)
        except Exception as err:
            print_log(ERROR_STRING % (type(err).__name__, err))
            message.reply_text("Возможно, Вы ввели неправильный адрес, пожалуйста, попробуйте ещё раз")
            return
    user_data["stop"] = get_nearest_stop(*locations)
    stop = user_data['stop']
    url = URLS[STATIC] + '?l=sat,skl&z=17&pt=' + create_point(stop['lng'], stop['lat'], "comma", '', '')
    user_data['stop']['url'] = url

    text = "Ближайшая к Вам остановка это \"%s\" (%s)" % (stop['name'], stop['descr'])
    message.reply_photo(url, text, reply_markup=smart_transport_keyboard)
    return SMART_TRANSPORT


@oops_error
def edit_location(bot: telegram.bot.Bot, update: telegram.update.Update):
    message = update.message
    message.reply_text(EDIT_LOCATION_STRING.capitalize(), reply_markup=get_location_keyboard)
    return GET_LOCATION


def test_smart_transport(function_index: int, message: telegram.message.Message, user_data: dict):
    if function_index == SMART_TRANSPORT:
        if not user_data['stop']:
            message.reply_text("Вы пока не устанавливали свою локацию. Сделайте это прямо сейчас!)"
                               "\nДля этого " + EDIT_LOCATION_STRING,
                               reply_markup=get_location_keyboard)
            return GET_LOCATION
    return function_index


def string_driver_data(driver_data):
    data = (
        driver_data['rnum'], get_gos_num(driver_data['vehid']),
        driver_data['lastst'], driver_data["where"],
        string_arrival_time(driver_data['arrt'])
    )
    return '  ● %s (гос. номер: %s):' \
           '\n   Сейчас на остановке: "%s"' \
           '\n   Конечная: "%s"' \
           '\n\n    Время прибытия: %s' % data


@oops_error
def get_timetable(bot: telegram.bot.Bot, update: telegram.update.Update, user_data: dict):
    message = update.message
    r_types = ["М", "А", "Т"]
    if message.text == TIMETABLE_STING:
        message.reply_text('Подождите секундочку…')

        station_data = station_filter(get_station_forecasts(user_data['stop']['id'], user_data['stop']['type']),
                                      sorted_key=lambda x: (r_types.index(x['rtype']), x['rnum']))

        minibus = '\n\n'.join(string_driver_data(i) for i in filter(lambda x: x['rtype'] == "М", station_data))
        bus = '\n\n'.join(string_driver_data(i) for i in filter(lambda x: x['rtype'] == "А", station_data))
        trolleybuses = '\n\n'.join(string_driver_data(i) for i in filter(lambda x: x['rtype'] == "Т", station_data))

        r = lambda x: "    Пока никто не едет..." if not x else x

        data = (user_data['stop']['name'], user_data['stop']['descr'],
                r(minibus),
                r(bus),
                r(trolleybuses))

        res = ('Расписание остановки "%s" (%s) на данный момент:'
               '\n\nМаршрутки:\n%s'
               '\n\n\nАвтобусы:\n%s'
               '\n\n\nТроллейбусы:\n%s' % data).replace("    Пока никто не едет...\n\n\n",
                                                        "    Пока никто не едет...\n\n")

        open("last_res.txt", "w").write(res)

        try:
            message.reply_photo(user_data['stop']['url'], res, reply_markup=smart_transport_keyboard)
        except Exception:
            message.reply_text(res, reply_markup=smart_transport_keyboard)

        return SMART_TRANSPORT


# ABOUT and HELP

@oops_error
def about(bot: telegram.bot.Bot, update: telegram.update.Update):
    message = update.message
    message.reply_text(ABOUT_STRING, reply_markup=start_keyboard)


@oops_error
def help_func(bot: telegram.bot.Bot, update: telegram.update.Update):
    message = update.message
    message.reply_text(HELP_STRING, reply_markup=start_keyboard)


ANSWERS = {
    HUMOR: lambda update: update.message.reply_text(
        get_request("https://tproger.ru/wp-content/plugins/citation-widget/get-quote.php").text)
}
