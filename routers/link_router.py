from aiogram.filters import Text
from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from config_data.config import Config, load_config
from aiogram.types import CallbackQuery
from keyboards.inline_kb import main_kb, back_kb
from routers.start_router import UserPhone
from config_data.site_api import get_referrals, get_user_id

config: Config = load_config()
router: Router = Router()
bot: Bot = Bot(config.tg_bot.token, parse_mode="HTML")


class MyLink(UserPhone):
    phone_number = UserPhone.phone_number


@router.callback_query(Text(text="link"))
async def base_knowledge_command(callback: CallbackQuery, state: FSMContext) -> None:
    phone_number = await state.get_data()
    user_id = await get_user_id(phone_number['phone_number'])
    referrals = await get_referrals(user_id)
    await callback.message.edit_text(
        text=f"Делитесь ссылкой на консультациях, в социальных сетях, сайтах и других площадках, где находятся ваши потенциальны клиенты.\n\nСкидка 10%: {referrals['link_10']}\nСкидка 25%: {referrals['link_25']}",
        reply_markup=back_kb
    )


@router.callback_query(Text(text="back_to_main"))
async def back_to_main_menu_command(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        text="Добро пожаловать в панель партнера ТРАДО.\n\nВыберите нужную кнопку:",
        reply_markup=main_kb
    )
