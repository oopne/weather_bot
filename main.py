from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

import weather
import sql
import datetime

db = None


def handle_help(update, context):
    text = update.effective_message.text
    command = text.split()[0]
    time = datetime.datetime.today().strftime("%Y-%m-%d-%H.%M.%S")
    db.add_line(time, str(update.effective_chat.id), command)
    if command == '/start':
        chat_id = update.effective_chat.id
        url = 'https://cdn-icons-png.flaticon.com/512/3898/3898671.png'
        context.bot.send_photo(chat_id, photo=url)
    update.message.reply_text('Type "/get <location>" to get weather.')


def handle_get(update, context):
    if len(context.args) == 0:
        update.message.reply_text('/get must have arguments.')
        return
    pos = ' '.join(context.args)
    time = datetime.datetime.today().strftime("%Y-%m-%d-%H.%M.%S")
    chat_id = update.effective_chat.id
    db.add_line(time, str(chat_id), '/get ' + pos)
    update.message.reply_text('\n'.join(weather.get_weather(pos)))


def handle_history(update, context):
    time = datetime.datetime.today().strftime("%Y-%m-%d-%H.%M.%S")
    chat_id = str(update.effective_chat.id)
    update.message.reply_text(db.get_lines(chat_id))
    db.add_line(time, chat_id, '/history')


def main():
    global db
    print('=== OpenWeatherBot started ===')
    db = sql.DBInterface()
    db.setup()
    updater = Updater('5355205416:AAG8S9BtaLabRYQhZLUyA6N7457ougLkPyU')
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', handle_help))
    dispatcher.add_handler(CommandHandler('help', handle_help))
    dispatcher.add_handler(CommandHandler('history', handle_history))
    dispatcher.add_handler(
        CommandHandler('get', handle_get, pass_args=True)
    )
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
