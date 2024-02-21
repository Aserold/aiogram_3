import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

from config import TOKEN

bot = Bot(token=TOKEN)

dp = Dispatcher()


@dp.message(CommandStart())
async def start_task(message: types.Message):
    await message.answer('ЭЭЭЩКЕРЕЕЕ')


@dp.message()
async def echo(message: types.Message):
    await message.answer(message.text)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
