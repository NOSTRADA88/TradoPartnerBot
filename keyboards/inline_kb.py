from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, InlineKeyboardMarkup

"""Main keyboard"""
main_buttons_kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

work_button: InlineKeyboardButton = InlineKeyboardButton(
    text=" 💼 Работа",
    callback_data="work"
)
base_knowledge_button: InlineKeyboardButton = InlineKeyboardButton(
    text="📖 База знаний",
    callback_data="base_knowledge"
)
link_button: InlineKeyboardButton = InlineKeyboardButton(
    text="📌 Моя ссылка",
    callback_data="link"
)
manager_button: InlineKeyboardButton = InlineKeyboardButton(
    text="👨‍💼 Мой менеджер",
    callback_data="manager"
)
main_buttons_kb_builder.row(work_button, base_knowledge_button).row(link_button, manager_button)
main_kb: InlineKeyboardMarkup = main_buttons_kb_builder.as_markup(resize_keyboard=True)

"""Back to main keyboard"""
back_kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

back_button: InlineKeyboardButton = InlineKeyboardButton(
    text="↩️ Главное меню",
    callback_data="back_to_main"
)
back_kb_builder.row(back_button)
back_kb: InlineKeyboardMarkup = back_kb_builder.as_markup(resize_keyboard=True)

"""work kb"""

work_kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
work_kb_builder.row(
    InlineKeyboardButton(text="👫 Клиенты", callback_data="clients"),
    InlineKeyboardButton(text="💰Вывести деньги", callback_data="withdraw_money")
).row(back_button)
work_kb = work_kb_builder.as_markup(resize_keyboard=True)

"""back to work kb"""

back_to_work_kb = InlineKeyboardBuilder().row(
            InlineKeyboardButton(text="Назад", callback_data="work")
        ).as_markup(resize_keyboard=True)
