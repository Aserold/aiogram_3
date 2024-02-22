import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode

from config import TOKEN
from handlers.user_group import user_group_rt
from handlers.user_private import user_private_rt
from common.bot_cmd import private

ALLOWED_UPDATES = ['message', 'edited_message']

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

dp.include_router(user_private_rt)
dp.include_router(user_group_rt)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    # await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


if __name__ == '__main__':
    asyncio.run(main())
