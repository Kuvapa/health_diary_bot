from aiogram import F, Router, types
from sqlalchemy.ext.asyncio import AsyncSession

import utils.keyboard as nav
import utils.text
from db.base import User

router = Router()


@router.message(F.text == 'Головная боль')
async def headache_mode(message: types.Message, session: AsyncSession,):
    telegram_id = message.from_user.id
    await session.merge(
        User(
            telegram_id=telegram_id,
            only_headaches=True,
            only_blood=False,
            both_mode=False,
        )
    )
    await session.commit()
    await message.answer(
        utils.text.change_mod_confirm,
        reply_markup=nav.mainMenu
    )


@router.message(F.text == 'Кровяное давление')
async def blood_mode(message: types.Message, session: AsyncSession,):
    telegram_id = message.from_user.id
    await session.merge(
        User(
            telegram_id=telegram_id,
            only_headaches=False,
            only_blood=True,
            both_mode=False,
        )
    )
    await session.commit()
    await message.answer(
        utils.text.change_mod_confirm,
        reply_markup=nav.mainMenu
    )


@router.message(F.text == 'Оба показателя')
async def both_mode(message: types.Message, session: AsyncSession,):
    telegram_id = message.from_user.id
    await session.merge(
        User(
            telegram_id=telegram_id,
            only_headaches=False,
            only_blood=False,
            both_mode=True,
        )
    )
    await session.commit()
    await message.answer(
        utils.text.change_mod_confirm,
        reply_markup=nav.mainMenu
    )
