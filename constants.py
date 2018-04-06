START = 0
CALCULATOR = 1
TRANSLATE = 2

# SMART_TRANSPORT
SMART_TRANSPORT = 3
GET_LOCATION = 4

EDIT_LOCATION_STRING = "введите адресс, где Вы сейчас находитесь (например: Пенза, Центральная 1в) " \
                       "или просто пришлите свою геолокацию, если Вы используете Telegram на телефоне."

UI = "ru"

ANNOTATION = {
    CALCULATOR: "Вы можете пользоваться как специальной клавиатурой, "
                "так и просто введя выражение в поле ввода сообщения (например: 64*49+18)",

    TRANSLATE: "Вы можете написать текст и отправить текст для перевода. По умолчанию переводится на Английский (en), "
               "Для смены языка на который переводить воспользуйтесь коммандой /edit_lang с параметром языка, "
               "на который переводить (например: /edit_lang en ИЛИ /edit_lang ru)",

    SMART_TRANSPORT: "Функция пока не доступна…"
}


GEOCODE = 'geocode'
STATIC = 'static'
SEARCH = 'search'

URLS = {
    GEOCODE: "http://geocode-maps.yandex.ru/1.x/",
    STATIC: "https://static-maps.yandex.ru/1.x/",
    SEARCH: "https://search-maps.yandex.ru/v1/"
}

API_KEY = open('api_keys/mapsApiKey', 'r').read()

QUESTION_STRING = "По всем вопросам обращатся к @Jag_k в Telegram (https://t.me/Jag_k) " \
                  "или в ВК (https://vk.com/jag_k58)"
