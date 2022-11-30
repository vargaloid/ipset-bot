from loguru import logger
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from bot.misc.ip import get_ips_list, add_ip, del_ip, ip_format_check


class IpManagement(StatesGroup):
    waiting_add_or_del = State()
    waiting_ip_add = State()
    waiting_ip_del = State()


async def callback_add_ip(callback_query: types.CallbackQuery):
    logger.info(f'Command: <ip> - Callback Query - <{callback_query.data}>')
    await callback_query.message.edit_text(text='✍️Enter IP address')
    await IpManagement.waiting_ip_add.set()


async def callback_del_ip(callback_query: types.CallbackQuery):
    logger.info(f'Command: <ip> - Callback Query - <{callback_query.data}>')
    ips = get_ips_list()
    msg = "<b>IPs list:</b>"
    for ip in ips:
        msg = msg + '\n' + ip
    msg = msg + '\n\n✍️Enter IP you want to delete'
    await callback_query.message.edit_text(msg)
    await IpManagement.waiting_ip_del.set()


async def enter_add_ip(message: types.Message, state: FSMContext):
    logger.info(f'Command: <ip> - Forwarded message to add user - <{message.forward_from}>')
    check_ip = ip_format_check(message.text)
    if check_ip is None:
        await message.answer("⚠️Wrong IP format")
    else:
        add_status = add_ip(message.text)
        if add_status == 0:
            await message.answer("IP successfully added!🤝\n\n")
        elif add_status == 1:
            await message.answer("IP already exists!🤦‍♂️")
        else:
            await message.answer("Error!🤦‍♂️")
    await state.finish()


async def enter_del_ip(message: types.Message, state: FSMContext):
    logger.info(f'Command: <ip> - Message to del user - <{message.text}>')
    check_ip = ip_format_check(message.text)
    if check_ip is None:
        await message.answer("⚠️Wrong IP format")
    else:
        del_status = del_ip(message.text)
        # there may be no such IP
        if del_status == 0:
            await message.answer("IP successfully deleted!💀")
        elif del_status == 1:
            await message.answer("There is no such IP 🤷‍♂️")
        else:
            await message.answer("Error!🤦‍♂️")
    await state.finish()


def register_ip(dp: Dispatcher):
    dp.register_callback_query_handler(callback_add_ip, lambda c: c.data == 'add_user',
                                       state=IpManagement.waiting_add_or_del, is_user=True)
    dp.register_callback_query_handler(callback_del_ip, lambda c: c.data == 'del_user',
                                       state=IpManagement.waiting_add_or_del, is_user=True)
    dp.register_message_handler(enter_add_ip, content_types=["text", "sticker"],
                                state=IpManagement.waiting_ip_add, is_user=True)
    dp.register_message_handler(enter_del_ip,
                                state=IpManagement.waiting_ip_del, is_user=True)
