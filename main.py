import asyncio

from sys import exit
from os import getenv
from loguru import logger
from aiogram.types import BotCommand
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot.filters.users import IsUser
from bot.handlers.bot_commands import register_bot_commands
from bot.handlers.ip import register_ip
from bot.handlers.user import register_users


def register_all_handlers(dp):
    register_bot_commands(dp)
    register_users(dp)
    register_ip(dp)


def register_all_filters(dp):
    dp.filters_factory.bind(IsUser)


async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Start bot"),
        BotCommand(command="user", description="Users management"),
        BotCommand(command="ip", description="IP management"),
        BotCommand(command="id", description="Get your Telegram ID"),
        BotCommand(command="version", description="Bot version"),
    ]
    await bot.set_my_commands(commands)


async def main():
    logger.add("logs/bot.log", level="INFO", encoding="utf8",
               format='{time:YYYY-MM-DD HH:mm:ss.SSS} | <level>{level: <8}</level> | {name}:{function}:{line} - '
                      '<level>{''message}</level>',
               filter=None, colorize=None, backtrace=True, diagnose=True, enqueue=False, catch=True,
               rotation="1 days", compression="zip")
    logger.add("logs/error.log", level="ERROR", encoding="utf8",
               format='{time:YYYY-MM-DD HH:mm:ss.SSS} | <level>{level: <8}</level> | {name}:{function}:{line} - '
                      '<level>{''message}</level>',
               filter=None, colorize=None, backtrace=True, diagnose=True, enqueue=False, catch=True,
               rotation="1 days", compression="zip")

    bot_token = getenv("BOT_TOKEN")
    if not bot_token:
        logger.error('Error: no Bot token provided')
        exit("Error: no Bot token provided")

    storage = MemoryStorage()
    bot = Bot(token=bot_token, parse_mode=types.ParseMode.HTML)
    dp = Dispatcher(bot, storage=storage)

    register_all_filters(dp)
    register_all_handlers(dp)

    await set_bot_commands(bot)

    logger.info('Bot started!')

    try:
        await dp.start_polling()
    finally:
        session = await bot.get_session()
        await session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped!")
