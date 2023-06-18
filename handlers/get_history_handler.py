from aiogram import Router, F
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import Message
import utils.keyboard as nav
from datetime import date, timedelta
from db.base import User, HealthDiary
from sqlalchemy import select

router = Router()


@router.message(
    F.text == 'За Неделю',
    F.text == 'За Месяц'
)
async def get_history_handler(message: Message, session: AsyncSession):
    if message.text == 'За неделю':
        _timedelta = timedelta(days=7)
    else:
        _timedelta = timedelta(days=30)

    end_date = date.today()
    start_date = end_date - _timedelta

    user = await session.execute(
        select(User.telegram_id)
        .where(User.telegram_id == message.from_user.id)
    )

    user_mode = await session.execute(
        select(
            # User.telegram_id,
            User.only_headaches,
            User.only_blood,
            User.both_mode
        ).where(User.telegram_id == user.scalar()))

    user_history = await session.execute(
        select(
            # HealthDiary.telegram_id,
            HealthDiary.date,
            HealthDiary.headaches,
            HealthDiary.blood_pressure,
            HealthDiary.drugs
        ).where(HealthDiary.telegram_id == user.scalar())
    )

    user_mode_result = user_mode.scalar()
    user_history_result = user_history.scalar()
    message_result = ''

    if user_mode_result.only_headaches is True:
        for result in user_history_result:
            date_str = result.date.strftime('%d.%m.%Y')
            headaches_str = str(result.only_headaches)
            drugs_str = result.drugs
            message_result += f"Дата: {date_str}, Головная боль: {headaches_str}, Лекарства: {drugs_str} \n"
    elif user_mode_result.blood is True:
        for result in user_history_result:
            date_str = result.date.strftime('%d.%m.%Y')
            blood_pressure_str = result.blood_pressure
            drugs_str = result.drugs
            message_result += f"Дата: {date_str}, Давление: {blood_pressure_str}, Лекарства: {drugs_str} \n"
    else:
        for result in user_history_result:
            date_str = result.date.strftime('%d.%m.%Y')
            headaches_str = result.headaches
            blood_pressure_str = result.blood_pressure
            drugs_str = result.drugs
            message_result += f"Дата: {date_str}, Головная боль: {headaches_str}, Давление: {blood_pressure_str}, Лекарства: {drugs_str} \n"

    await message.answer('Вот твоя история')
    await message.answer(message_result,
                         reply_markup=nav.mainMenu)
