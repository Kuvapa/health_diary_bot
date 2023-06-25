from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import Message
from db.base import User, HealthDiary
from sqlalchemy import select
from datetime import datetime
from datetime import date


async def add_to_db(telegram_id, data, session):
    if data['GET_MODE'] == 'Головная боль':
        only_headaches = True
        only_blood = False
        both_mode = False
        if data['GET_MODE_PUSH'] == '1 раз в день':
            push_mode_1 = True
            one_time_push_format = datetime.strptime(data['GET_TIME'], '%H:%M').time()
            one_time_push = one_time_push_format
            push_mode_2 = False
            first_time_push = None
            second_time_push = None
            await session.merge(
                User(telegram_id=telegram_id,
                     only_headaches=only_headaches,
                     only_blood=only_blood,
                     both_mode=both_mode,
                     push_mode_1=push_mode_1,
                     one_time_push=one_time_push,
                     push_mode_2=push_mode_2,
                     first_time_push=first_time_push,
                     second_time_push=second_time_push
                     )
            )
        else:
            time_values = data['GET_TIME']
            time_list = time_values.split(', ')
            time_str1 = time_list[0]
            time_format1 = datetime.strptime(time_str1, '%H:%M').time()
            time_str2 = time_list[1]
            time_format2 = datetime.strptime(time_str2, '%H:%M').time()
            push_mode_1 = False
            one_time_push = None
            push_mode_2 = True
            first_time_push = time_format1
            second_time_push = time_format2
            await session.merge(
                User(telegram_id=telegram_id,
                     only_headaches=only_headaches,
                     only_blood=only_blood,
                     both_mode=both_mode,
                     push_mode_1=push_mode_1,
                     one_time_push=one_time_push,
                     push_mode_2=push_mode_2,
                     first_time_push=first_time_push,
                     second_time_push=second_time_push
                     )
            )
    elif data['GET_MODE'] == 'Кровяное давление':
        only_headaches = False
        only_blood = True
        both_mode = False
        if data['GET_MODE_PUSH'] == '1 раз в день':
            push_mode_1 = True
            one_time_push_format = datetime.strptime(data['GET_TIME'], '%H:%M').time()
            one_time_push = one_time_push_format
            push_mode_2 = False
            first_time_push = None
            second_time_push = None
            await session.merge(
                User(telegram_id=telegram_id,
                     only_headaches=only_headaches,
                     only_blood=only_blood,
                     both_mode=both_mode,
                     push_mode_1=push_mode_1,
                     one_time_push=one_time_push,
                     push_mode_2=push_mode_2,
                     first_time_push=first_time_push,
                     second_time_push=second_time_push
                     )
            )
        else:
            time_values = data['GET_TIME']
            time_list = time_values.split(', ')
            time_str1 = time_list[0]
            time_format1 = datetime.strptime(time_str1, '%H:%M').time()
            time_str2 = time_list[1]
            time_format2 = datetime.strptime(time_str2, '%H:%M').time()
            push_mode_1 = False
            one_time_push = None
            push_mode_2 = True
            first_time_push = time_format1
            second_time_push = time_format2
            await session.merge(
                User(telegram_id=telegram_id,
                     only_headaches=only_headaches,
                     only_blood=only_blood,
                     both_mode=both_mode,
                     push_mode_1=push_mode_1,
                     one_time_push=one_time_push,
                     push_mode_2=push_mode_2,
                     first_time_push=first_time_push,
                     second_time_push=second_time_push
                     )
            )
    else:
        only_headaches = False
        only_blood = False
        both_mode = True
        if data['GET_MODE_PUSH'] == '1 раз в день':
            push_mode_1 = True
            one_time_push_format = datetime.strptime(data['GET_TIME'], '%H:%M').time()
            one_time_push = one_time_push_format
            push_mode_2 = False
            first_time_push = None
            second_time_push = None
            await session.merge(
                User(telegram_id=telegram_id,
                     only_headaches=only_headaches,
                     only_blood=only_blood,
                     both_mode=both_mode,
                     push_mode_1=push_mode_1,
                     one_time_push=one_time_push,
                     push_mode_2=push_mode_2,
                     first_time_push=first_time_push,
                     second_time_push=second_time_push
                     )
            )
        else:
            time_values = data['GET_TIME']
            time_list = time_values.split(', ')
            time_str1 = time_list[0]
            time_format1 = datetime.strptime(time_str1, '%H:%M').time()
            time_str2 = time_list[1]
            time_format2 = datetime.strptime(time_str2, '%H:%M').time()
            push_mode_1 = False
            one_time_push = None
            push_mode_2 = True
            first_time_push = time_format1
            second_time_push = time_format2
            await session.merge(
                User(telegram_id=telegram_id,
                     only_headaches=only_headaches,
                     only_blood=only_blood,
                     both_mode=both_mode,
                     push_mode_1=push_mode_1,
                     one_time_push=one_time_push,
                     push_mode_2=push_mode_2,
                     first_time_push=first_time_push,
                     second_time_push=second_time_push
                     )
            )


async def get_mode(message: Message, session: AsyncSession):
    user_mode = await session.execute(
        select(
            User.telegram_id,
            User.only_headaches,
            User.only_blood,
            User.both_mode
        ).where(User.telegram_id == message.from_user.id))
    user_mode_scalar = user_mode.fetchone()
    return user_mode_scalar


async def add_by_notification(telegram_id, data, session):
    if data['SET_HEADACHE'] and not data['SET_PRESSURE'] and data['SET_BOTH']:
        await session.merge(
            HealthDiary(
                telegram_id=telegram_id,
                date=date.today(),
                headaches=data['SET_HEADACHE'],
                drugs=data['SET_DRUGS']
            )
        )
    elif data['SET_PRESSURE'] and not data['SET_HEADACHE'] and data['SET_BOTH']:
        await session.merge(
            HealthDiary(
                telegram_id=telegram_id,
                date=date.today(),
                blood_pressure=data['SET_PRESSURE'],
                drugs=data['SET_DRUGS']
            )
        )
    else:
        await session.merge(
            HealthDiary(
                telegram_id=telegram_id,
                date=date.today(),
                headaches=data['SET_BOTH'],
                blood_pressure=data['SET_BOTH_BLOOD'],
                drugs=data['SET_DRUGS']
            )
        )
