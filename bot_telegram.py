from aiogram.utils import executor
from create_bot import dp
from handlers import admin, client
from data_base import sqlite_db


async def bot_start(_):
    print('Bot online')



admin.register_handler_admin(dp)
client.register_handler_client(dp)


executor.start_polling(dp, skip_updates=True, on_startup=bot_start)
