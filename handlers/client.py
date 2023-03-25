from create_bot import bot, dp
from aiogram.dispatcher import Dispatcher
from aiogram import types
from buttons import client_keyboard
from data_base import sqlite_db


async def start_command(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Выберите пункт меню:', \
                               reply_markup=client_keyboard.client_buttons_menu_first_level)
    except:
        await message.reply('Общение с ботом через личные сообщения, напишите ему: '
                            '\nhttps://t.me/Filter2000_bot')


async def show_price_list(callback: types.callback_query):
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    await bot.send_message(callback.from_user.id, 'Выбирете интересующие фильтра', \
                           reply_markup=client_keyboard.client_buttons_menu_second_level)


async def show_air_filter(message: types.Message):
    sqlite_db.price_list = 'air_filter'
    sqlite_db.sql_start()
    await sqlite_db.sql_read(message)
    await command_back(message)


async def show_fuel_filter(message: types.Message):
    sqlite_db.price_list = 'fuel_filter'
    sqlite_db.sql_start()
    await sqlite_db.sql_read(message)
    await command_back(message)


async def show_oil_filter(message: types.Message):
    sqlite_db.price_list = 'oil_filter'
    sqlite_db.sql_start()
    await sqlite_db.sql_read(message)
    await command_back(message)


async def command_back(callback: types.callback_query):
    # await bot.delete_message(callback.from_user.id, callback.message.message_id)
    await bot.send_message(callback.from_user.id, 'Выберите пункт меню:', \
                           reply_markup=client_keyboard.client_buttons_menu_first_level)


async def work_mode(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Пн-Пт с 8.00 до 20.00, Сб с 8.00 до 14.00')


async def location(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Республика Татарстан, г.Набережные Челны, '
                                                        'ул Казанский проспект, 226а 2 этаж')


async def contact(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, '+7 (8552) 25‒85‒75 +7‒960‒045‒85‒75 +7‒917‒292‒95‒55')

    # keyboard_markup = types.InlineKeyboardMarkup()
    # website_button = types.InlineKeyboardButton('Перейти на сайт', url='https://filter2000.ru/')
    # keyboard_markup.add(website_button)
    #
    # await bot.send_message(callback_query.from_user.id, 'Посетите наш сайт:', reply_markup=keyboard_markup)


def register_handler_client(dp: Dispatcher):
    dp.register_message_handler(start_command, commands='start')
    dp.register_callback_query_handler(show_price_list, lambda c: c.data == 'show_price_list')
    dp.register_callback_query_handler(show_air_filter, text='client_air_filter')
    dp.register_callback_query_handler(show_fuel_filter, text='client_fuel_filter')
    dp.register_callback_query_handler(show_oil_filter, text='client_oil_filter')
    dp.register_callback_query_handler(command_back, text='client_button_back')
    dp.register_callback_query_handler(work_mode, lambda c: c.data == 'worker_mode')
    dp.register_callback_query_handler(location, lambda c: c.data == 'location')
    dp.register_callback_query_handler(contact, lambda c: c.data == 'contacts')
