import sqlite3 as sq
from create_bot import bot

price_list = ''

def sql_start():
    global base, cur
    base = sq.connect('filter2000.db')
    cur = base.cursor()
    if base:
        print('Data base connected Ok.')
        base.execute(f'CREATE TABLE IF NOT EXISTS {price_list}(img TEXT, name TEXT PRIMARY KEY, '
                     f'description TEXT, price TEXT)')
        base.commit()


"""add goods in sql base"""
async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute(f'INSERT INTO {price_list} VALUES (?, ?, ?, ?)', tuple(data.values()))
        base.commit()


async def sql_read(message):
    for goods in cur.execute(f'SELECT * FROM {price_list}').fetchall():
        await bot.send_photo(message.from_user.id, goods[0], f'{goods[1]}'
                                                             f'\nОписание: {goods[2]}'
                                                             f'\nЦена: {goods[-1]}')
async def sql_read2():
    return cur.execute(f'SELECT * FROM {price_list}').fetchall()

"""delete goods in sql base"""

async def sql_delete_command(data):
    cur.execute(f'DELETE FROM {price_list} WHERE name == ?', (data,))
    base.commit()