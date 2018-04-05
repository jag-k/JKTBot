from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from constants import *


def flat_keyboard(kb):
    return [j for i in kb for j in i]


# START

start_keyboard_list = [
    ['Калькулятор', 'Переводчик'],
    ['"Умный транспорт" (βeta)']  # αlpha βeta
]


functions = flat_keyboard(start_keyboard_list)
start_keyboard = ReplyKeyboardMarkup(start_keyboard_list)


# CALCULATOR

calculator_keyboard_list = [
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    [".", "0", "=", "+"]
]

calculator_keyboard = ReplyKeyboardMarkup(calculator_keyboard_list, one_time_keyboard=False)


# TRANSLATE

translate_keyboard_list = [
    ["/edit_lang"],
    ["/cancel"]
]

translate_keyboard = ReplyKeyboardMarkup(translate_keyboard_list)

# SMART_TRANSPORT

TIMETABLE_STING = "Расписание"
transport_keyboard_list = [
    [TIMETABLE_STING, '/edit_location'],
    ['/cancel']
]

get_location_keyboard_list = [
    ["/cancel"]
]

get_location_keyboard = ReplyKeyboardMarkup(get_location_keyboard_list, True)

smart_transport_keyboard = ReplyKeyboardMarkup(transport_keyboard_list, one_time_keyboard=False)

# Remove
remove_kb = ReplyKeyboardRemove()

# KEYBOARD DICT

keyboard_dict = {
    CALCULATOR: calculator_keyboard,
    TRANSLATE: translate_keyboard,
    SMART_TRANSPORT: smart_transport_keyboard,
    GET_LOCATION: get_location_keyboard
}
