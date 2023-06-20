import asyncio

from aiogram.filters import Text
from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from config_data.config import Config, load_config
from aiogram.types import CallbackQuery, InputMediaPhoto, FSInputFile
from keyboards.inline_kb import work_kb, back_to_work_kb, back_kb
from config_data.site_api import get_clients, get_account_details, get_user_id
from routers.start_router import UserPhone

config: Config = load_config()
router: Router = Router()
bot: Bot = Bot(config.tg_bot.token, parse_mode="HTML")


class Work(UserPhone):
    phone_number: UserPhone = UserPhone.phone_number


@router.callback_query(Text(text="work"))
async def work_command(callback: CallbackQuery, state: FSMContext) -> None:
    phone_number = await state.get_data()
    user_id = await get_user_id(phone_number['phone_number'])
    account_details = await get_account_details(user_id)
    balance_all_time = "{:,.2f}".format(account_details['incoming_balance_all_time']).replace(',', ' ')
    last_month = "{:,.2f}".format(account_details['last_month_incoming']).replace(',', ' ')
    current_balance = "{:,.2f}".format(account_details['balance']).replace(',', ' ')
    await callback.message.edit_media(
        media=InputMediaPhoto(media=FSInputFile('photos/income.png'), caption=f"Текущий баланс кошелька: {current_balance}\n\nЗа прошлый месяц вы заработали: {last_month}\n\nВсего заработано: {balance_all_time}"),
        reply_markup=work_kb
    )


@router.callback_query(Text(text="clients"))
async def clients_command(callback: CallbackQuery, state: FSMContext) -> None:
    phone_number = await state.get_data()
    user_id = await get_user_id(phone_number['phone_number'])
    clients_list = await get_clients(user_id)
    clients_list = [" ".join([client_dict['consignee'], client_dict['product_name'], '-', client_dict['sale_amount'], 'руб.', f'({client_dict["sale_date"]} в {client_dict["sale_time"]} по мск)']) for client_dict in clients_list]
    client_str = ''
    for iteration in range(len(clients_list)):
        client_str += clients_list[iteration] + "\n"
    await callback.message.edit_media(
        media=InputMediaPhoto(media=FSInputFile('photos/clients.png'), caption=f'Последние клиенты:\n{client_str if client_str else "похоже, что тут пока пусто 😔"}'),
        reply_markup=back_to_work_kb
    )


@router.callback_query(Text(text="withdraw_money"))
async def withdraw_money_command(callback: CallbackQuery) -> None:
    await callback.message.edit_media(
        media=InputMediaPhoto(media=FSInputFile("photos/manager.png"), caption='Пожалуйста, свяжитесь с вашим персональным менеджером, чтобы заполнить заявку на вывод средств\n\nТелеграм: @ilyyyyaaa\nНомер телефона: + 7 (996) 404 7612\nПочта: trado.marketing@gmail.com'),
        reply_markup=back_kb
    )
