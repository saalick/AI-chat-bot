import os
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ChatAction

TOKEN = ""
OPENAI_API_KEY = ""
bot = Updater(TOKEN, use_context=True).bot


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please send /sendimage {text}")


def send_image(update, context):
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    text = ' '.join(context.args)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    data = {
        "model": "image-alpha-001",
        "prompt": f"Generate an image of {text}",
        "num_images": 1,
        "size": "256x256",
        "response_format": "url"
    }
    response = requests.post('https://api.openai.com/v1/images/generations', headers=headers, json=data)
    image_url = response.json()["data"][0]["url"]
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=image_url)


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("sendimage", send_image))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
