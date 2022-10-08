from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from bot_master import Bot_Master_Parent
from config import token_telegram


def main():
    bot = Bot(token=token_telegram)
    dp = Dispatcher(bot)

    @dp.message_handler(commands=['start'])
    async def send_start(message: types.Message):
        await message.reply(Bot_Master_Parent.greetings_message)

    @dp.message_handler(commands=['week'])
    async def send_week(message: types.Message):
        await message.reply(Bot_Master_Parent.get_message_with_weekly_events())

    executor.start_polling(dp)

    
if __name__ == '__main__':
    main()
