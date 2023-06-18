from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from db.base import User
from sqlalchemy import select


class StateValueFilter(BaseFilter):
    def __init__(self, state_value):
        self.state_value = state_value

    async def __call__(self, message: Message, state: FSMContext) -> bool:
        user_data = await state.get_data()
        return user_data.get('GET_MODE_PUSH') == self.state_value


class PushModeValueFilter(BaseFilter):
    def __init__(self, push_value):
        self.push_value = push_value

    async def __call__(self, message: Message, session: AsyncSession) -> bool:
        user = await session.execute(
            select(
                User.telegram_id,
                User.push_mode_1,
                User.push_mode_2
            ).where(User.telegram_id == message.from_user.id))
        if user:
            row = user.fetchone()
            push_mode_1 = row[1]
            push_mode_2 = row[2]
            if push_mode_1 and not push_mode_2:
                return True
            else:
                return False
