from aiogram import Router, F
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import Message
import utils.keyboard as nav
from datetime import date, timedelta
from db.base import User, HealthDiary
from sqlalchemy import select

router = Router()


@router.message(F.text == 'За Неделю')
async def get_history_week_handler(message: Message, session: AsyncSession):
    _timedelta = timedelta(days=7)

    end_date = date.today()
    start_date = end_date - _timedelta
    user_id = message.from_user.id

    user_mode = await session.execute(
        select(
            User.telegram_id,
            User.only_headaches,
            User.only_blood,
            User.both_mode
        ).where(User.telegram_id == user_id))

    user_mode_scalar = user_mode.fetchone()

    user_history = await session.execute(
        select(
            HealthDiary.telegram_id,
            HealthDiary.date,
            HealthDiary.headaches,
            HealthDiary.blood_pressure,
            HealthDiary.drugs
        ).where(
            (HealthDiary.telegram_id == user_id) &
            (HealthDiary.date >= start_date) &
            (HealthDiary.date <= end_date))
    )

    user_history_scalar = user_history.fetchall()

    message_result = ''

    if user_mode_scalar.only_headaches is True:
        for result in user_history_scalar:
            date_str = result.date.strftime('%d.%m.%Y')
            headaches_str = result.headaches
            if headaches_str is None:
                continue
            drugs_str = result.drugs
            message_result += f"Дата: {date_str}, Головная боль: {headaches_str}, Лекарства: {drugs_str} \n"
    elif user_mode_scalar.only_blood is True:
        for result in user_history_scalar:
            date_str = result.date.strftime('%d.%m.%Y')
            blood_pressure_str = result.blood_pressure
            if blood_pressure_str is None:
                continue
            drugs_str = result.drugs
            message_result += f"Дата: {date_str}, Давление: {blood_pressure_str}, Лекарства: {drugs_str} \n"
    else:
        for result in user_history_scalar:
            date_str = result.date.strftime('%d.%m.%Y')
            headaches_str = result.headaches
            blood_pressure_str = result.blood_pressure
            drugs_str = result.drugs
            # if headaches_str is None:
            #     message_result += f"Дата: {date_str}, Давление: {blood_pressure_str}, Лекарства: {drugs_str} \n"
            # elif blood_pressure_str is None:
            #     message_result += f"Дата: {date_str}, Головная боль: {headaches_str}, Лекарства: {drugs_str} \n"
            # else:
            message_result += f"Дата: {date_str}, Головная боль: {headaches_str}, Давление: {blood_pressure_str}, Лекарства: {drugs_str} \n"
    await message.answer('Вот твоя история')
    await message.answer(message_result, reply_markup=nav.mainMenu)


@router.message(F.text == 'За Месяц')
async def get_history_month_handler(message: Message, session: AsyncSession):
    _timedelta = timedelta(days=30)

    end_date = date.today()
    start_date = end_date - _timedelta
    user_id = message.from_user.id

    user_mode = await session.execute(
        select(
            User.telegram_id,
            User.only_headaches,
            User.only_blood,
            User.both_mode
        ).where(User.telegram_id == user_id))

    user_mode_scalar = user_mode.fetchone()

    user_history = await session.execute(
        select(
            HealthDiary.telegram_id,
            HealthDiary.date,
            HealthDiary.headaches,
            HealthDiary.blood_pressure,
            HealthDiary.drugs
        ).where(
            (HealthDiary.telegram_id == user_id) &
            (HealthDiary.date >= start_date) &
            (HealthDiary.date <= end_date)
        )
    )

    user_history_scalar = user_history.fetchall()

    message_result = ''

    if user_mode_scalar.only_headaches is True:
        for result in user_history_scalar:
            date_str = result.date.strftime('%d.%m.%Y')
            headaches_str = result.headaches
            if headaches_str is None:
                continue
            drugs_str = result.drugs
            message_result += f"Дата: {date_str}, Головная боль: {headaches_str}, Лекарства: {drugs_str} \n"
    elif user_mode_scalar.only_blood is True:
        for result in user_history_scalar:
            date_str = result.date.strftime('%d.%m.%Y')
            blood_pressure_str = result.blood_pressure
            if blood_pressure_str is None:
                continue
            drugs_str = result.drugs
            message_result += f"Дата: {date_str}, Давление: {blood_pressure_str}, Лекарства: {drugs_str} \n"
    else:
        for result in user_history_scalar:
            date_str = result.date.strftime('%d.%m.%Y')
            headaches_str = result.headaches
            blood_pressure_str = result.blood_pressure
            drugs_str = result.drugs
            # if headaches_str is None:
            #     message_result += f"Дата: {date_str}, Давление: {blood_pressure_str}, Лекарства: {drugs_str} \n"
            # elif blood_pressure_str is None:
            #     message_result += f"Дата: {date_str}, Головная боль: {headaches_str}, Лекарства: {drugs_str} \n"
            # else:
            message_result += f"Дата: {date_str}, Головная боль: {headaches_str}, Давление: {blood_pressure_str}, Лекарства: {drugs_str} \n"
    await message.answer('Вот твоя история')
    await message.answer(message_result, reply_markup=nav.mainMenu)