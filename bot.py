import requests
import json
import os
import uuid
import cv2
import random 
global machineID
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputFile

import profile

bot = Bot(token='5893920925:AAHCU_FZNN5S7BwtPMVExy9bAE6Qr5ej0uQ')
dp = Dispatcher(bot)

menu_btn = InlineKeyboardButton('Меню 🗺️', callback_data='menu')
menu_btns = InlineKeyboardMarkup()
menu_btns.add(menu_btn)

goods = {
    "Bear": "500",
    "Paper": "100",
    "Hoodie": "1000",
    "Cap": "700",
}

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):

    reg_btn = InlineKeyboardButton('Зарегистрироваться 🍃', callback_data='reg')

    start_btns = InlineKeyboardMarkup()
    start_btns.add(reg_btn)

    await message.answer("Привет!✌️ \n 🏔️ Я - ЭкоБот, я помогаю делать природу чище! ", reply_markup=start_btns)

@dp.message_handler()
async def echo(message: types.Message):
    if message.text.lower() == 'привет':
        await message.answer('Привееет ✌️')

@dp.callback_query_handler(lambda c: c.data == 'menu')
async def process_callback_menu(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    collect_btn = InlineKeyboardButton('Приемка мусора 🚮', callback_data='collect')
    catalog_btn = InlineKeyboardButton('Каталог 📖', callback_data='catalog')
    profile_btn = InlineKeyboardButton('Профиль 👀', callback_data='profile')

    menu_kb = InlineKeyboardMarkup()

    menu_kb.add(collect_btn)
    menu_kb.add(catalog_btn)
    menu_kb.add(profile_btn)

    await bot.send_message(callback_query.from_user.id, 'Вы находитесь в меню 🗺️ \n Здесь вы можете: \n 🚮 Сдать мусор  \n 📖 Заглянуть в каталог товаров \n 👀 Посмотреть профиль \n ', reply_markup=menu_kb)

@dp.callback_query_handler(lambda c: c.data == 'profile')
async def process_callback_menu(callback_query: types.CallbackQuery):

    data = requests.get(f'http://127.0.0.1:5000/api?target=account&id={callback_query.from_user.id}')
    user = json.loads(data.text)[0]
    username = user[0]
    coins = user[1]
    garbage = user[2]

    goods = requests.get(f'http://127.0.0.1:5000/api?target=goods&id={callback_query.from_user.id}')
    goods = json.loads(goods.text)[0]
    user_goods = []

    for good in goods:
        if int(good) != int(callback_query.from_user.id):
            user_goods.append(good)

    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f'👀 Ваш профиль: \n Имя: {username} \n ЭкоКоинов: {coins} \n Сдано мусора: {garbage} \n Ваши товары: \n {user_goods[0]} плюшевых медведей \n {user_goods[1]} пачек бумаги \n {user_goods[2]} худи \n {user_goods[3]} крутых кепок', reply_markup=menu_btns)

# @dp.callback_query_handler(lambda c: c.data == 'profile')
# async def go_pr(cq):
#     await profile.process_callback_profile(cq, callback_query.from_user.id)

@dp.callback_query_handler(lambda c: c.data == 'reg')
async def process_callback_menu(callback_query: types.CallbackQuery):

    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Введите свой номер телефона (начинается на 7 или 8, без остальных знаков, только цифры)')

######

@dp.callback_query_handler(lambda c: c.data == 'catalog')
async def process_callback_menu(callback_query: types.CallbackQuery):

    bear_btn = InlineKeyboardButton('Плюшевый мишка 🐻', callback_data='seeBear')
    paper_btn = InlineKeyboardButton('Переработанная бумага 📜', callback_data='seePaper')
    hoodie_btn = InlineKeyboardButton('Эко-худи 🧑‍💻', callback_data='seeHoodie')
    cap_btn = InlineKeyboardButton('Кепка "Спаси природу! 🧢 "', callback_data='seeCap')

    catalog_btns = InlineKeyboardMarkup()

    catalog_btns.add(bear_btn)
    catalog_btns.add(paper_btn)
    catalog_btns.add(hoodie_btn)
    catalog_btns.add(cap_btn)
    catalog_btns.add(menu_btn)

    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, '📖 Каталог \n Здесь вы можете купить наши эко-товары, произведенные из переработанных материалов ♻️', reply_markup=catalog_btns)

# товары

@dp.callback_query_handler(lambda c: 'see' in c.data)
async def process_callback_menu(callback_query: types.CallbackQuery):

    good = callback_query.data.replace('see', '')

    buy_btn = InlineKeyboardButton('Купить за ' + goods[good] + ' ЭкоБаллов ❤️', callback_data='buy' + good)
    catalog_btn = InlineKeyboardButton('Каталог 📖', callback_data='catalog')

    buy_btns = InlineKeyboardMarkup()
    buy_btns.add(buy_btn)
    buy_btns.add(catalog_btn)
    buy_btns.add(menu_btn)

    await bot.answer_callback_query(callback_query.id)

    if good == 'Bear':
        await bot.send_photo(callback_query.from_user.id,
        photo=InputFile("imgs/bear.jpeg"),
        caption='Красивый плюшевый мишка из переработанных материалов 🐻',
        reply_markup=buy_btns)
    elif good == 'Paper':
        await bot.send_photo(callback_query.from_user.id,
        photo=InputFile("imgs/paper.jpeg"),
        caption='Переработанная бумага 📖',
        reply_markup=buy_btns)
    elif good == 'Hoodie':
        await bot.send_photo(callback_query.from_user.id,
        photo=InputFile("imgs/hoodie.jpeg"),
        caption='Красивое (или красивый) худи, который вам точно подойдет) ✌️',
        reply_markup=buy_btns)
    elif good == 'Cap':
        await bot.send_photo(callback_query.from_user.id,
        photo=InputFile("imgs/cap.jpeg"),
        caption='Кепка с логотипом нашей компании 🧢',
        reply_markup=buy_btns)


@dp.callback_query_handler(lambda c: 'buy' in c.data)
async def process_callback_menu(callback_query: types.CallbackQuery):

    good = callback_query.data.replace('buy', '')

    await bot.answer_callback_query(callback_query.id)

    if good == 'Bear':
        res = requests.get(f'http://127.0.0.1:5000/api?target=buy&good={good.lower()}&id={callback_query.from_user.id}&cost={goods[good]}')
        if res.text == 'ok':
            await bot.send_message(callback_query.from_user.id, 'Вы успешно купили медвежонка, спасибо ❤️', reply_markup=menu_btns)
        else:
            await bot.send_message(callback_query.from_user.id, 'У вас недостаточно средств 😥', reply_markup=menu_btns)

    elif good == 'Paper':
        res = requests.get(f'http://127.0.0.1:5000/api?target=buy&good={good.lower()}&id={callback_query.from_user.id}&cost={goods[good]}')
        if res.text == 'ok':
            await bot.send_message(callback_query.from_user.id, 'Вы успешно купили бумагу, спасибо ❤️', reply_markup=menu_btns)
        else:
            await bot.send_message(callback_query.from_user.id, 'У вас недостаточно средств 😥', reply_markup=menu_btns)

    elif good == 'Hoodie':
        res = requests.get(f'http://127.0.0.1:5000/api?target=buy&good={good.lower()}&id={callback_query.from_user.id}&cost={goods[good]}')
        if res.text == 'ok':
            await bot.send_message(callback_query.from_user.id, 'Вы успешно купили худи, спасибо ❤️', reply_markup=menu_btns)
        else:
            await bot.send_message(callback_query.from_user.id, 'У вас недостаточно средств 😥', reply_markup=menu_btns)

    elif good == 'Cap':
        res = requests.get(f'http://127.0.0.1:5000/api?target=buy&good={good.lower()}&id={callback_query.from_user.id}&cost={goods[good]}')
        if res.text == 'ok':
            await bot.send_message(callback_query.from_user.id, 'Вы успешно купили кепку, спасибо ❤️', reply_markup=menu_btns)
        else:
            await bot.send_message(callback_query.from_user.id, 'У вас недостаточно средств 😥', reply_markup=menu_btns)

@dp.callback_query_handler(lambda c: c.data == 'collect')
async def process_callback_menu(callback_query: types.CallbackQuery):

    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Ты можешь сдать свой мусор на переработку! Просто отсканируй QR-код автомата для приемки вторсырья, пришли фото с ним в чат и следуй инструкциям!')

@dp.message_handler(content_types=['photo'])
async def handle_docs_photo(message: types.Message):

    paper_btn = InlineKeyboardButton('Бумага 📜', callback_data='collect_paper')
    glass_btn = InlineKeyboardButton('Стекло 🔍', callback_data='collect_glass')
    plastic_btn = InlineKeyboardButton('Пластик ♻', callback_data='collect_plastic')

    collect_btns = InlineKeyboardMarkup()
    collect_btns.add(paper_btn)
    collect_btns.add(glass_btn)
    collect_btns.add(plastic_btn)

    id = str(uuid.uuid4())
    await message.photo[-1].download('qr/' + id + '.png')
    img = cv2.imread('qr/' + id + '.png')
    det = cv2.QRCodeDetector()
    val, pts, st_code = det.detectAndDecode(img)
    global machineID
    machineID = val
    if len(val) > 0:
        automate = requests.get(f'http://127.0.0.1:5000/api?target=automate&auto_id={val}')
        automate = json.loads(automate.text)[0]
        await message.answer(f"ID автомата: {val}\nВсего сдано мусора: {automate[0]} \n Осталось места: {100 - int(automate[1])}", reply_markup=collect_btns)
        os.remove('qr/' + id + '.png')
    else:
        await message.answer('QR-код не обнаружен, попробуйте снова')
        os.remove('qr/' + id + '.png')

@dp.callback_query_handler(lambda c: 'collect' in c.data)
async def process_callback_menu(callback_query: types.CallbackQuery):

    trash = callback_query.data.replace('collect_', '')

    put_btns = InlineKeyboardMarkup()
    put_btns.add(InlineKeyboardButton('Я положил 👍', callback_data=f'put_{trash}'))

    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Положи в автомат свой мусор ♻️', reply_markup=put_btns)

@dp.callback_query_handler(lambda c: 'put' in c.data)
async def process_callback_menu(callback_query: types.CallbackQuery):

    putted_trash = callback_query.data.replace('put_', '')
    mass = random.randint(1, 10)
    requests.get(f'http://127.0.0.1:5000/api?trash={putted_trash}&mass={mass}&mach_id={machineID}&id={callback_query.from_user.id}')

    await bot.answer_callback_query(callback_query.id)

    if putted_trash == 'paper':
        await bot.send_message(callback_query.from_user.id, f'Спасибо за помощь природе! ❤️ Вы успешно сдали {mass} кг бумаги', reply_markup=menu_btns)
    elif putted_trash == 'glass':
        await bot.send_message(callback_query.from_user.id, f'Спасибо за помощь природе! ❤️ Вы успешно сдали {mass} кг стекла', reply_markup=menu_btns)
    elif putted_trash == 'plastic':
        await bot.send_message(callback_query.from_user.id, f'Спасибо за помощь природе! ❤️ Вы успешно сдали {mass} кг пластика', reply_markup=menu_btns)

executor.start_polling(dp, skip_updates=True)
# 