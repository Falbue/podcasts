from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from telebot import types
import random
from scripts import *
import json

URL = "https://podcast.ru/"

def create_buttons(data, prefix=URL, web_app=False):
    buttons = []
    for text, callback in data.items():
        if not isinstance(text, str):
            text = str(text)
        if callback == "":
            callback = text
        if web_app == False:
            button = types.InlineKeyboardButton(text, callback_data=f'{prefix}:{callback}')
        else:
            button = types.InlineKeyboardButton(text, web_app=types.WebAppInfo(url=f'{prefix}{callback}/e'))
        buttons.append(button)
    return buttons

def main(call):
    text = """Добро пожаловать в мир подкастов 🎙️

🔎 *Хотите* узнать что-то новое, посмеяться или найти вдохновение? У нас есть подкасты на любой вкус

🔊 *Слушай* в дороге, на прогулке или дома — запускайте любимые выпуски одним нажатием

🌐 *Нашли* что-то крутое? Расскажите друзьям или сохраните в избранное

*Никаких лишних движений* — только вы, ваши наушники и океан историй, знаний и эмоций"""
    keyboard = InlineKeyboardMarkup(row_width=2)
    btn_save = InlineKeyboardButton("⭐️ Избранное", callback_data='save')
    # btn_random = InlineKeyboardButton("Случайный", callback_data='random')
    keyboard.add(btn_save)
    text = markdown(text)
    return text, keyboard

def help(call):
    text = """*Как сохранить подкаст в избранное?*

Пришлите ссылку на подкаст из приложения и бот сам сохранит его в избранном\!
"""
    keyboard = InlineKeyboardMarkup(row_width=2)
    btn_return = InlineKeyboardButton("⬅️ Назад", callback_data='return:main')
    keyboard.add(btn_return)
    return text, keyboard

def save(call):
    user_id = call.message.chat.id
    podcasts = SQL_request("SELECT podcasts FROM users WHERE id = ?", (user_id,))
    podcasts = json.loads(podcasts[0])
    keyboard = InlineKeyboardMarkup(row_width=2)
    btn_return = InlineKeyboardButton("⬅️ Назад", callback_data='return:main')
    if not podcasts:
        text = "У Вас нет сохранённых подкастов\n\nКак добававить в избранное? /help"
    else:
        text = f"*Добавлено подкастов\:* {len(podcasts)}\n\nВыберите подкаст, который хотите послушать:"
        buttons = create_buttons(podcasts, "open_podcast")
        keyboard.add(*buttons)
    keyboard.add(btn_return)
    text = markdown(text)
    return text, keyboard

def random(call):
    text = "Случайные подкасты в разработке!"
    keyboard = InlineKeyboardMarkup(row_width=2)
    btn_return = InlineKeyboardButton("⬅️ Назад", callback_data='return:main')
    keyboard.add(btn_return)
    text = markdown(text)
    return text, keyboard

def save_podcast():
    keyboard = InlineKeyboardMarkup(row_width=2)
    btn_return = InlineKeyboardButton("⬅️ Назад", callback_data='return:main')
    keyboard.add(btn_return)
    return keyboard

def open_podcast(podcast_id):
    text = f"[Открыть в бразузере ›]({URL}{podcast_id}/info)"
    keyboard = InlineKeyboardMarkup(row_width=2)
    btn_open = types.InlineKeyboardButton("🎧 Слушать", web_app=types.WebAppInfo(url=f'{URL}{podcast_id}/e'))
    # btn_share = InlineKeyboardButton(text="➦ Поделится", switch_inline_query="") 
    btn_delete = InlineKeyboardButton("🚫 Удалить", callback_data=f'delete:{podcast_id}')
    btn_return = InlineKeyboardButton("⬅️ Назад", callback_data='return:save')
    keyboard.add(btn_open,btn_delete, btn_return)
    return text, keyboard