from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, KeyboardButtonPollType
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def create_kb_reply(
        *buttons: str,
        placeholder: str = None,
        request_location: int = None,
        request_contact: int = None,
        sizes: tuple[int, ...] = (2,)
):
    """
    Create reply keyboard

    :param buttons:
    :param placeholder:
    :param request_location:
    :param request_contact:
    :param sizes:
    :return:
    """
    keyboard = ReplyKeyboardBuilder()

    for index, text in enumerate(buttons, start=0):
        if request_contact is not None and request_contact == index:
            keyboard.add(KeyboardButton(text=text, request_contact=True))
        elif request_location is not None and request_location == index:
            keyboard.add(KeyboardButton(text=text, request_location=True))
        else:
            keyboard.add(KeyboardButton(text=text))

    return keyboard.adjust(*sizes).as_markup(resize_keyboard=True, input_field_placeholder=placeholder)
