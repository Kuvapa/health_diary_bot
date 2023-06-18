from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

"""Button back to Main menu"""
btnBack = KeyboardButton(text='⬅️ Назад')

"""Choose how bot works"""
btnOnlyHeadache = KeyboardButton(text='Головная боль')
btnOnlyBloodPressure = KeyboardButton(text='Кровяное давление')
btnBothOptions = KeyboardButton(text='Оба показателя')
modeMenu = ReplyKeyboardMarkup(
    keyboard=[[btnOnlyHeadache, btnOnlyBloodPressure, btnBothOptions]],
    resize_keyboard=True)

"""Choose time for notificcation"""
btnOneTime = KeyboardButton(text='1 раз в день')
btnTwoTimes = KeyboardButton(text='2 раза в день')
timeMenu = ReplyKeyboardMarkup(
    keyboard=[[btnOneTime, btnTwoTimes]],
    resize_keyboard=True
    )

"""Main menu keyboard"""
btnHeadache = KeyboardButton(text='Запись о головной боли')
btnBloodPressure = KeyboardButton(text='Запись о давлении')
btnHistory = KeyboardButton(text='Получить историю')
btnSettings = KeyboardButton(text='Настройки')
mainMenu = ReplyKeyboardMarkup(
    keyboard=[[btnHeadache, btnBloodPressure], [btnHistory], [btnSettings]],
    resize_keyboard=True)

"""Settings menu"""
btnChangeTime = KeyboardButton(text='Изменить время оповещения')
btnChangePush = KeyboardButton(text='Изменить режим оповещений')
btnChangeMode = KeyboardButton(text='Изменить режим работы')
# btnChangeLanguage = KeyboardButton(text='Изменить язык')
settingsMenu = ReplyKeyboardMarkup(
    keyboard=[[btnChangeMode, btnChangePush],
              [btnChangeTime],  [btnBack]],
    resize_keyboard=True)


"""History menu"""
btnWeek = KeyboardButton(text='За Неделю')
btnMonth = KeyboardButton(text='За Месяц')
historyMenu = ReplyKeyboardMarkup(
    keyboard=[[btnWeek, btnMonth], [btnBack]],
    resize_keyboard=True)


""""Yes or No keyboard"""
btnYes = KeyboardButton(text='Да')
btnNo = KeyboardButton(text='Нет')
chooseMenu = ReplyKeyboardMarkup(
    keyboard=[[btnYes, btnNo]],
    resize_keyboard=True
)
