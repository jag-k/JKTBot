import requests

__url__ = 'https://dictionary.yandex.net/api/v1/dicservice.json/lookup?'  # key=API-ключ&lang=en-ru&text=time
__api_key__ = open('dictionaryApiKey').read()


def get_dict(text, from_lang, to_lang=None, ui='ru', api_key=__api_key__):
    lang = ('-'.join([from_lang, from_lang]) if len(from_lang) else from_lang)if to_lang is None else '-'.join(
        [from_lang, to_lang])
    params = {
        "key": api_key,
        "text": text,
        "lang": lang,
        "ui": ui,
    }
    print(requests.get(__url__, params).url)
    return requests.get(__url__, params).json()['def']


if __name__ == '__main__':
    from pprint import pprint
    pprint(get_dict(input(), 'ru', 'en'))
