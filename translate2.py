import requests

__api_key__ = open("translateApiKey").read()  # https://translate.yandex.ru/developers/keys


def translate(text, to_lang, from_lang=None, api_key=__api_key__):
    url = 'https://translate.yandex.net/api/v1.5/tr.json/translate?'
    params = {
        "key": api_key,
        "lang": '-'.join(filter(lambda x: x is not None, [to_lang, from_lang])),
        "text": text
    }
    try:
        r = requests.get(url, params).json()
        del r['code']
        r['text'] = '\n'.join(r['text'])
        return r
    except:
        return


def get_support_langs(ui="ru", api_key=__api_key__):
    url = "https://translate.yandex.net/api/v1.5/tr.json/getLangs?"
    params = {
        "key": api_key,
        "ui": ui
    }

    try:
        return requests.get(url, params).json()
    except:
        return


if __name__ == '__main__':
    text = input('Введите текст для перевода: ').replace('\\n', '\n')
    print("RU:", translate(text, 'ru')['text'])
    print("EN:", translate(text, 'en')['text'])
