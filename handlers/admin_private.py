from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.ext.asyncio import AsyncSession
from database.orm_queries import orm_add_product, orm_get_products, orm_delete_product
from filters.chat_types import ChatTypeFilter, IsAdmin
from keyboards.inline import get_callback_buttons
from keyboards.reply import create_kb_reply

admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())

ADMIN_KB = create_kb_reply(
    "Добавить товар",
    "Каталог",
    placeholder="Выберите действие",
    sizes=(2,),
)


@admin_router.message(Command("admin"))
async def add_product(message: types.Message):
    await message.answer("Что хотите сделать?", reply_markup=ADMIN_KB)


@admin_router.message(F.text == "Каталог")
async def starring_at_product(message: types.Message, session: AsyncSession):
    for product in await orm_get_products(session):
        await message.answer_photo(
            product.image,
            caption=f'<strong>{product.name}</strong>\
                    \n{product.description}\nЦена: {round(product.price, 2)} руб.',
            reply_markup=get_callback_buttons(buttons={
                'Удалить': f'delete_{product.id}',
                'Изменить': f'edit_{product.id}',
            })
        )
    await message.answer("ОК, вот список товаров")


@admin_router.callback_query(F.data.startswith("delete_"))
async def delete_product(callback: types.CallbackQuery, session: AsyncSession):
    print(callback.data)
    product_id = int(callback.data.split('_')[-1])
    await orm_delete_product(session, product_id)

    await callback.answer('Товар удален!')
    await callback.message.answer("Товар удален!")


class AddProduct(StatesGroup):
    name = State()
    description = State()
    price = State()
    image = State()

    texts = {
        'AddProduct:name': "Введите название товара",
        'AddProduct:description': "Введите описание товара",
        'AddProduct:price': "Введите цену товара",
        'AddProduct:image': "Введите ссылку на изображение товара",
    }


@admin_router.message(StateFilter(None), F.text == "Добавить товар")
async def add_product(message: types.Message, state: FSMContext):
    await message.answer(
        "Введите название товара", reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(AddProduct.name)


@admin_router.message(StateFilter('*'), Command("cancel"))
@admin_router.message(StateFilter('*'), F.text.casefold() == "отмена")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer("Действия отменены", reply_markup=ADMIN_KB)


@admin_router.message(Command("назад"))
@admin_router.message(F.text.casefold() == "назад")
async def back_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()

    if current_state == AddProduct.name:
        await cancel_handler(message=message, state=state)
        return

    previous = None
    for step in AddProduct.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(f'Ок, вы вернулись к предыдущему шагу\n{AddProduct.texts[previous.state]}')
            return
        previous = step

    await message.answer(f"ок, вы вернулись к прошлому шагу")


@admin_router.message(AddProduct.name, F.text)
async def add_name(message: types.Message, state: FSMContext):
    if len(message.text) >= 150:
        await message.answer("Название товара не может быть более 150 символов")
        return
    await state.update_data(name=message.text)
    await message.answer("Введите описание товара")
    await state.set_state(AddProduct.description)


@admin_router.message(AddProduct.name)
async def incorrect_name(message: types.Message, state: FSMContext):
    await message.answer("Пожалуйста введите текст, названия товара")


@admin_router.message(AddProduct.description, F.text)
async def add_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Введите стоимость товара цифрами\nНапример: 1000")
    await state.set_state(AddProduct.price)


@admin_router.message(AddProduct.description)
async def incorrect_description(message: types.Message, state: FSMContext):
    await message.answer("Пожалуйста введите текст, описывающий товар")


@admin_router.message(AddProduct.price, F.text)
async def add_price(message: types.Message, state: FSMContext):
    price = message.text
    try:
        price = float(price)
        await state.update_data(price=price)
        await message.answer("Загрузите изображение товара")
        await state.set_state(AddProduct.image)
    except ValueError:
        await message.answer("Пожалуйста введите стоимость товара цифрами без пробелов\nНапример: <b>1000</b>")

    # await state.update_data(price=price)
    # await message.answer("Загрузите изображение товара")
    # await state.set_state(AddProduct.image)


@admin_router.message(AddProduct.price)
async def incorrect_price(message: types.Message, state: FSMContext):
    await message.answer("Пожалуйста введите стоимость товара цифрами без пробелов\nНапример: <b>1000</b>")


@admin_router.message(AddProduct.image, F.photo)
async def add_image(message: types.Message, state: FSMContext, session: AsyncSession):

    await state.update_data(image=message.photo[-1].file_id)
    await message.answer("Товар добавлен", reply_markup=ADMIN_KB)
    data = await state.get_data()

    await orm_add_product(session=session, data=data)

    await state.clear()


@admin_router.message(AddProduct.image)
async def incorrect_image(message: types.Message, state: FSMContext):
    await message.answer("Пожалуйста отправьте изображение товара")
