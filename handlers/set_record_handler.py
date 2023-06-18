from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import ReplyKeyboardRemove, Message
from aiogram import Router, F
from datetime import date
import utils.keyboard as nav
from db.base import User, HealthDiary
from sqlalchemy import select

router = Router()

allowed_cmd = ['Да', 'Нет']


class RecordForm(StatesGroup):
    GET_HEADACHE = State()
    GET_PRESSURE_CONF = State()
    GET_PRESSURE = State()
    GET_DRUGS = State()


@router.message(F.text == 'Запись о головной боли')
async def set_headache(message: Message, state: FSMContext):
    await state.set_state(RecordForm.GET_HEADACHE)
    await message.answer(
        'Внезапно заболела голова?',
        reply_markup=nav.chooseMenu
    )


@router.message(F.text == 'Запись о давлении')
async def confirm_set_pressure(message: Message, state: FSMContext):
    await state.set_state(RecordForm.GET_PRESSURE_CONF)
    await message.answer(
        'Внести данные о давлении?',
        reply_markup=nav.chooseMenu
    )


@router.message(F.text == 'Нет')
async def cancel_record(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer(
        'Отменяю внесение данных',
        reply_markup=nav.mainMenu
    )


@router.message(
    RecordForm.GET_HEADACHE,
    RecordForm.GET_PRESSURE_CONF,
    ~F.text.in_(allowed_cmd)
)
async def wrong_cmd(message: Message):
    await message.answer(
        'Пожалуйста, нажми на кнопочку',
    )


@router.message(RecordForm.GET_PRESSURE_CONF)
async def set_pressure(message: Message, state: FSMContext):
    await state.update_data(GET_PRESSURE_CONF=True)
    await state.set_state(RecordForm.GET_PRESSURE)
    await message.answer(
        'Напиши свое давление в формате СТ\ДТ',
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(
    RecordForm.GET_PRESSURE,
    F.text.regexp(r'^(8[0-9]|9[0-9]|1[0-9]{2}|2[0-9]{2})\\(4[0-9]|[5-9][0-9]|1[0-4][0-9]|150)$')
)
async def get_drugs_pressure(message: Message, state: FSMContext):
    await state.update_data(GET_PRESSURE=message.text)
    await state.set_state(RecordForm.GET_DRUGS)
    await message.answer('Напиши какие препараты принимал')


@router.message(RecordForm.GET_PRESSURE)
async def wrong_pressure_format(message: Message):
    await message.answer('Указан неверный формат давления')


@router.message(RecordForm.GET_HEADACHE)
async def get_drugs_headache(message: Message, state: FSMContext):
    await state.update_data(GET_HEADACHE=message.text)
    await state.set_state(RecordForm.GET_DRUGS)
    await message.answer(
        'Напиши какие препараты принимал',
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(RecordForm.GET_DRUGS)
async def finish_record(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(GET_DRUGS=message.text)
    user = await session.execute(
        select(
            User.telegram_id,
        ).where(User.telegram_id == message.from_user.id))
    user_id = user.scalar()
    data = await state.get_data()
    if 'GET_HEADACHE' in data:
        headaches = data['GET_HEADACHE']
        blood_pressure = None
    else:
        headaches = None
        blood_pressure = data['GET_PRESSURE']
    await session.merge(
        HealthDiary(
            telegram_id=user_id,
            date=date.today(),
            headaches=headaches,
            blood_pressure=blood_pressure,
            drugs=data['GET_DRUGS']
        )
    )
    await state.clear()
    await session.commit()
    await message.answer(
        'Отлично, данные записаны',
        reply_markup=nav.mainMenu
    )
