from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import ReplyKeyboardRemove, Message
import utils.keyboard as nav
from utils.text import (start_message, start_message2, wrong_cmd, start_message3,
                        time_1, set_time1, time_2, set_time2, wrong_time_format, equal_time,
                        end_start_handler)
from db.db_methods import add_to_db
from filters.filter import StateValueFilter
import time

router = Router()


allowed_cmd = [
    'Головная боль',
    'Кровяное давление',
    'Оба показателя',
    '1 раз в день',
    '2 раза в день',
]


class ModeForm(StatesGroup):
    GET_MODE = State()
    GET_MODE_PUSH = State()
    GET_TIME = State()
    CHECK_TIME = State()


@router.message(Command("start"))
async def cmd_start(
    message: Message,
    state: FSMContext,
):
    """Start command handler and beginning of FSM"""
    await state.set_state(ModeForm.GET_MODE)
    await message.answer(start_message)
    await message.answer(
        start_message2,
        reply_markup=nav.modeMenu
    )


@router.message(ModeForm.GET_MODE, ~F.text.in_(allowed_cmd))
async def unknown_mode(message: Message):
    """If not pressed button but smthng else"""
    await message.reply(wrong_cmd, reply_markup=nav.modeMenu)


@router.message(ModeForm.GET_MODE)
async def get_time_mode(message: Message, state: FSMContext):
    """FSM choosing push mode"""
    await state.update_data(GET_MODE=message.text)
    await state.set_state(ModeForm.GET_MODE_PUSH)
    await message.answer(
        start_message3,
        reply_markup=nav.timeMenu
        )


@router.message(ModeForm.GET_MODE_PUSH, F.text == time_1)
async def set_time_1(message: Message, state: FSMContext):
    """If 1 time notification, type time"""
    await state.update_data(GET_MODE_PUSH=message.text)
    await state.set_state(ModeForm.GET_TIME)
    await message.answer(
        set_time1,
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(ModeForm.GET_MODE_PUSH, F.text == time_2)
async def set_time_2(message: Message, state: FSMContext):
    """If 2 time notification, type time"""
    await state.update_data(GET_MODE_PUSH=message.text)
    await state.set_state(ModeForm.GET_TIME)
    await message.answer(
        set_time2,
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(ModeForm.GET_MODE_PUSH, ~F.text.in_(allowed_cmd))
async def unknown_time_cmd(message: Message):
    """If not pressed button but smthng else"""
    await message.reply(wrong_cmd, reply_markup=nav.timeMenu)


@router.message(
    ModeForm.GET_TIME,
    StateValueFilter(time_1),
    F.text.regexp(r"^(?:[01]\d|2[0-3]):[0-5]\d$")
)
async def check_time1(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(GET_TIME=message.text)
    await state.set_state(ModeForm.CHECK_TIME)
    await start_handler_end(message, state, session)


@router.message(
    ModeForm.GET_TIME,
    StateValueFilter(time_2),
    F.text.regexp(r"^(?!.*(\d{2}:\d{2}),\s*\1)(?:[01]\d|2[0-3]):[0-5]\d, (?:[01]\d|2[0-3]):[0-5]\d$")
)
async def check_time2(message: Message, state: FSMContext, session: AsyncSession,):
    await state.update_data(GET_TIME=message.text)
    await state.set_state(ModeForm.CHECK_TIME)
    await start_handler_end(message, state, session)


@router.message(
    ModeForm.GET_TIME,
    StateValueFilter(time_1),
)
async def wrong_time(message: Message):
    await message.answer(wrong_time_format)


@router.message(
    ModeForm.GET_TIME,
    StateValueFilter(time_2),
)
async def wrong_time(message: Message):
    input_str = message.text.strip()
    time_values = input_str.split(', ')
    if len(time_values) != 2:
        await message.answer(wrong_time_format)
    else:
        time1 = time_values[0].strip()
        time2 = time_values[1].strip()
        if time1 == time2:
            await message.answer(equal_time)


@router.message(ModeForm.CHECK_TIME)
async def start_handler_end(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
):
    """End of FSM and over of start handler"""
    await state.update_data(CHECK_TIME=True)
    await message.answer(end_start_handler,
                         reply_markup=nav.mainMenu)
    telegram_id = message.from_user.id
    if telegram_id == 5174925245:
        await message.answer('Сработало? Да ладно')
        await message.answer_sticker(r'CAACAgIAAxkBAAJaQ2SDZNRgDRJ_kgrNakMZNP1NNGSAAAISFAACxKi4SvuDeGU0zHjnLwQ')
        time.sleep(5)
        await message.answer('Меня если что звать')
        await message.answer_sticker(r'CAACAgIAAxkBAAJaQWSDZM16Okbp6td6vqeYNbIBiSrFAAI4GAACg8CwSqVPSLqF0GmsLwQ')
        time.sleep(5)
        await message.answer('А теперь')
        await message.answer_sticker(r'CAACAgIAAxkBAAJaP2SDZDvGGh3-xlpDclXOCduWf0XjAALaFwACZg_xStjUsJqeuKVYLwQ')
    data = await state.get_data()
    await add_to_db(telegram_id, data, session)
    await session.commit()
    await state.clear()
