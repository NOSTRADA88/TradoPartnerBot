from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from config_data.config import Config, load_config
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from routers import start_router, base_knowledge_router, link_router, manager_router, work_router
import asyncio
from middleware.db import DataBase
from routers.start_router import send_spam_1, send_spam_2, send_spam_3


async def start_bot():
    config: Config = load_config('.env')
    bot: Bot = Bot(config.tg_bot.token)
    storage: RedisStorage = RedisStorage.from_url(config.redis.url)
    dp: Dispatcher = Dispatcher(storage=storage)
    db: DataBase = DataBase()
    db.create_table()

    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(send_spam_1, trigger='interval', seconds=3, kwargs={'bot': bot})
    scheduler.add_job(send_spam_2, trigger='interval', seconds=3, kwargs={'bot': bot})
    scheduler.add_job(send_spam_3, trigger='interval', seconds=3, kwargs={'bot': bot})
    scheduler.start()

    dp.include_router(start_router.router)
    dp.include_router(base_knowledge_router.router)
    dp.include_router(link_router.router)
    dp.include_router(manager_router.router)
    dp.include_router(work_router.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(start_bot())
