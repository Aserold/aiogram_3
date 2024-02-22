from string import punctuation

from aiogram import F, types, Router
from aiogram.filters import CommandStart, Command, or_f

from filters.chat_types import ChatTypeFilter

user_group_rt = Router()
user_group_rt.message.filter(ChatTypeFilter(['group', 'supergroup']))

restricted_words = {'урод', 'тварь', 'скотина'}


def clean_text(text: str):
    return text.translate(str.maketrans('', '', punctuation))


@user_group_rt.edited_message()
@user_group_rt.message()
async def punisher(message: types.Message):
    if restricted_words.intersection(clean_text(message.text.lower()).split()):
        await message.answer('Без ругани, шакалы!')
        await message.delete()
