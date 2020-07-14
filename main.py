import logging
import re
import os
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, dispatcher
from relink.client import RelinkClient




PORT = int(os.environ.get('PORT', 5000))


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)



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
    update.message.reply_text("Было ли у тебя когда-нибудь такое, что ты хочешь отправить кому-нибудь,например, неожиданный факт из Википедии, а ссылка на этот факт была огромной и некрасивой?\n"
                              "Это всегда бесило и усложняло жизнь. Но теперь, с моей помощью, ты можешь это исправить!\n"
                              "Отправь мне ссылку, а я ее сокращу. Все просто!\n"
                              "А если тебе вдруг понадобятся последние 10 ссылок, которые я для тебя сократил, то введи команду\n")




    








def message(update, context):
  text = update.message.text
  client = RelinkClient()
  shortened_url = client.shorten_url(text)
  client.get_full_url(shortened_url)
  update.message.reply_text("Вот твоя сокращенная ссылка - " + shortened_url)
  
  
 





def error(update, context):
  logger.warning('Update "%s" caused error "%s"', update, context.error)
  
    



def get_answer():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1399486062:AAHCrL0p23QCLoPHSdt_9GDdQUBNpZYGMtw", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # хендлеры под /start и /help
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

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
    

