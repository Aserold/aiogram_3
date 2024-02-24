from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_callback_buttons(
        *,
        buttons: dict[str, ...],
        sizes: tuple[int, ...] = (2,)
):
    keyboard = InlineKeyboardBuilder()

    for text, data in buttons.items():
        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))

    return keyboard.adjust(*sizes).as_markup()


def get_url_buttons(
        *,
        buttons: dict[str, ...],
        sizes: tuple[int, ...] = (2,)
):
    keyboard = InlineKeyboardBuilder()

    for text, url in buttons.items():
        keyboard.add(InlineKeyboardButton(text=text, url=url))

    return keyboard.adjust(*sizes).as_markup()


def get_mixed_buttons(
        *,
        buttons: dict[str, ...],
        sizes: tuple[int, ...] = (2,)
):
    keyboard = InlineKeyboardBuilder()

    for text, value in buttons.items():
        if '://' in value:
            keyboard.add(InlineKeyboardButton(text=text, url=value))
        else:
            keyboard.add(InlineKeyboardButton(text=text, callback_data=value))

    return keyboard.adjust(*sizes).as_markup()
