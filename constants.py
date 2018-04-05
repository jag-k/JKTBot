START = 0
CALCULATOR = 1
TRANSLATE = 2

# SMART_TRANSPORT
SMART_TRANSPORT = 3
GET_LOCATION = 4

UI = "ru"

ANNOTATION = {
    CALCULATOR: "Вы можете пользоваться как специальной клавиатурой, "
                "так и просто введя выражение в поле ввода сообщения (например: 64*49+18)",

    TRANSLATE: "Вы можете написать текст и отправить текст для перевода. По умолчанию переводится на Английский (en), "
               "Для смены языка на который переводить воспользуйтесь коммандой /edit_lang с параметром языка, "
               "на который переводить (например: /edit_lang en ИЛИ /edit_lang ru)",

    SMART_TRANSPORT: "Функция пока не доступна…"
}

URLS = {
    "geocode": "http://geocode-maps.yandex.ru/1.x/",
    "static": "https://static-maps.yandex.ru/1.x/",
    "search": "https://search-maps.yandex.ru/v1/"
}

GEOCODE = 'geocode'
STATIC = 'static'
SEARCH = 'search'
API_KEY = open('mapsApiKey', 'r').read()

