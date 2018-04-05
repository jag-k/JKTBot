from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, ConversationHandler, RegexHandler
from reply_keyboards import *
from functions import *


def reply_md(update, *args, **kwargs):
    return update.message.bot.send_message(update.message.chat_id, parse_mode=telegram.ParseMode.MARKDOWN, *args,
                                           **kwargs)


def start(bot: telegram.bot.Bot, update: telegram.update.Update):
    message: telegram.message.Message = update.message
    message.reply_text("Привет, Я — \"многофункциональный\" бот)\n" + functions_str,
                       reply_markup=start_keyboard)
    return 0


def cancel(bot: telegram.bot.Bot, update: telegram.update.Update):
    message: telegram.message.Message = update.message
    message.reply_text(functions_str, reply_markup=start_keyboard)
    return START


def select_function(bot: telegram.bot.Bot, update: telegram.update.Update, user_data: dict):
    message: telegram.message.Message = update.message
    text = message.text.strip()
    if text in functions:
        index = functions.index(text)

        if "tr" not in user_data:
            user_data['tr'] = {"from": "ru", "to": "en"}
        if "calc" not in user_data:
            user_data['calc'] = ''
        if "stop" not in user_data:
            user_data['stop'] = None

        function_index = index + 1

        annotation = "\nПримечание: %s\n" % ANNOTATION[function_index] if function_index in ANNOTATION else ""
        markup = keyboard_dict[function_index] if function_index in keyboard_dict else remove_kb
        
        message.reply_text("Включена функция: %s\n%s\nДля выхода из данной функции введите команду /cancel" %
                           (functions[index], annotation),
                           reply_markup=markup)

        return test_smart_transport(function_index, message, user_data)


def main():
    updater = Updater(open("api_key").read())

    dp = updater.dispatcher

    cancel_handler = CommandHandler("cancel", cancel)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START: [MessageHandler(Filters.text, select_function, pass_user_data=True)],
            CALCULATOR: [MessageHandler(Filters.text, calculate_function, pass_user_data=True),
                         MessageHandler(Filters.command, calculate_function, pass_user_data=True)],
            TRANSLATE: [MessageHandler(Filters.text, translate_function, pass_user_data=True),
                        CommandHandler('edit_lang', edit_lang, pass_user_data=True)],
            SMART_TRANSPORT: [MessageHandler(Filters.location, get_locations, pass_user_data=True)],

            GET_LOCATION: [MessageHandler(Filters.location, get_locations, pass_user_data=True),
                           MessageHandler(Filters.text, get_locations, pass_user_data=True)]

        },
        fallbacks=[cancel_handler]
    )

    dp.add_handler(conv_handler)

    # Запускаем цикл приема и обработки сообщений.
    print("Bot started…")
    updater.start_polling()

    # Ждем завершения приложения. (например, получение сигнала SIG_TERM при нажатии клавиш Ctrl+C)
    updater.idle()
    print('Mission complete!)')


if __name__ == '__main__':
    main()
