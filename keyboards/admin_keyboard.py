from aiogram import types

def get_admin_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("Посмотреть заказы"))
    keyboard.add(types.KeyboardButton("Завершить заказ"))
    return keyboard