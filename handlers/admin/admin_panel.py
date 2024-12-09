from aiogram import types
from keyboards.admin_keyboard import get_admin_keyboard

async def admin_panel_command(message: types.Message):
    await message.answer("Добро пожаловать в админ-панель! Используйте команды для управления пользователями и заказами.", reply_markup=get_admin_keyboard())