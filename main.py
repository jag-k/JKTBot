from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, ConversationHandler, RegexHandler
from reply_keyboards import *
from functions import *


def reply_md(update, *args, **kwargs):
    return update.message.bot.send_message(update.message.chat_id, parse_mode=telegram.ParseMode.MARKDOWN, *args,
                                           **kwargs)


def start(bot: telegram.bot.Bot, update: telegram.update.Update):
    message: telegram.message.Message = update.message
    message.reply_text("Привет, Я — \"многофункциональный\" бот)\nВыберите функцию:\n    %s" % '\n    '.join(functions),
                       reply_markup=start_keyboard)
    return 0


def cancel(bot: telegram.bot.Bot, update: telegram.update.Update):
    message: telegram.message.Message = update.message
    message.reply_text("Выберите функцию:\n    %s" % '\n    '.join(functions), reply_markup=start_keyboard)
    return START


def select_function(bot: telegram.bot.Bot, update: telegram.update.Update, user_data):
    message: telegram.message.Message = update.message
    text = message.text.strip()
    if text in functions:
        index = functions.index(text) + 1

        if "tr" not in user_data:
            user_data['tr'] = {"from": "ru", "to": "en"}
        if "calc" not in user_data:
            user_data['calc'] = ''

        message.reply_text("Включена функция: %s\n\nДля выхода из данной функции введите команду /cancel" %
                           functions[index-1],
                           reply_markup=(keyboard_dict[index] if index in keyboard_dict else remove_kb))

        return index


def main():
    updater = Updater(open("api_key").read())

    dp = updater.dispatcher

    cancel_handler = CommandHandler("cancel", cancel)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START: [MessageHandler(Filters.text, select_function, pass_user_data=True)],
            CALCULATOR: [MessageHandler(Filters.text, calculate_function, pass_user_data=True)]
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
