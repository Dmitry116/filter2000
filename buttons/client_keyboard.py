from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


button_show_price_list = InlineKeyboardButton(text='Посмотреть прайс лист', callback_data='show_price_list')
button_worker_mode = InlineKeyboardButton(text='Режим работы', callback_data='worker_mode')
button_location = InlineKeyboardButton(text='Расположение магазина', callback_data='location')
button_contact = InlineKeyboardButton(text='Контакты', callback_data='contacts')

button_client_contact = InlineKeyboardButton(text='Поделиться номером', callback_data='my_contact')
button_client_location = InlineKeyboardButton(text='Мое местоположение', callback_data='client_location')

client_buttons_menu_first_level = InlineKeyboardMarkup(row_width=1).add(button_show_price_list, button_worker_mode,\
                                                        button_location, button_contact, button_client_contact,\
                                                        button_client_location)


client_air_filter = InlineKeyboardButton(text='Воздушные фильтра', callback_data='client_air_filter')
client_fuel_filter = InlineKeyboardButton(text='Топливные фильтра', callback_data='client_fuel_filter')
client_oil_filter = InlineKeyboardButton(text='Масляные фильтра', callback_data='client_oil_filter')
client_button_back = InlineKeyboardButton(text='Назад', callback_data='client_button_back')

client_buttons_menu_second_level = InlineKeyboardMarkup(row_width=1).add(client_air_filter, client_fuel_filter,\
                                                                         client_oil_filter, client_button_back)