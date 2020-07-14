import logging

import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, dispatcher
from relink.client import RelinkClient




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



def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)

    client = RelinkClient()
    shortened_url = client.shorten_url(echo_handler)
    client.get_full_url(shortened_url)
    update.message.reply_text("Вот твоя сокращенная ссылка - " + shortened_url)






def message(update, context):
    pass





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

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, message))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()




if __name__ == "__main__":
    get_answer()
    

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Our app is running on port ${ PORT }`);
});
