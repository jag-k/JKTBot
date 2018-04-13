import requests, sys
from constants import *


def no_color(string):
    res = ''
    fill = True
    for i in string:
        if fill and i == '\x1b':
            fill = False
        if not fill and i == 'm':
            fill = True

        res += i if fill else ''
    return res


def get_request(url, params=None, **kwargs):
    try:
        if url in URLS:
            if url == SEARCH:
                if params is None:
                    url += "&apikey=" + API_KEY + "&lang=ru_RU"
                else:
                    params['apikey'] = API_KEY
                    params['lang'] = 'ru_RU'

            if url == GEOCODE:
                if params is None:
                    url += "&format=json"
                else:
                    params['format'] = 'json'

            url = URLS[url]
        res = requests.get(url, params=params, **kwargs)
        if not res:
            print(ERROR_STRING % (res.status_code, res.reason), "\n\nURL:", res.url)
            sys.exit(res.status_code)
        else:
            return res
    except Exception as err:
        print(ERROR_STRING % (type(err).__name__, err))
        sys.exit(1)


def str_param(*params):
    return ','.join(map(str, params))


ERROR_STRING = '\x1b[31;1mError\x1b[0m \x1b[1m(\x1b[36;1m%s\x1b[1m): \x1b[4;1m%s\x1b[0m'
if 'win' in sys.platform:
    try:
        import colorama
        colorama.init()
    except ImportError:
        ERROR_STRING = no_color(ERROR_STRING)


def oops_error(function_to_decorate):
    def decoration(bot, update, *args, **kwargs):
        try:
            return function_to_decorate(bot, update, *args, **kwargs)
        except Exception as err:
            print(ERROR_STRING % (type(err).__name__, err), "\nFunctions: %s\n\n" %
                  function_to_decorate.__name__)
            update.message.reply_text("Упс… Что-то пошло не так, пожалуйста, повторите попытку)\n\n" + QUESTION_STRING)
    return decoration
