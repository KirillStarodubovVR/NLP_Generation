from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


# Define a function to handle the /start command
def start(update, context):
    update.message.reply_text('Hello! I am your Telegram bot.')

# Define a function to handle normal text messages
def echo(update, context):
    update.message.reply_text(update.message.text)

def main():
    # Create an Updater object and pass your bot's token
    updater = Updater("6840926389:AAHNUkJQKpbDQAqInbCN8SBLeol54FaDAbk", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add command handler for the /start command
    dp.add_handler(CommandHandler("start", start))

    # Add a message handler for normal text messages
    dp.add_handler(MessageHandler(Filters.text, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()
