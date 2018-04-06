import printLog
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

    SMART_TRANSPORT: "Для получения сведений о транспорте на данной остановке нажмите на кнопу или введите "
                     "\"Расписание\". Для смены локации введите команду /edit_location"
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

ABOUT_STRING = """Бот использовал следующие API:
    ● Yandex Map API (Static API): Было использованно для отображения местонахождения остановки
        https://tech.yandex.ru/maps/staticapi/
    
    ● Yandex Translator: Было использованно для перевода текста в функции "Переводчик"
        https://tech.yandex.ru/translate/

    ● (Псевдо) API сервиса "Умного Транспорта" с сайта 58bus.ru
    
    ● Запросы к сайту tproger.ru для получения шуток))
    
    Более подробную информацию можно найти в репозитории на GitHub (github.com/jag-k/JKTBot)
    
    """ + QUESTION_STRING


print_log = printLog.PrintLog()
