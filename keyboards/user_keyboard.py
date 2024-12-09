from aiogram import types

def get_user_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("Меню"))
    keyboard.add(types.KeyboardButton("История заказов"))
    keyboard.add(types.KeyboardButton("Повторить последний заказ"))
    return keyboard