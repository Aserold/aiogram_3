from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, KeyboardButtonPollType
from aiogram.utils.keyboard import ReplyKeyboardBuilder

start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Меню'),
            KeyboardButton(text='О боте'),
        ],
        [
            KeyboardButton(text='Оплата'),
            KeyboardButton(text='Доставка'),
        ],
        [
            KeyboardButton(text='Поддержка'),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder='Выберите кнопку'
)

del_kb = ReplyKeyboardRemove()


start_kb2 = ReplyKeyboardBuilder()
start_kb2.add(
    KeyboardButton(text='Меню'),
    KeyboardButton(text='О боте'),
    KeyboardButton(text='Оплата'),
    KeyboardButton(text='Доставка'),
    KeyboardButton(text='Поддержка'),
)
start_kb2.adjust(2, 3)


start_kb3 = ReplyKeyboardBuilder()
start_kb3.attach(start_kb2)
start_kb3.row(KeyboardButton(text='Оставить отзыв'))


test_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Poll', request_poll=KeyboardButtonPollType()),
        ],
        [
            KeyboardButton(text='Numba', request_contact=True),
            KeyboardButton(text='gimme that lo', request_location=True)
        ]
    ],
    resize_keyboard=True
)
