from loguru import logger
from aiogram import types, Dispatcher

from bot.handlers.ip import IpManagement
from bot.handlers.user import UserManagement
from bot.keyboards.inline import inline_kb_users
from bot.misc.ip import get_ips_list
from bot.misc.user import get_users


async def cmd_start(message: types.Message):
    logger.info(f'Command: <start> - {message.from_user.username}:{message.from_user.id}')
    await message.answer(f"Hello {message.from_user.username}")


async def cmd_version(message: types.Message):
    logger.info(f'Command: <version> - {message.from_user.username}:{message.from_user.id}')
    await message.answer("Bot version: <b>0.0.1</b>")


async def cmd_id(message: types.Message):
    logger.info(f'Command: <ID> - {message.from_user.username}:{message.from_user.id}')
    await message.answer(f"Your ID: <b>{message.from_user.id}</b>")


async def cmd_user(message: types.Message):
    logger.info(f'Command: <user> - {message.from_user.username}:{message.from_user.id}')
    users = get_users()
    msg = "<b>Users list:</b>"
    for user_id in users.keys():
        msg_user = f'{user_id} - {users.get(user_id)}'
        msg = msg + '\n' + msg_user
    await message.answer(msg, reply_markup=inline_kb_users)
    await UserManagement.waiting_add_or_del.set()


async def cmd_ip(message: types.Message):
    logger.info(f'Command: <add> - {message.from_user.username}:{message.from_user.id}')
    ips = get_ips_list()
    msg = "<b>IPs list:</b>"
    for ip in ips:
        msg = msg + '\n' + ip
    await message.answer(msg, reply_markup=inline_kb_users)
    await IpManagement.waiting_add_or_del.set()


def register_bot_commands(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=["start"], state='*', is_user=True)
    dp.register_message_handler(cmd_version, commands=["version"], state='*', is_user=True)
    dp.register_message_handler(cmd_id, commands=["id"], state='*', is_user=True)
    dp.register_message_handler(cmd_user, commands=["user"], state='*', is_user=True)
    dp.register_message_handler(cmd_ip, commands=["ip"], state='*', is_user=True)
