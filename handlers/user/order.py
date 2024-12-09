import logging
from aiogram import types
from database import get_session
from models import User, Order
from datetime import datetime
from keyboards.user_keyboard import get_user_keyboard

logging.basicConfig(level=logging.INFO)


async def place_order(message: types.Message):
    # Проверяем, что сообщение содержит только цифры
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введите номер товара.", reply_markup=get_user_keyboard())
        return

    item_number = int(message.text.strip())

    session = get_session()

    try:
        user = session.query(User).filter_by(phone_number=message.from_user.phone_number).first()

        items = {1: "Хлеб", 2: "Булочки", 3: "Пироги"}

        if item_number in items:
            order = Order(user_id=user.id, item_name=items[item_number], delivery_time=datetime.now(), status='pending')
            session.add(order)
            session.commit()
            await message.answer(f"Ваш заказ на {items[item_number]} оформлен!", reply_markup=get_user_keyboard())
        else:
            await message.answer("Неверный номер товара.", reply_markup=get_user_keyboard())
    except Exception as e:
        await message.answer("Произошла ошибка при оформлении заказа. Попробуйте еще раз.")
        logging.error(f"Ошибка при оформлении заказа: {e}")
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
            await message.answer(f"Ваш заказ на {last_order.item_name} повторен!", reply_markup=get_user_keyboard())
        else:
            await message.answer("У вас нет завершенных заказов для повторения.", reply_markup=get_user_keyboard())
    except Exception as e:
        await message.answer("Произошла ошибка при повторении заказа. Попробуйте еще раз.")
        logging.error(f"Ошибка при повторении заказа: {e}")
    finally:
        session.close()