import logging
from aiogram import Bot, Dispatcher, executor
from config import API_TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Импортируем обработчики команд из разных модулей.
from handlers.start import start_command, register_user
from handlers.menu import menu_command
from handlers.order import place_order, repeat_last_order
from handlers.cancel import cancel_order, confirm_cancel_order
from handlers.history import order_history

# Регистрация обработчиков команд.
dp.register_message_handler(start_command, commands=['start'])
dp.register_message_handler(register_user, lambda message: message.text.startswith('+'))
dp.register_message_handler(menu_command, commands=['menu'])
dp.register_message_handler(place_order, lambda message: message.text.isdigit())
dp.register_message_handler(repeat_last_order, commands=['repeat'])
dp.register_message_handler(cancel_order, commands=['cancel'])
dp.register_message_handler(confirm_cancel_order, lambda message: message.text.isdigit())
dp.register_message_handler(order_history, commands=['history'])

if __name__ == '__main__':
    from database import get_engine

    engine = get_engine()

    executor.start_polling(dp, skip_updates=True)