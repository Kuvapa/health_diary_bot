from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import ReplyKeyboardRemove, Message
from filters.filter import PushModeValueFilter
import utils.text
import utils.keyboard as nav
from datetime import datetime
from db.base import User

router = Router()


class TimeForm(StatesGroup):
    GET_TIME1 = State()
    GET_TIME2 = State()
    CHECK_TIME = State()


@router.message(
    PushModeValueFilter(True),
    F.text == 'Изменить время оповещения',
)
async def set_time1(message: Message, state: FSMContext):
    await state.set_state(TimeForm.GET_TIME1)
    await message.answer(
        utils.text.set_time1,
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(
    ~PushModeValueFilter(True),
    F.text == 'Изменить время оповещения',
)
async def set_time2(message: Message, state: FSMContext):
    await state.set_state(TimeForm.GET_TIME2)
    await message.answer(
        utils.text.set_time2,
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(
    TimeForm.GET_TIME1,
    F.text.regexp(r"^(?:[01]\d|2[0-3]):[0-5]\d$")
)
async def check_time1(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(GET_TIME=message.text)
    await state.set_state(TimeForm.CHECK_TIME)
    await confirm_time1(message, state, session)


@router.message(
    TimeForm.GET_TIME2,
    F.text.regexp(r"^(?!.*(\d{2}:\d{2}),\s*\1)(?:[01]\d|2[0-3]):[0-5]\d, (?:[01]\d|2[0-3]):[0-5]\d$")
)
async def check_time2(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(GET_TIME=message.text)
    await state.set_state(TimeForm.CHECK_TIME)
    await confirm_time2(message, state, session)


@router.message(
    TimeForm.GET_TIME1,
)
async def wrong_time1(message: Message):
    await message.answer(utils.text.wrong_time_format)


@router.message(
    TimeForm.GET_TIME2,
)
async def wrong_time2(message: Message):
    input_str = message.text.strip()
    time_values = input_str.split(', ')
    if len(time_values) != 2:
        await message.answer(utils.text.wrong_time_format)
    else:
        time1 = time_values[0].strip()
        time2 = time_values[1].strip()
        if time1 == time2:
            await message.answer(utils.text.equal_time)


@router.message(TimeForm.CHECK_TIME)
async def confirm_time1(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(CHECK_TIME=True)
    await message.answer('Новое время установлено',
                         reply_markup=nav.mainMenu)
    data = await state.get_data()
    one_time_push_format = datetime.strptime(data['GET_TIME'], '%H:%M').time()
    one_time_push = one_time_push_format
    await session.merge(User(
        telegram_id=message.from_user.id,
        one_time_push=one_time_push
        )
    )
    await session.commit()
    await state.clear()


@router.message(TimeForm.CHECK_TIME)
async def confirm_time2(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(CHECK_TIME=True)
    await message.answer('Новое время установлено',
                         reply_markup=nav.mainMenu)
    data = await state.get_data()
    time_values = data['GET_TIME']
    time_list = time_values.split(', ')
    time_str1 = time_list[0]
    time_format1 = datetime.strptime(time_str1, '%H:%M').time()
    time_str2 = time_list[1]
    time_format2 = datetime.strptime(time_str2, '%H:%M').time()
    await session.merge(User(
        telegram_id=message.from_user.id,
        first_time_push=time_format1,
        second_time_push=time_format2
        )
    )
    await session.commit()
    await state.clear()
