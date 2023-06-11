from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

authorization_kb = ReplyKeyboardBuilder().row(
            KeyboardButton(text="Авторизация", request_contact=True)).as_markup(
            resize_keyboard=True, one_time_keyboard=True)