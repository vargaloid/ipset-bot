
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


inline_btn_user_add = InlineKeyboardButton('➕Add', callback_data='add_user')
inline_btn_user_del = InlineKeyboardButton('❌Delete', callback_data='del_user')
inline_kb_users = InlineKeyboardMarkup(row_width=2).add(inline_btn_user_add, inline_btn_user_del)
