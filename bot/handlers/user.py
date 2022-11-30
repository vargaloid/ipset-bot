from loguru import logger
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from bot.misc.user import get_users, add_user, del_user


class UserManagement(StatesGroup):
    waiting_add_or_del = State()
    waiting_forwarded_message = State()
    waiting_user_to_del = State()


async def callback_add_user(callback_query: types.CallbackQuery):
    logger.info(f'Command: <user> - Callback Query - <{callback_query.data}>')
    await callback_query.message.edit_text(text='To add - forward to me any message from the user you want to add')
    await UserManagement.waiting_forwarded_message.set()


async def callback_del_user(callback_query: types.CallbackQuery):
    logger.info(f'Command: <user> - Callback Query - <{callback_query.data}>')
    users = get_users()
    msg = "<b>Users list:</b>"
    for user_id in users.keys():
        msg_user = f'{user_id} - {users.get(user_id)}'
        msg = msg + '\n' + msg_user
    msg = msg + '\n\nWhich user you want to delete (provide ID)?'
    await callback_query.message.edit_text(msg)
    await UserManagement.waiting_user_to_del.set()


async def forwarded_message_add_user(message: types.Message, state: FSMContext):
    logger.info(f'Command: <user> - Forwarded message to add user - <{message.forward_from}>')
    # Telegram user can have forward message privacy
    if message.forward_from:
        adding_status = add_user(message)
        if adding_status:
            await message.answer("User successfully added!🤝\n\n"
                                 f"ID: <b>{message.forward_from.id}</b>\n"
                                 f"Name: <b>{message.forward_from.username}</b>\n")
        else:
            await message.answer("User already exists!🤦‍♂️")
    else:
        await message.answer("User has forward message privacy. 🤷‍♂️ Please, add user manually.")
    await state.finish()


async def id_del_user(message: types.Message, state: FSMContext):
    logger.info(f'Command: <user> - Message to del user - <{message.text}>')
    del_status = del_user(message.text)
    # there may be no such user
    if del_status is None:
        await message.answer("There is no user with such telegram ID 🤷‍♂️")
    else:
        await message.answer("User successfully deleted!💀")
    await state.finish()


def register_users(dp: Dispatcher):
    dp.register_callback_query_handler(callback_add_user, lambda c: c.data == 'add_user',
                                       state=UserManagement.waiting_add_or_del, is_user=True)
    dp.register_callback_query_handler(callback_del_user, lambda c: c.data == 'del_user',
                                       state=UserManagement.waiting_add_or_del, is_user=True)
    dp.register_message_handler(forwarded_message_add_user, content_types=["text", "sticker"],
                                state=UserManagement.waiting_forwarded_message, is_user=True)
    dp.register_message_handler(id_del_user,
                                state=UserManagement.waiting_user_to_del, is_user=True)
