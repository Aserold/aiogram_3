from string import punctuation

from aiogram import types, Router, Bot
from aiogram.filters import Command

from filters.chat_types import ChatTypeFilter

user_group_rt = Router()
user_group_rt.message.filter(ChatTypeFilter(['group', 'supergroup']))

restricted_words = {'урод', 'тварь', 'скотина'}


@user_group_rt.message(Command('admin'))
async def get_admins(message: types.Message, bot: Bot):
    chat_id = message.chat.id
    admins_list = await bot.get_chat_administrators(chat_id)
    admins_list = [
        member.user.id
        for member in admins_list
        if member.status == 'creator' or member.status == 'administrator'
    ]
    bot.my_admins_list = admins_list
    if message.from_user.id in admins_list:
        await message.delete()


def clean_text(text: str):
    return text.translate(str.maketrans('', '', punctuation))


@user_group_rt.edited_message()
@user_group_rt.message()
async def punisher(message: types.Message):
    if message.text is not None:
        if restricted_words.intersection(clean_text(message.text.lower()).split()):
            await message.answer('Без ругани, шакалы!')
            await message.delete()
