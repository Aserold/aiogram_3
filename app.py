import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import TOKEN
from database.engine import create_db, drop_db, session_maker
from handlers.admin_private import admin_router
from handlers.user_group import user_group_rt
from handlers.user_private import user_private_rt
from common.bot_cmd import private
from midlewares.database import DatabaseSession

# from midlewares.database import CounterMiddleware

# ALLOWED_UPDATES = ['message', 'edited_message', 'callback_query']

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
bot.my_admins_list = [1311756393,]

dp = Dispatcher()

# admin_router.message.middleware(CounterMiddleware())

dp.include_router(user_group_rt)
dp.include_router(admin_router)
dp.include_router(user_private_rt)


async def on_startup(bot):
    run_param = False
    if run_param:
        await drop_db()

    await create_db()


async def on_shutdown(bot):
    print('Shutting down...')


async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.update.middleware(DatabaseSession(session_pool=session_maker))
    await bot.delete_webhook(drop_pending_updates=True)
    # await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    asyncio.run(main())
