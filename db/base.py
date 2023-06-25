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
