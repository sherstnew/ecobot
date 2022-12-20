import requests
import json
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputFile

async def process_callback_profile(callback_query, phone):

    data = requests.get(f'http://127.0.0.1:5000/api?target=account&id={phone}')
    user = json.loads(data.text)[0]
    username = user[0]
    coins = user[1]
    garbage = user[2]

    goods = requests.get(f'http://127.0.0.1:5000/api?target=goods&id={phone}')
    goods = json.loads(goods.text)[0]
    user_goods = []

    for good in goods:
        if int(good) != int(phone):
            user_goods.append(good)

    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f'👀 Ваш профиль: \n Имя: {username} \n ЭкоКоинов: {coins} \n Сдано мусора: {garbage} \n Ваши товары: \n {user_goods[0]} плюшевых медведей \n {user_goods[1]} пачек бумаги \n {user_goods[2]} худи \n {user_goods[3]} крутых кепок', reply_markup=menu_btns)