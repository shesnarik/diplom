import logging
from aiogram import Bot, Dispatcher, executor, types
from config import API_TOKEN, ADMIN_ID

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Импортируем обработчики команд из разных модулей.
from handlers.user.start import start_command, register_user
from handlers.user.menu import menu_command
from handlers.user.order import place_order, repeat_last_order
from handlers.user.history import show_history

from handlers.admin.admin_panel import admin_panel_command
from handlers.admin.orders import view_orders, complete_order

# Регистрация пользовательских команд.
dp.register_message_handler(start_command, commands=['start'])
dp.register_message_handler(register_user, lambda message: message.text.startswith('+'))
dp.register_message_handler(menu_command, commands=['menu'])
dp.register_message_handler(place_order, lambda message: message.text.isdigit())
dp.register_message_handler(repeat_last_order, lambda message: message.text == "Повторить последний заказ")
dp.register_message_handler(show_history, lambda message: message.text == "История заказов")

# Регистрация админских команд.
dp.register_message_handler(admin_panel_command, commands=['admin'], chat_id=ADMIN_ID)
dp.register_message_handler(view_orders, lambda message: message.text == "Посмотреть заказы", chat_id=ADMIN_ID)
dp.register_message_handler(complete_order,
                            lambda message: "Завершить заказ" in message.text and len(message.text.split()) > 1,
                            chat_id=ADMIN_ID)

if __name__ == '__main__':
    from database import get_engine

    engine = get_engine()

    executor.start_polling(dp, skip_updates=True)