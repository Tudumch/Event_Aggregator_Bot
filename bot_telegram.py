from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from bot_master import Bot_Master_Parent
from config import token_telegram


def main():
    bot = Bot(token=token_telegram)
    dp = Dispatcher(bot)


    @dp.message_handler(content_types=['text'])
    async def get_text_messages(msg: types.Message):
       if msg.text.lower() == 'привет':
           await msg.answer('Привет!')
       else:
           await msg.answer('Не понимаю, что это значит.')

    executor.start_polling(dp)


if __name__ == '__main__':
    main()
