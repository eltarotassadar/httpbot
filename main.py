from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, dispatcher
from relink.client import RelinkClient
import sqlite3 as sql
import logging
import re
import os
import telegram

# variables-------------------------------------

PORT = int(os.environ.get('PORT', 5000))

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# -----------------Telegram Bot-----------------

def start(update, context):
    'Что же произойдет, когда будет дана команда /start ?'
   
    update.message.reply_text("*Привет!*\n"
                              "Я бот, который сокращает ссылки.\n"
                              "Зачем это нужно? Здесь ответы - https://rel.ink/kbvZpP (а вот и пример сокращенной ссылки!).\n"
                              "Я могу сделать две вещи:\n"
                              "- сократить твою ссылку (просто отправь ее мне)\n"
                              "- показать последние 10 ссылок, которые ты сократил(а)\n"
                              "Успехов! :)", parse_mode=telegram.ParseMode.MARKDOWN)


def help(update, context):
  
    'Как бот поможет, если пользователь введет команду /help ?'
    update.message.reply_text("Отправь мне URL ссылку, а я ее сокращу до приемлемых размеров. Все просто!\n"
                              "А если тебе вдруг понадобятся последние 10 ссылок, которые я для тебя сократил, то введи команду /show\n")




def show(update, context):
    base = DatabaseUseage()
    meow = base.show(str(update.message.from_user.id))
    number = 1
    text = ''
    for url in meow:
      text += number + ') ' + url[0] + '\n'
      number += 1
      
      
    update.message.reply_text("Вот последние 10 ссылок, которые я для тебя сократил\n" + text)


def message(update, context):
    
    text = update.message.text
    client = RelinkClient()
    shortened_url = client.shorten_url(text)
    base = DatabaseUseage()
    base.adding(str(update.message.from_user.id), shortened_url)
    client.get_full_url(shortened_url)
    update.message.reply_text("Вот твоя сокращенная ссылка - " + shortened_url)


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


# -----------------Inner Logic-------------------

class DatabaseUseage():

    def __init__(self):
        self.database = sql.connect('url-s.db')
        self.users = self.database.cursor()

    def adding(self, id, shortened_url):
        self.users.execute('INSERT INTO url_list(user_id, abbr_url) VALUES("' + id + '", "' + shortened_url + '")')
        self.database.commit()

    def show(self, id):
        result = self.users.execute('SELECT abbr_url FROM url_list WHERE user_id = "' + id + '" ORDER BY id DESC LIMIT 10').fetchall()
        return result
        


# -----------------Start App---------------------


def get_answer():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1399486062:AAHCrL0p23QCLoPHSdt_9GDdQUBNpZYGMtw", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # хендлеры под /start, /help и /show
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("show", show))

    # хендлер для сообщений
    dp.add_handler(MessageHandler(Filters.regex(r'http'), message))

    # для ошибок
    dp.add_error_handler(error)

    # подключаемся к Heroku
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path='1399486062:AAHCrL0p23QCLoPHSdt_9GDdQUBNpZYGMtw')
    updater.bot.setWebhook('https://httpdwhbot.herokuapp.com/' + '1399486062:AAHCrL0p23QCLoPHSdt_9GDdQUBNpZYGMtw')
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


# при использовании файла напрямую
if __name__ == "__main__":
    get_answer()


