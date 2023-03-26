from create_bot import bot, dp
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import types
from buttons import admin_keyboard
from data_base import sqlite_db
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.dispatcher.filters import Text

ID = None



class FSM_admin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


async def comand_start(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'Что желаете, господин?', \
                           reply_markup=admin_keyboard.admin_buttons_menu_first_level)
    await message.delete()


async def command_add_goods(callback: types.callback_query):
    if callback.from_user.id == ID:
        admin_keyboard.choice_action = 'add_goods'
        await bot.delete_message(callback.from_user.id, callback.message.message_id)
        await bot.send_message(callback.from_user.id, 'Что желаете добавить, господин?', \
                               reply_markup=admin_keyboard.admin_buttons_menu_second_level)



async def command_del_goods(callback: types.callback_query):
    if callback.from_user.id == ID:
        admin_keyboard.choice_action  = 'del_goods'
        await bot.delete_message(callback.from_user.id, callback.message.message_id)
        await bot.send_message(callback.from_user.id, 'Что желаете удалить, господин?', \
                               reply_markup=admin_keyboard.admin_buttons_menu_second_level)



# async def process_filter_choice(callback_query: CallbackQuery, callback_data: dict):
#     if callback_query.from_user.id == ID:
#         filter_type = ''
#
#
#         if filter_type == 'air filter':
#             sqlite_db.price_list = 'air_filter'
#             sqlite_db.sql_start()
#
#             # if commands == 'load_data':
#             #     await cm_start(callback_query)
#             # elif action == 'delete_data':
#             #     await command_del_goods('air_filter.csv')
#         # elif filter_type == 'oil filter':
#         #     if action == 'load_data':
#         #         command_add_goods('oil_filter.csv')
#         #     elif action == 'delete_data':
#         #         command_del_goods('oil_filter.csv')
#         # elif filter_type == 'fuel filter':
#         #     if action == 'load_data':
#         #         command_add_goods('fuel_filter.csv')
#         #     elif action == 'delete_data':
#         #         command_del_goods('fuel_filter.csv')
#         # elif filter_type == 'Add goods':  # добавляем условие для опции "Добавить товар"
#         #     if action == 'load_goods':
#         #         command_add_goods()
#         else:
#             print('Invalid choice!')
#
#         await bot.answer_callback_query(callback_query.id)

async def command_air_filter(message: types.Message):
    if message.from_user.id == ID:
        sqlite_db.price_list = 'air_filter'
        sqlite_db.sql_start()
        if admin_keyboard.choice_action  == 'add_goods':
            await cm_start(message)
        elif admin_keyboard.choice_action  == 'del_goods':
            await delete_goods(message)
        # await message.answer('Выбран воздушный фильтр')


async def command_fuel_filter(message: types.Message):
    if message.from_user.id == ID:
        sqlite_db.price_list = 'fuel_filter'
        sqlite_db.sql_start()
        if admin_keyboard.choice_action == 'add_goods':
            await cm_start(message)
        elif admin_keyboard.choice_action == 'del_goods':
            await delete_goods(message)
        # await callback.answer('Выбран топливный фильтр')


async def command_oil_filter(message: types.Message):
    if message.from_user.id == ID:
        sqlite_db.price_list = 'oil_filter'
        sqlite_db.sql_start()
        if admin_keyboard.choice_action == 'add_goods':
            await cm_start(message)
        elif admin_keyboard.choice_action == 'del_goods':
            await delete_goods(message)
        # await callback.answer('Выбран масляный фильтр')


async def command_back(callback: types.callback_query):
    if callback.from_user.id == ID:
        await bot.delete_message(callback.from_user.id, callback.message.message_id)
        await bot.send_message(callback.from_user.id, 'Что желаете, господин?', \
                               reply_markup=admin_keyboard.admin_buttons_menu_first_level)


"""Запускается машина состояний"""


async def cm_start(message: types.Message):
    if message.from_user.id == ID:
        await message.answer('Загрузите фото')
        await FSM_admin.photo.set()


"""Загружаем фото товара"""


async def load_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSM_admin.next()
        await message.reply('Введите название')


"""Записываем название товара"""


async def load_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSM_admin.next()
        await message.reply('Введите описание')


"""Записываем описание товара"""


async def load_description(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description'] = message.text
        await FSM_admin.next()
        await message.reply('Введите цену')


"""Записываем цену товара"""


async def load_price(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['price'] = f'{message.text}₽'
        await sqlite_db.sql_add_command(state)
        await state.finish()
        await cm_start(message)


"""Удаление товара"""


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_callback_run(callback_query: types.CallbackQuery):
    await sqlite_db.sql_delete_command(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del ", "")} удалена.', show_alert=True)


async def delete_goods(message: types.Message):
    if message.from_user.id == ID:
        read = await sqlite_db.sql_read2()
        for ret in read:
            await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}'
                                                               f'\nОписание: {ret[2]}'
                                                               f'\nЦена: {ret[-1]}')
            await bot.send_message(message.from_user.id, text='^^^', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(f'Удалить {ret[1]}', callback_data=f'del {ret[1]}')))


"""Тут надо доделать выбор двух кнопок"""


# @dp.callback_query_handler(Text(startswith='price_list'))
# async def test_command(callback: types.callback_query):
#     await callback.answer('Выбал прайслист')

def register_handler_admin(dp: Dispatcher):
    dp.register_message_handler(comand_start, commands='moderator', is_chat_admin=True)
    dp.register_callback_query_handler(command_add_goods, lambda x: x.data == 'load_goods')
    dp.register_callback_query_handler(command_del_goods, lambda x: x.data == 'delete_goods')
    # dp.register_callback_query_handler(process_filter_choice, text='choice_filter')





    dp.register_callback_query_handler(command_air_filter, text='air_filter')
    dp.register_callback_query_handler(command_fuel_filter, text='fuel_filter')
    dp.register_callback_query_handler(command_oil_filter, text='oil_filter')
    dp.register_callback_query_handler(command_back, text='button_back')
    dp.register_message_handler(cm_start, commands='load_goods', state=None)
    dp.register_message_handler(load_photo, content_types='photo', state=FSM_admin.photo)
    dp.register_message_handler(load_name, state=FSM_admin.name)
    dp.register_message_handler(load_description, state=FSM_admin.description)
    dp.register_message_handler(load_price, state=FSM_admin.price)
