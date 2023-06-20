from aiogram.filters import Text
from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from config_data.config import Config, load_config
from aiogram.types import CallbackQuery, InputMediaPhoto, FSInputFile
from keyboards.inline_kb import main_kb, back_kb
from routers.start_router import UserPhone

config: Config = load_config()
router: Router = Router()
bot: Bot = Bot(config.tg_bot.token, parse_mode="HTML")


class DefaultState(UserPhone):
    phone_number: UserPhone = UserPhone.phone_number


@router.callback_query(Text(text="base_knowledge"))
async def base_knowledge_command(callback: CallbackQuery) -> None:
    await callback.message.edit_media(
        media=InputMediaPhoto(media=FSInputFile('photos/base_knowledge.png'), caption="Информация о продуктах, их использовании, а также об ингредиентах: https://trado-znaniya.gitbook.io/products/"),
        reply_markup=back_kb
    )


@router.callback_query(Text(text="back_to_main"))
async def back_to_main_menu_command(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(DefaultState.phone_number)
    await callback.message.edit_media(
        media=InputMediaPhoto(media=FSInputFile('photos/main_menu.png'), caption="Добро пожаловать в панель партнера ТРАДО.\n\nВыберите нужную кнопку:"),
        reply_markup=main_kb
    )
