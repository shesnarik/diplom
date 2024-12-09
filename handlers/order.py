import logging
from aiogram import types
from database import get_session
from models import User, Order
from datetime import datetime

logging.basicConfig(level=logging.INFO)


async def place_order(message: types.Message):
    item_number = int(message.text.strip())

    session = get_session()

    try:
        user = session.query(User).filter_by(phone_number=message.from_user.phone_number).first()

        items = {1: "Хлеб", 2: "Булочки", 3: "Пироги"}

        if item_number in items:
            order = Order(user_id=user.id, item_name=items[item_number], delivery_time=datetime.now(), status='pending')
            session.add(order)
            session.commit()
            await message.answer(f"Ваш заказ на {items[item_number]} оформлен!")
        else:
            await message.answer("Неверный номер товара.")
    except Exception as e:
        await message.answer("Произошла ошибка при оформлении заказа. Попробуйте еще раз.")
        print(e)
    finally:
        session.close()


async def repeat_last_order(message: types.Message):
    session = get_session()

    try:
        user = session.query(User).filter_by(phone_number=message.from_user.phone_number).first()

        if not user:
            await message.answer("Вы не зарегистрированы.")
            return

        last_order = session.query(Order).filter_by(user_id=user.id).order_by(Order.id.desc()).first()

        if last_order and last_order.status == 'completed':
            new_order = Order(user_id=user.id, item_name=last_order.item_name, delivery_time=datetime.now(),
                              status='pending')
            session.add(new_order)
            session.commit()
            await message.answer(f"Ваш заказ на {last_order.item_name} повторен!")
        else:
            await message.answer("У вас нет завершенных заказов для повторения.")
    except Exception as e:
        await message.answer("Произошла ошибка при повторении заказа. Попробуйте еще раз.")
        print(e)
    finally:
        session.close()