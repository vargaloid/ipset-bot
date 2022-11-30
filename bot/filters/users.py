from loguru import logger
from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from bot.misc.user import get_users_ids


class IsUser(BoundFilter):
    key = 'is_user'

    def __init__(self, is_user: bool):
        self.is_user = is_user

    async def check(self, message: types.Message) -> bool:
        user = message.from_user.id
        users_list = get_users_ids()
        if user in users_list:
            logger.info(f'User Filter - <{user}> is in users <{users_list}>')
        else:
            logger.info(f'User Filter - <{user}> is not in users <{users_list}>')
        return user in users_list
