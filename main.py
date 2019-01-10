from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, ConversationHandler
from functions import *


def reply_md(update, *args, **kwargs):
    return update.message.bot.send_message(update.message.chat_id, parse_mode=telegram.ParseMode.MARKDOWN, *args,
                                           **kwargs)


def start(bot: telegram.bot.Bot, update: telegram.update.Update):
    message = update.message
    message.reply_text("Привет, Я — \"многофункциональный\" бот)\n%s\n\n"
                       "P.S.: Если бот перестал реагировать, попробуйте прописать комманду /start. "
                       "Возможно, бота просто перезагружали.\n\n%s" % (functions_str, QUESTION_STRING),
                       reply_markup=start_keyboard)
    print("Start command")
    return 0


def cancel(bot: telegram.bot.Bot, update: telegram.update.Update):
    message = update.message
    message.reply_text(functions_str, reply_markup=start_keyboard)
    return START


@oops_error
def select_function(bot: telegram.bot.Bot, update: telegram.update.Update, user_data: dict):
    message = update.message
    text = message.text.strip()
    if text in functions:
        index = functions.index(text)

        if "tr" not in user_data:
            user_data['tr'] = {"from": "ru", "to": "en"}
        if "calc" not in user_data:
            user_data['calc'] = ['']
        if "stop" not in user_data:
            user_data['stop'] = None

        function_index = index + 1

        if text in ANSWERS:
            t = ANSWERS[text](update)
            # print_log(t)
            return t

        annotation = "\nПримечание: %s\n" % ANNOTATION[function_index] if function_index in ANNOTATION else ""
        markup = keyboard_dict[function_index] if function_index in keyboard_dict else remove_kb

        message.reply_text("Включена функция: %s\n%s\nДля выхода из данной функции введите команду /cancel" %
                           (functions[index], annotation),
                           reply_markup=markup)

        return test_smart_transport(function_index, message, user_data)


@oops_error
def stop_bot(bot: telegram.bot.Bot, update: telegram.update.Update):
    message = update.message
    if message.from_user['id'] == 241440713:
        message.reply_text("Выключаюсь…", reply_markup=remove_kb)
        updater.stop()
        sys.exit()
    else:
        message.reply_text("У Вас недостаточно прав")


def main():
    dp = updater.dispatcher

    cancel_handler = CommandHandler("cancel", cancel)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START: [MessageHandler(Filters.text, select_function, pass_user_data=True),
                    CommandHandler("about", about), CommandHandler("help", help_func)],
            CALCULATOR: [MessageHandler(Filters.text, calculate_function, pass_user_data=True),
                         MessageHandler(Filters.command, calculate_function, pass_user_data=True)],
            TRANSLATE: [MessageHandler(Filters.text, translate_function, pass_user_data=True),
                        CommandHandler('edit_lang', edit_lang, pass_user_data=True)],
            SMART_TRANSPORT: [MessageHandler(Filters.text, get_timetable, pass_user_data=True),
                              CommandHandler("edit_location", edit_location)],

            GET_LOCATION: [MessageHandler(Filters.location, get_locations, pass_user_data=True),
                           MessageHandler(Filters.text, get_locations, pass_user_data=True)],

        },
        fallbacks=[cancel_handler, CommandHandler('off', stop_bot)]
    )

    dp.add_handler(conv_handler)
    dp.add_handler(MessageHandler(Filters.all, (lambda bot, update: print("message", update.message.text))))

    # Запускаем цикл приема и обработки сообщений.
    print_log("Bot started…")
    updater.start_polling()

    # Ждем завершения приложения. (например, получение сигнала SIG_TERM при нажатии клавиш Ctrl+C)
    updater.idle()
    print_log('Mission complete!)')


if __name__ == '__main__':
    updater = Updater(open("api_keys/api_key").read(), request_kwargs={
        'proxy_url': 'socks5://35.185.64.205:1080/',
        # 'proxy_url': 'https://162.243.162.54:80',
        # Optional, if you need authentication:
        # 'urllib3_proxy_kwargs': {
        #     'username': 'PROXY_USER',
        #     'password': 'PROXY_PASS',
        # }
    })
    main()
