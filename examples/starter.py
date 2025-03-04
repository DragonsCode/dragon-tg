import dragontg
from dragontg.handlers import Dispatcher
from dragontg.methods import send_message
from dragontg.models import Message, Bot
import logging
from os import getenv
import asyncio

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(filename)s - %(message)s",
    level=logging.DEBUG 
)
BOT_TOKEN = getenv("BOT_TOKEN")
dp = Dispatcher()

@dp.message_handler(filters={'text': '/start'}) # filter for start. Use anything you want from Message object: https://core.telegram.org/bots/api#message
async def start(update, message: Message):
    success, result = await send_message(BOT_TOKEN, message.chat.id, 'Hello!')

@dp.message_handler(filters={'chat.id': 235519518, 'text': '/bot'}) # multiple filters are possible
async def admin(update, message: Message):
    # success, result = await get_me(BOT_TOKEN) # returns dict
    # OR
    result = await message.bot.get_me() # returns User object
    await message.reply(f"I am a bot! My name is {result.first_name}\n\nMy link: https://t.me/{result.username}")

@dp.message_handler() # No filters means it will match everything
async def all(update, message: Message):
    success, result = await message.reply(message.text)

async def main():
    bot = Bot(token=BOT_TOKEN, dispatcher=dp)
    await bot.get_me()
    print("Starting bot...")
    await bot.long_polling()

if __name__ == "__main__":
    print(f"Bot made using dragontg v{dragontg.__version__} by @{dragontg.__author__}, {dragontg.__credits__}")
    asyncio.run(main())