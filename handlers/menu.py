from aiogram import types

async def menu_command(message: types.Message):
    menu_items = "1. Хлеб\n2. Булочки\n3. Пироги"
    await message.answer(f"Меню:\n{menu_items}\nВведите номер товара для заказа.")