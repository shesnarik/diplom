from aiogram import types
from database import get_session
from models import User, Order
from keyboards.user_keyboard import get_user_keyboard


async def show_history(message: types.Message):
    session = get_session()

    try:
        user = session.query(User).filter_by(phone_number=message.from_user.phone_number).first()

        if not user:
            await message.answer("Вы не зарегистрированы.")
            return

        orders = session.query(Order).filter_by(user_id=user.id).all()

        if not orders:
            await message.answer("У вас нет заказов.", reply_markup=get_user_keyboard())
            return

        history_list = "\n".join([f"{order.id}. {order.item_name} - {order.status}" for order in orders])
        await message.answer(f"Ваша история заказов:\n{history_list}", reply_markup=get_user_keyboard())

    except Exception as e:
        await message.answer("Произошла ошибка при получении истории заказов. Попробуйте еще раз.")

    finally:
        session.close()