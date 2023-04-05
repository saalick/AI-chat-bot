import logging
import openai
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Set logger
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

# Define OpenAI API key
openai.api_key = ""

# Handle /start command
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello, i'm Salik - An AI chatbot")

# Handle /ask command
def ask(update, context):
    # Get user message
    message = update.message.text

    # Generate response
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"{message}\n",
        max_tokens=128,
        n=1,
        stop=None,
        temperature=0.5,
    ).choices[0].text

    # Send message back
    context.bot.send_message(chat_id=update.effective_chat.id, text=response)

# Handle unknown command
def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I don't understand your command.")

if __name__ == '__main__':
    # Set Telegram bot
    updater = Updater(token="", use_context=True)

    # /start
    start_handler = CommandHandler('start', start)
    updater.dispatcher.add_handler(start_handler)

    # /ask
    ask_handler = CommandHandler('ask', ask)
    updater.dispatcher.add_handler(ask_handler)

    # Unknown command handler
    unknown_handler = MessageHandler(Filters.command, unknown)
    updater.dispatcher.add_handler(unknown_handler)

    # Start bot
    updater.start_polling()
    updater.idle()

