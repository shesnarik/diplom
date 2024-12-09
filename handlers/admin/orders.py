import logging
from aiogram import types
from database import get_session
from models import Order

logging.basicConfig(level=logging.INFO)


async def view_orders(message: types.Message):
    session = get_session()

    try:
        orders = session.query(Order).all()

        if not orders:
            await message.answer("Нет активных заказов.")
            return

        orders_list = "\n".join(
            [f"ID: {order.id}, Пользователь ID: {order.user_id}, Товар: {order.item_name}, Статус: {order.status}" for
             order in orders])
        await message.answer(f"Все заказы:\n{orders_list}")

    except Exception as e:
        await message.answer("Произошла ошибка при получении заказов. Попробуйте еще раз.")
        print(e)

    finally:
        session.close()


async def complete_order(message: types.Message):
    order_id_str = message.text.strip().split()[-1]

    try:
        order_id = int(order_id_str)

        session = get_session()

        order = session.query(Order).filter_by(id=order_id).first()

        if order and order.status == 'pending':
            order.status = 'completed'
            session.commit()
            await message.answer(f"Заказ ID {order_id} завершен!")
        else:
            await message.answer(f"Заказ ID {order_id} не найден или уже завершен.")

    except ValueError:
        await message.answer("Пожалуйста, введите корректный ID заказа.")

    except Exception as e:
        await message.answer("Произошла ошибка при завершении заказа. Попробуйте еще раз.")
        print(e)