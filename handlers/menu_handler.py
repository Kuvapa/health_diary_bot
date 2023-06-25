from aiogram import types, Router, F

import utils.keyboard as nav
import utils.text

router = Router()


allowed_cmd = [
    'Запись о головной боли',
    'Запись о давлении',
    'Получить историю',
    'Настройки',
    'Изменить время оповещения',
    'Изменить режим оповещений',
    'Изменить режим работы',
    '⬅️ Назад',
    'Головная боль',
    'Кровяное давление',
    'Оба показателя',
    'За Неделю',
    'За Месяц',
]


@router.message(~(F.text.in_(allowed_cmd)))
async def unknown_cmd(message: types.Message):
    """If not pressed menu button"""
    await message.reply(
        utils.text.help_message,
        reply_markup=nav.mainMenu)


@router.message(F.text == 'Настройки')
async def settings_menu(message: types.Message):
    """Opens settings menu"""
    await message.answer(
        'Открываю меню настроек',
        reply_markup=nav.settingsMenu)


@router.message(F.text == '⬅️ Назад')
async def back_button(message: types.Message):
    """Button for main menu"""
    await message.answer(
        'Возвращаемся в главное меню',
        reply_markup=nav.mainMenu)


@router.message(F.text == 'Получить историю')
async def history_button(message: types.Message):
    """Opens history menu"""
    await message.answer(
        'Получение истории',
        reply_markup=nav.historyMenu)


@router.message(F.text == 'Изменить режим работы')
async def change_mode(message: types.Message):
    """Change operating mode"""
    await message.answer(
        'Какие показатели будем отслеживать?',
        reply_markup=nav.modeMenu
    )
# логика кнопки изменения режима оповещений и времени работы в соответствующих хендлерах для логики
# потому что тут им особо нет места :D то же самое и про ручные записи

