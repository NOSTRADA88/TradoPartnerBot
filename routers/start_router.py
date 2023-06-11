from datetime import datetime
from middleware.db import DataBase
from aiogram.filters import CommandStart, StateFilter
from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from config_data.site_api import get_user_id, get_account_details, get_referrals
from config_data.config import Config, load_config
from keyboards.reply_kb import authorization_kb
from aiogram.types import Message, FSInputFile
from keyboards.inline_kb import main_kb
import asyncio
from aiogram.types import ReplyKeyboardRemove

config: Config = load_config()
router: Router = Router()
bot: Bot = Bot(config.tg_bot.token, parse_mode='HTML')
db: DataBase = DataBase()


class UserPhone(StatesGroup):
    phone_number: State = State()


@router.message(CommandStart())
async def command_start_ask_phone(message: Message, state: FSMContext):
    photo = FSInputFile(path="photos/TgBot1.png")
    await bot.send_photo(
        chat_id=message.from_user.id,
        photo=photo,
        caption="Здравствуйте.\nДля начала работы в Панели, вам нужно авторизоваться. Нажмите кнопку «Авторизация», чтобы поделиться номером телефона",
        reply_markup=authorization_kb
    )
    await state.set_state(UserPhone.phone_number)
    await asyncio.sleep(45)


@router.message(StateFilter(UserPhone.phone_number), F.contact)
async def command_start(message: Message, state: FSMContext) -> None:
    phone_number = message.contact.phone_number if '+' in message.contact.phone_number else '+' + message.contact.phone_number
    if await get_user_id(phone_number):
        if not db.check_phone_number(phone_number) and not db.check_user_id(phone_number, message.from_user.id):
            db.add_phone_number(phone_number)
            db.update_user_id(phone_number, message.from_user.id)
            db.update_spam_1(phone_number, datetime.now())
            db.update_spam_2(phone_number, db.get_spam_1(phone_number))
            db.update_spam_3(phone_number, db.get_spam_2(phone_number))
        user_id = await get_user_id(phone_number)
        account_details = await get_account_details(user_id)
        if not db.check_client_name(phone_number, account_details['first_name']):
            db.update_client_name(phone_number, account_details['first_name'])
        referrals = await get_referrals(user_id)
        if not db.check_link10(phone_number, referrals['link_10']) and not db.check_link25(
                phone_number, referrals['link_25']):
            db.update_link10(phone_number, referrals['link_10'])
            db.update_link25(phone_number, referrals['link_25'])
        await state.update_data(phone_number=phone_number)
        await bot.send_chat_action(chat_id=message.from_user.id, action='typing')
        await asyncio.sleep(3)

        msg_1 = await bot.send_message(
            chat_id=message.from_user.id,
            text="Здравствуйте! Спасибо, что присоединились к партнерской программе ТРАДО.\n\nСейчас расскажу, как этот бот поможет вам в работе",
            reply_markup=ReplyKeyboardRemove()
        )
        await bot.send_chat_action(chat_id=message.from_user.id, action='typing')
        await asyncio.sleep(5)
        # await bot.delete_message(chat_id=message.from_user.id, message_id=msg_0.message_id)

        msg_2 = await bot.send_message(
            chat_id=message.from_user.id,
            text='Кнопка "Работа" - позволит узнать текущий баланс, а также получить статистику продаж по вашей партнерской ссылке',
        )
        await bot.send_chat_action(chat_id=message.from_user.id, action='typing')
        await asyncio.sleep(5)
        # await bot.delete_message(chat_id=message.from_user.id, message_id=msg_1.message_id)

        msg_3 = await bot.send_message(
            chat_id=message.from_user.id,
            text='"База знаний" - получить больше информации о препаратах и работе партнерской программы',
        )
        await bot.send_chat_action(chat_id=message.from_user.id, action='typing')
        await asyncio.sleep(5)
        # await bot.delete_message(chat_id=message.from_user.id, message_id=msg_2.message_id)

        msg_4 = await bot.send_message(
            chat_id=message.from_user.id,
            text='"Ссылка" - отправим уникальную ссылку на сайт, привязанную к вам, как к партнеру\n\nКогда человек делает покупку по этой ссылке, вам начисляется вознаграждение',
        )
        await bot.send_chat_action(chat_id=message.from_user.id, action='typing')
        await asyncio.sleep(5)
        # await bot.delete_message(chat_id=message.from_user.id, message_id=msg_3.message_id)

        msg_5 = await bot.send_message(
            chat_id=message.from_user.id,
            text='"Менеджер" - отправим ссылку на вашего личного менеджера, который поможет в чем-то разобраться или решить проблему',
        )
        await bot.send_chat_action(chat_id=message.from_user.id, action='typing')
        await asyncio.sleep(5)
        # await bot.delete_message(chat_id=message.from_user.id, message_id=msg_4.message_id)

        msg_6 = await bot.send_message(
            chat_id=message.from_user.id,
            text='А также бот будет уведомлять вас о важных событиях в партнерской программе и обучениях по препаратам.\n\nНадеюсь, что наша работа будет продолжаться долго и принесет не только денежный результат, но и поможет людям избавиться от проблем со здоровьем',
        )
        await bot.send_chat_action(chat_id=message.from_user.id, action='typing')
        await asyncio.sleep(5)
        # await bot.delete_message(chat_id=message.from_user.id, message_id=msg_5.message_id)

        msg_7 = await bot.send_message(
            chat_id=message.from_user.id,
            text='Давайте начинать работу',
        )
        await bot.send_chat_action(chat_id=message.from_user.id, action='typing')
        await asyncio.sleep(3)
        # await bot.delete_message(chat_id=message.from_user.id, message_id=msg_6.message_id)

        await bot.send_message(
            chat_id=message.from_user.id,
            text="Добро пожаловать в панель партнера ТРАДО.\n\nВыберите нужную кнопку:",
            reply_markup=main_kb
        )
    else:
        await bot.send_message(
            chat_id=message.from_user.id,
            text='При авторизации произошла ошибка.\n\nЗарегистрироваться: https://www.tradoclub.ru/cooperation/register-as-club-member/\n\nСтолкнулись с проблемой: https://forms.yandex.ru/u/6477620143f74f09d941514c/'
        )
        await state.clear()


@router.message()
async def default_answer(message: Message) -> None:
    await bot.send_message(
        chat_id=message.from_user.id,
        text='Для того, чтобы отправить сообщение, воспользуйтесь формой "Мой менеджер - Оставить обращение"',
        reply_markup=main_kb
    )


async def send_spam_1(bot: Bot = Bot(config.tg_bot.token)):
    clients_list = db.get_all_clients()
    for iteration in range(0, len(clients_list)):
        client_data_tuple = clients_list[iteration]
        if client_data_tuple[6] - datetime.now().timestamp() <= 0:
            photo = FSInputFile('photos/TgBot5.png')
            await bot.send_photo(
                chat_id=client_data_tuple[5],
                photo=photo,
                caption=f"Уже прямо сейчас вы можете начать работу с нами.\n\nОтправляем ссылки, которыми вы можете делиться с клиентами на личных консультациях или в своих соцсетях\n\nСкидка 10%: {client_data_tuple[2]}\nСкидка 25%: {client_data_tuple[3]}",
                reply_markup=main_kb
            )
            db.update_spam_1(client_data_tuple[1], datetime.now())


async def send_spam_2(bot: Bot = Bot(config.tg_bot.token)):
    clients_list = db.get_all_clients()
    for iteration in range(0, len(clients_list)):
        client_data_tuple = clients_list[iteration]
        if client_data_tuple[7] - datetime.now().timestamp() <= 0:
            photo = FSInputFile("photos/TgBot6.png")
            await bot.send_photo(
                chat_id=client_data_tuple[5],
                photo=photo,
                caption=f"Увеличьте свои продажи на 30%. Разместите пост с продукцией ТРАДО в социальных сетях и получите до 1000 рублей от компании за рекламу продукта. Узнайте подробнее у персонального менеджера",
                reply_markup=main_kb
            )
            db.update_spam_2(client_data_tuple[1], db.get_spam_1(client_data_tuple[1]))


async def send_spam_3(bot: Bot = Bot(config.tg_bot.token)):
    clients_list = db.get_all_clients()
    for iteration in range(0, len(clients_list)):
        client_data_tuple = clients_list[iteration]
        if client_data_tuple[8] - datetime.now().timestamp() <= 0:
            photo = FSInputFile("photos/TgBot4.png")
            await bot.send_photo(
                chat_id=client_data_tuple[5],
                photo=photo,
                caption=f"Узнайте новую полезную информацию о продуктах ТРАДО в нашей базе знаний:",
                reply_markup=main_kb
            )
            db.update_spam_3(client_data_tuple[1], db.get_spam_2(client_data_tuple[1]))

