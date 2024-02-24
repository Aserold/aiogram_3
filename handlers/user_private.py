from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_queries import orm_get_products
from filters.chat_types import ChatTypeFilter
from keyboards.reply import create_kb_reply

user_private_rt = Router()
user_private_rt.message.filter(ChatTypeFilter(['private']))


@user_private_rt.message((F.text.lower() == 'в начало') | (F.text.lower().contains('приве')))
@user_private_rt.message(CommandStart())
async def start_task(message: types.Message):
    name = message.from_user.first_name
    await message.answer(f'Ну привет, {name}!😈\nНажмите на одну из кнопок ниже, чтобы воспользоваться ботом!', reply_markup=create_kb_reply(
        'Меню',
        'Оплата',
        'Доставка',
        'Сведения',
        'Поддержка',
        sizes=(2, 2, 1)
    )
                         )


@user_private_rt.message(F.text == 'Меню')
@user_private_rt.message(Command('menu'))
async def menu(message: types.Message, session: AsyncSession):
    for product in await orm_get_products(session):
        await message.answer_photo(
            product.image,
            caption=f'<strong>{product.name}</strong>\
                    \n{product.description}\nЦена: {round(product.price, 2)} руб.',
        )
    await message.answer('Вот меню:')


@user_private_rt.message(F.text.lower().contains('сведения'))
@user_private_rt.message(Command('about'))
async def about(message: types.Message):
    await message.answer('Этот бот может быть закажет для тебя пиццу, но только если хорошо попросишь😁')


@user_private_rt.message(F.text.lower() == 'поддержка')
@user_private_rt.message(Command('support'))
async def about(message: types.Message):
    await message.answer('Свяжитесь с поддержкой', reply_markup=create_kb_reply(
        'Отправить свой контакт для связи',
        'В начало',
        request_contact=0,
        sizes=(1, 1)
    ))


@user_private_rt.message(F.text.lower() == 'оплата')
@user_private_rt.message(Command('payment'))
async def about(message: types.Message):
    await message.answer('Способы оплаты:')


@user_private_rt.message(F.text.lower() == 'доставка')
@user_private_rt.message(Command('shipping'))
async def about(message: types.Message):
    await message.answer('Локация для доставки:', reply_markup=create_kb_reply(
        'Отправить свою локацию',
        'В начало',
        request_location=0,
        sizes=(1, 1)
    ))


@user_private_rt.message(F.location)
async def get_lo(message: types.Message):
    await message.answer('Ваша локация в наших владениях')
    await message.answer(str(message.location))


@user_private_rt.message(F.contact)
async def get_lo(message: types.Message):
    await message.answer('Ваш телефон в наших владениях')
    await message.answer(str(message.contact))


# @user_private_rt.message((F.text | ~(F.text != '/admin')) & types.Message.from_user.id)
@user_private_rt.message((F.text | ~(F.text != '/admin')))
async def base_answer(message: types.Message):
    await message.answer('Пожалуйста выберите кнопку ниже или выполните комманду /start')
