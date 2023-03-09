from flask import Flask
# import bot

import random
import logging
import json

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


with open("./novynyarDB.txt", "r", encoding="utf-8") as f:
    messages = json.loads(f.read())
with open("./neuralDB.txt", "r", encoding="utf-8") as f:
    neurals = json.loads(f.read())
       
# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('/get - випадкова новина з новин.яру\n/generate - згенерована нейронкой новина')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('/get - випадкова новина з новин.яру\n/generate - згенерована нейронкой новина')

def generate(update, context):
    id = random.randint(0, len(neurals) - 1)
    msg = neurals[id]
    update.message.reply_text(msg)


def get(update, context):
    id = random.randint(0, len(messages) - 1)
    msg = messages[id]
    update.message.reply_text(msg)
    #update.message.reply_text(update.message.chat.first_name + " shut up")


def echo(update, context):
    update.message.reply_text('/get - випадкова новина з новин.яру\n/generate - згенерована нейронкой новина')


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


# Create an instance of the Flask class that is the WSGI application.
# The first argument is the name of the application module or package,
# typically __name__ when using a single module.
app = Flask(__name__)

# Flask route decorators map / and /hello to the hello function.
# To add other resources, create functions that generate the page contents
# and add decorators to define the appropriate resource locators for them.

@app.route('/')
def home():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("5202200266:AAEfAw1bsRBmL-_2dhOkyakzX93B9nze7Dw", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("get", get))
    dp.add_handler(CommandHandler("generate", generate))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
    # Render the page
    return "Running..."

def list_post():
    json_body = request.get_json()
    predictions = 2 * json_body[0]   
    predictions = list(predictions)
    return jsonify(results = predictions)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000)
