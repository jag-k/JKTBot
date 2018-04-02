import requests

__api_key__ = open("translateApiKey").read()  # https://translate.yandex.ru/developers/keys


def translate(text, to_lang, from_lang=None):
    url = 'https://translate.yandex.net/api/v1.5/tr.json/translate?'
    params = {
        "key": __api_key__,
        "lang": '-'.join(filter(lambda x: x is not None, [to_lang, from_lang])),
        "text": text
    }
    r = requests.get(url, params).json()
    del r['code']
    r['text'] = '\n'.join(r['text'])
    return r


if __name__ == '__main__':
    text = input('Введите текст для перевода: ').replace('\\n', '\n')
    print("RU:", translate(text, 'ru')['text'])
    print("EN:", translate(text, 'en')['text'])
