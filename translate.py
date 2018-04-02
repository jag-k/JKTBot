from urllib import request, parse
import json
__api_key__ = open("translateApiKey").read()  # https://translate.yandex.ru/developers/keys


class Translate:
    def __init__(self, text, default_lang='en', from_lang=None, api=__api_key__):
        self.text = parse.quote_plus(str(text))
        self.api = api
        self.from_lang = from_lang
        self.default_lang = default_lang

    def __getattr__(self, to_lang):
        lang = filter(lambda x: x is not None, [to_lang, self.from_lang])
        url = 'https://translate.yandex.net/api/v1.5/tr.json/translate?key=%s&text=%s&lang=%s' % (self.api, self.text,
                                                                                                  '-'.join(lang))
        r = json.loads(str(request.urlopen(url).read(), encoding='utf-8'))
        res = {}
        for i in r:
            if i != 'code':
                res[i] = r[i]
        return res

    def __str__(self):
        return '\n'.join(self.__getattr__(self.default_lang)['text'])


if __name__ == '__main__':
    t = Translate(input('Введите слово для перевода: ').replace('\\n', '\n'))
    print("RU:", t.ru['text'][0])
    print("EN:", t.en['text'][0])
