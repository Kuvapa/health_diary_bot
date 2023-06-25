from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import Message, ReplyKeyboardRemove
import utils.keyboard as nav
from db.db_methods import get_mode, add_by_notification
from sqlalchemy import select
from db.base import User
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()
router = Router()


class NotificationForm(StatesGroup):
    SET_HEADACHE = State()
    SET_PRESSURE = State()
    SET_BOTH = State()
    SET_BOTH_BLOOD = State()
    SET_DRUGS = State()


async def get_push(message: Message, session: AsyncSession):
    user_push = await session.execute(
        select(
            User.telegram_id,
            User.push_mode_1,
            User.push_mode_2
        ).where(User.telegram_id == message.from_user.id))
    user_push_scalar = user_push.fetchone()
    return user_push_scalar


@router.message()
async def star_of_notification(
        message: Message,
        session: AsyncSession,
        state: FSMContext
):
    user_mode = await get_mode(message, session)
    if user_mode.only_headaches is True:
        await record_headache(message, state)
    elif user_mode.only_blood is True:
        await record_blood(message, state)
    else:
        await record_both(message, state)


async def get_time(telegram_id, data, session: AsyncSession, message: Message):
    user_push = await get_push(message, session)
    if user_push.push_mode_1 is True:
        user_time = await session.execute(
            select(
                User.telegram_id,
                User.one_time_push
            ).where(User.telegram_id == message.from_user.id)
        )
        user_time_scalar = user_time.scalar()
        scheduler.add_job(
            star_of_notification,
            'date',
            run_date=user_time_scalar,
            args=[telegram_id, data, session]
        )
    else:
        user_time = await session.execute(
            select(
                User.telegram_id,
                User.first_time_push,
                User.second_time_push
            ).where(User.telegram_id == message.from_user.id)
        )
        user_time_scalar = user_time.fetchone()
        scheduler.add_job(
            star_of_notification,
            'date',
            run_date=user_time_scalar[0],
            args=[telegram_id, data, session]
        )
        scheduler.add_job(
            star_of_notification,
            'date',
            run_date=user_time_scalar[1],
            args=[telegram_id, data, session]
        )


async def record_headache(message: Message, state: FSMContext):
    await state.set_state(NotificationForm.SET_HEADACHE)
    await message.answer("Привет! Я с оповещением, давай запишем данные")
    await message.answer("Болела голова сегодня?",
                         reply_markup=nav.chooseMenu)


@router.message(
    NotificationForm.SET_HEADACHE,
    (~(F.text == 'Да') | ~(F.text == 'Нет'))
)
async def wrong_cmd(message: Message):
    await message.answer(
        'Пожалуйста, нажми на кнопочку',
        reply_markup=nav.chooseMenu
    )


async def record_blood(message: Message, state: FSMContext):
    await state.set_state(NotificationForm.SET_PRESSURE)
    await message.answer("Привет! Я с оповещением, давай запишем данные")
    await message.answer("Укажи данные давления в формате СТ\ДТ",
                         reply_markup=ReplyKeyboardRemove())


async def record_both(message: Message, state: FSMContext):
    await state.set_state(NotificationForm.SET_BOTH)
    await message.answer("Привет! Я с оповещением, давай запишем данные")
    await message.answer("Болела голова сегодня?",
                         reply_markup=nav.chooseMenu)


@router.message(
    NotificationForm.SET_HEADACHE,
    (~(F.text == 'Да') | ~(F.text == 'Нет'))
)
async def wrong_cmd(message: Message):
    await message.answer(
        'Пожалуйста, нажми на кнопочку',
        reply_markup=nav.chooseMenu
    )


@router.message(NotificationForm.SET_BOTH)
async def record_both_blood(message: Message, state: FSMContext):
    await state.update_data(SET_BOTH=message.text)
    await state.set_state(NotificationForm.SET_BOTH_BLOOD)
    await message.answer("Укажи данные давления в формате СТ\ДТ",
                         reply_markup=ReplyKeyboardRemove())


@router.message(NotificationForm.SET_HEADACHE)
async def record_drugs_headache(
        message: Message,
        state: FSMContext,
):
    await state.update_data(SET_HEADACHE=message.text)
    await state.set_state(NotificationForm.SET_DRUGS)
    await message.answer("Укажи какие препараты принимал")


@router.message(
    StateFilter(
        NotificationForm.SET_PRESSURE,
        NotificationForm.SET_BOTH_BLOOD
    ),
    F.text.regexp(r'^(8[0-9]|9[0-9]|1[0-9]{2}|2[0-9]{2})\\(4[0-9]|[5-9][0-9]|1[0-4][0-9]|150)$')
)
async def record_drugs(
        message: Message,
        state: FSMContext,
):
    if NotificationForm.SET_PRESSURE:
        await state.update_data(SET_PRESSURE=message.text)
    else:
        await state.update_data(SET_BOTH_BLOOD=message.text)
    await state.set_state(NotificationForm.SET_DRUGS)
    await message.answer("Укажи какие препараты принимал")


@router.message(
    StateFilter(
        NotificationForm.SET_PRESSURE,
        NotificationForm.SET_BOTH_BLOOD
    )
)
async def wrong_pressure_format(message: Message):
    await message.answer('Указан неверный формат давления')


@router.message(NotificationForm.SET_DRUGS)
async def end_of_notification(
        message: Message,
        state: FSMContext,
        session: AsyncSession
):
    await state.update_data(SET_DRUGS=message.text)
    telegram_id = message.from_user.id
    data = await state.get_data()
    await add_by_notification(telegram_id, data, session)
    await session.commit()
    await state.clear()
    await get_time(telegram_id, data, session)
