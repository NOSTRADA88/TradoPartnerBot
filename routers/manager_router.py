from aiogram.filters import Text
from aiogram import Router, Bot
from config_data.config import Config, load_config
from aiogram.types import CallbackQuery, InputMediaPhoto, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from keyboards.inline_kb import back_kb, back_button

config: Config = load_config()
router: Router = Router()
bot: Bot = Bot(config.tg_bot.token, parse_mode="HTML")


@router.callback_query(Text(text="manager"))
async def my_manager_command(callback: CallbackQuery) -> None:
    manager_kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    manager_kb_builder.row(
        InlineKeyboardButton(text="✏️ Оставить обращение", callback_data="appeal")
    ).row(back_button)
    # await callback.message.edit_media(
    #     media=InputMediaPhoto(media=FSInputFile('photos/TgBot3.png'), caption="Илья Семёнов\n\nТелеграм: @ilyyyyaaa\nНомер телефона: + 7 (996) 404 7612\nПочта: trado.marketing@gmail.com\n\nОтветит на ваши вопросы 10:00-18:00"),
    #     reply_markup=manager_kb_builder.as_markup(resize_keyboard=True),
    # )
    await callback.message.edit_text(
        text="Илья Семёнов\n\nТелеграм: @ilyyyyaaa\nНомер телефона: + 7 (996) 404 7612\nПочта: trado.marketing@gmail.com\n\nОтветит на ваши вопросы 10:00-18:00",
        reply_markup=manager_kb_builder.as_markup(resize_keyboard=True)
    )


@router.callback_query(Text(text="appeal"))
async def appeal_to_manager(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        text="Обращение в ТРАДО по качеству работы менеджера, выплатам и условиям партнерской программы: https://forms.yandex.ru/u/6477620143f74f09d941514c/",
        reply_markup=back_kb
    )

