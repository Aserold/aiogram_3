from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command

from filters.chat_types import ChatTypeFilter
from keyboards.reply import start_kb3, del_kb, test_kb

user_private_rt = Router()
user_private_rt.message.filter(ChatTypeFilter(['private']))


@user_private_rt.message((F.text.lower().contains('здрав')) | (F.text.lower().contains('приве')))
@user_private_rt.message(CommandStart())
async def start_task(message: types.Message):
    name = message.from_user.first_name
    await message.answer(f'Ну привет, {name}!😈', reply_markup=start_kb3.as_markup(
        resize_keyboard=True, input_field_placeholder='Выберите кнопку')
    )


@user_private_rt.message(F.text.lower() == 'меню')
@user_private_rt.message(Command('menu'))
async def menu(message: types.Message):
    await message.answer('Вот меню:', reply_markup=del_kb)


@user_private_rt.message(F.text.lower().contains('бот'))
@user_private_rt.message(Command('about'))
async def about(message: types.Message):
    await message.answer('Что делает бот:', reply_markup=test_kb)


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


@user_private_rt.message(F.location)
async def get_lo(message: types.Message):
    await message.answer('Ваша локация в наших владениях')
    await message.answer(str(message.location))


@user_private_rt.message(F.contact)
async def get_lo(message: types.Message):
    await message.answer('Ваш телефон в наших владениях')
    await message.answer(str(message.contact))
