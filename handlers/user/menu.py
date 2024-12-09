from aiogram import types
from keyboards.user_keyboard import get_user_keyboard

async def menu_command(message: types.Message):
    menu_items = "1. Хлеб\n2. Булочки\n3. Пироги"
    await message.answer(f"Меню:\n{menu_items}\nВведите номер товара для заказа.", reply_markup=get_user_keyboard())