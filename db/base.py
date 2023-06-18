from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    BigInteger, Boolean, Column, Date, Time, ForeignKey,
    String, Integer
)
from sqlalchemy import func
from sqlalchemy.orm import relationship
from datetime import datetime

BaseModel = declarative_base()


class User(BaseModel):
    __tablename__ = 'users_info'

    telegram_id = Column(
        BigInteger,
        unique=True,
        nullable=False,
        primary_key=True
    )
    # Записи режима работы бота
    only_headaches = Column(Boolean, default=False)
    only_blood = Column(Boolean, default=False)
    both_mode = Column(Boolean, default=False)
    # Выбор режима оповещений
    push_mode_1 = Column(Boolean, default=False)
    push_mode_2 = Column(Boolean, default=False)
    # Запись времени оповещений в зависимости от режима
    one_time_push = Column(Time, server_default=None)
    first_time_push = Column(Time, server_default=None)
    second_time_push = Column(Time, server_default=None)

    health_diary_entries = relationship('HealthDiary', back_populates='user')

    def __str__(self):
        return f"<User:{self.telegram_id}>"


class HealthDiary(BaseModel):
    __tablename__ = 'health_diary'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, ForeignKey('users_info.telegram_id'))
    date = Column(Date, server_default=func.current_date())
    headaches = Column(String(20))
    blood_pressure = Column(String(15))
    drugs = Column(String)

    user = relationship('User', back_populates='health_diary_entries')


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
