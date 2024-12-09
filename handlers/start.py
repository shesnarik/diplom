from aiogram import types
from database import get_session
from models import User


async def start_command(message: types.Message):
    await message.answer("Добро пожаловать в пекарню! Пожалуйста, введите ваш номер телефона для авторизации.")


async def register_user(message: types.Message):
    phone_number = message.text.strip()

    session = get_session()

    try:
        user = session.query(User).filter_by(phone_number=phone_number).first()

        if not user:
            user = User(phone_number=phone_number)
            session.add(user)
            session.commit()
            await message.answer("Вы успешно зарегистрированы!")
        else:
            await message.answer("Вы уже зарегистрированы!")
    except Exception as e:
        await message.answer("Произошла ошибка при регистрации. Попробуйте еще раз.")
        print(e)
    finally:
        session.close()