import logging
from aiogram import types
from database import get_session
from models import User, Order

logging.basicConfig(level=logging.INFO)


async def cancel_order(message: types.Message):
    session = get_session()

    try:
        user = session.query(User).filter_by(phone_number=message.from_user.phone_number).first()

        if not user:
            await message.answer("Вы не зарегистрированы.")
            return

        orders = session.query(Order).filter_by(user_id=user.id, status='pending').all()

        if not orders:
            await message.answer("У вас нет активных заказов.")
            return

        order_list = "\n".join([f"{order.id}. {order.item_name}" for order in orders])
        await message.answer(f"Ваши активные заказы:\n{order_list}\nВведите номер заказа для отмены.")

    except Exception as e:
        await message.answer("Произошла ошибка при получении активных заказов. Попробуйте еще раз.")
        print(e)

    finally:
        session.close()


async def confirm_cancel_order(message: types.Message):
    order_id = int(message.text.strip())

    session = get_session()

    try:
        order = session.query(Order).filter_by(id=order_id, status='pending').first()

        if order:
            order.status = 'cancelled'
            session.commit()
            await message.answer(f"Заказ {order.item_name} отменен.")
        else:
            await message.answer("Заказ не найден или уже отменен.")

    except Exception as e:
        await message.answer("Произошла ошибка при отмене заказа. Попробуйте еще раз.")
        print(e)

    finally:
        session.close()