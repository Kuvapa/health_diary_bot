from datetime import datetime

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession

import utils.keyboard as nav
import utils.text
from db.base import User
from filters.filter import StateValueFilter

router = Router()


allowed_cmd = [
    '1 раз в день',
    '2 раза в день',
]


class PushForm(StatesGroup):
    GET_MODE_PUSH = State()
    GET_TIME = State()
    CHECK_TIME = State()


@router.message(F.text == 'Изменить режим оповещений')
async def get_time_mode(message: types.Message, state: FSMContext):
    await state.set_state(PushForm.GET_MODE_PUSH)
    await message.answer(
        utils.text.start_message3,
        reply_markup=nav.timeMenu
        )


@router.message(PushForm.GET_MODE_PUSH, F.text == utils.text.time_1)
async def set_time1(message: types.Message, state: FSMContext):
    await state.update_data(GET_MODE_PUSH=message.text)
    await state.set_state(PushForm.GET_TIME)
    await message.answer(
        utils.text.set_time1,
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(PushForm.GET_MODE_PUSH, F.text == utils.text.time_2)
async def set_time2(message: types.Message, state: FSMContext):
    await state.update_data(GET_MODE_PUSH=message.text)
    await state.set_state(PushForm.GET_TIME)
    await message.answer(
        utils.text.set_time2,
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(PushForm.GET_MODE_PUSH, ~F.text.in_(allowed_cmd))
async def unknown_time_cmd(message: types.Message):
    """If not pressed button but smthng else"""
    await message.reply(utils.text.wrong_cmd, reply_markup=nav.timeMenu)


@router.message(
    PushForm.GET_TIME,
    StateValueFilter(utils.text.time_1),
    F.text.regexp(r"^(?:[01]\d|2[0-3]):[0-5]\d$")
)
async def check_time1(message: types.Message, state: FSMContext, session: AsyncSession,):
    await state.update_data(GET_TIME=message.text)
    await state.set_state(PushForm.CHECK_TIME)
    await confirm_change1(message, state, session)


@router.message(
    PushForm.GET_TIME,
    StateValueFilter(utils.text.time_2),
    F.text.regexp(r"^(?!.*(\d{2}:\d{2}),\s*\1)(?:[01]\d|2[0-3]):[0-5]\d, (?:[01]\d|2[0-3]):[0-5]\d$")
)
async def check_time2(message: types.Message, state: FSMContext, session: AsyncSession,):
    await state.update_data(GET_TIME=message.text)
    await state.set_state(PushForm.CHECK_TIME)
    await confirm_change2(message, state, session)


@router.message(
    PushForm.GET_TIME,
    StateValueFilter(utils.text.time_1),
)
async def wrong_time(message: types.Message):
    await message.answer(utils.text.wrong_time_format)


@router.message(
    PushForm.GET_TIME,
    StateValueFilter(utils.text.time_2),
)
async def wrong_time(message: types.Message):
    input_str = message.text.strip()
    time_values = input_str.split(', ')
    if len(time_values) != 2:
        await message.answer(utils.text.wrong_time_format)
    else:
        time1 = time_values[0].strip()
        time2 = time_values[1].strip()
        if time1 == time2:
            await message.answer(utils.text.equal_time)


@router.message(PushForm.CHECK_TIME)
async def confirm_change1(message: types.Message, state: FSMContext, session: AsyncSession):
    await state.update_data(CHECK_TIME=True)
    await message.answer('Новый режим и время установлены',
                         reply_markup=nav.mainMenu)
    data = await state.get_data()
    push_mode_1 = True
    push_mode_2 = False
    one_time_push_format = datetime.strptime(data['GET_TIME'], '%H:%M').time()
    one_time_push = one_time_push_format
    await session.merge(User(
        telegram_id=message.from_user.id,
        push_mode_1=push_mode_1,
        push_mode_2=push_mode_2,
        one_time_push=one_time_push,
        first_time_push=None,
        second_time_push=None
        )
    )
    await session.commit()
    await state.clear()


@router.message(PushForm.CHECK_TIME)
async def confirm_change2(message: types.Message, state: FSMContext, session: AsyncSession):
    await state.update_data(CHECK_TIME=True)
    await message.answer('Новый режим и время установлены',
                         reply_markup=nav.mainMenu)
    data = await state.get_data()
    push_mode_1 = False
    push_mode_2 = True
    time_values = data['GET_TIME']
    time_list = time_values.split(', ')
    time_str1 = time_list[0]
    time_format1 = datetime.strptime(time_str1, '%H:%M').time()
    time_str2 = time_list[1]
    time_format2 = datetime.strptime(time_str2, '%H:%M').time()
    await session.merge(User(
        telegram_id=message.from_user.id,
        push_mode_1=push_mode_1,
        push_mode_2=push_mode_2,
        one_time_push=None,
        first_time_push=time_format1,
        second_time_push=time_format2
        )
    )
    await session.commit()
    await state.clear()
