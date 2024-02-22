from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command

from filters.chat_types import ChatTypeFilter

user_private_rt = Router()
user_private_rt.message.filter(ChatTypeFilter(['private']))


@user_private_rt.message((F.text.lower().contains('здрав')) | (F.text.lower().contains('приве')))
@user_private_rt.message(CommandStart())
async def start_task(message: types.Message):
    name = message.from_user.first_name
    await message.answer(f'Ну привет, {name}!😈')


@user_private_rt.message(F.text.lower() == 'меню')
@user_private_rt.message(Command('menu'))
async def menu(message: types.Message):
    await message.answer('Вот меню:')


@user_private_rt.message(F.text.lower() == 'бот')
@user_private_rt.message(Command('about'))
async def about(message: types.Message):
    await message.answer('Что делает бот:')


@user_private_rt.message(F.text.lower() == 'поддержка')
@user_private_rt.message(Command('support'))
async def about(message: types.Message):
    await message.answer('Свяжитесь с поддержкой')


@user_private_rt.message(F.text.lower() == 'оплата')
@user_private_rt.message(Command('payment'))
async def about(message: types.Message):
    await message.answer('Способы оплаты:')


@user_private_rt.message(F.text.lower() == 'доставка')
@user_private_rt.message(Command('shipping'))
async def about(message: types.Message):
    await message.answer('Способы доставки:')
