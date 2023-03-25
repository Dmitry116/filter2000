from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import types
from create_bot import dp


"""first level keyboard"""
button_load_goods = InlineKeyboardButton(text='Добавить товар', callback_data='load_goods')
button_delete_goods = InlineKeyboardButton(text='Удалить товар', callback_data='delete_goods')
admin_buttons_menu_first_level = InlineKeyboardMarkup(row_width=1).add(button_load_goods, button_delete_goods)


"""second level keyboard and button to previous menu"""
air_filter = InlineKeyboardButton(text='Воздушные фильтра', callback_data='air_filter')
fuel_filter = InlineKeyboardButton(text='Топливные фильтра', callback_data='fuel_filter')
oil_filter = InlineKeyboardButton(text='Масляные фильтра', callback_data='oil_filter')
button_back = InlineKeyboardButton(text='Назад', callback_data='button_back')

admin_buttons_menu_second_level = InlineKeyboardMarkup(row_width=1).add(air_filter, fuel_filter, oil_filter, button_back)


