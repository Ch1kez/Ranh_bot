from aiogram import types
from main import dp, bot, db
from datetime import datetime
from student_schedule_data import student_schedule
from schedule_univers import get_today_schedule_from_data, get_week_schedule_from_data


# @dp.message_handler()
# async def start(message: types.Message):
#     print(message)


# Обработка команды /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id = message.from_user.id

    # Проверяем, зарегистрирован ли пользователь в базе данных
    if not db.check_user_exist(user_id):
        db.add_student_info(user_id, message.text)
        await message.answer(
            "Добро пожаловать! Вы успешно зарегистрированы в базе данных бота.\n"
            "Расписание будет отправляться вам в следующие моменты:\n"
            "- В 9:00 утра\n"
            "- В 14:30\n"
            "- За 10 минут до начала каждой пары."
        )
    else:
        await message.answer(
            "Вы уже зарегистрированы в базе данных бота.\n"
            "Расписание будет отправляться вам в следующие моменты:\n"
            "- В 9:00 утра\n"
            "- В 14:30\n"
            "- За 10 минут до начала каждой пары."
        )

    # Отправляем информацию о доступных командах
    await message.answer(
        '<b>Доступные команды:</b>\n'
        '<code>/schedule</code> - получить расписание на день\n'
        '<code>/week_schedule</code> - получить расписание на неделю\n'
        '<code>/help</code> - получить справку о доступных командах',
        parse_mode='HTML'
    )

# Обработка команды /help (второе приветственное сообщение)
@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    await message.answer(
        '<b>Привет!</b>\nЯ бот для отправки расписания. \nНажми:\n<code>/schedule</code> и получи '
        'расписание на день\n<code>/week_schedule</code> для расписания на неделю. 😊\n'
        'Если у вас есть вопросы, предложения или жалобы на бота, пожалуйста, обращайтесь к '
        'создателю по тэгу в Telegram: @KurnaevDV',
        parse_mode='HTML')

# Обработка команды /schedule
@dp.message_handler(commands=['schedule'])
async def get_schedule(message: types.Message):
    chat_id = message.chat.id
    await send_schedule(chat_id)


@dp.message_handler(commands=['week_schedule'])
async def get_week_schedule(message: types.Message):
    chat_id = message.chat.id
    week_schedule = await get_week_schedule_from_data(student_schedule)

    if week_schedule:
        msg = "<b>Расписание на текущую неделю:</b>\n\n"
        for day, day_schedule in week_schedule.items():
            msg += f"<u>{day}:</u>\n"
            for date, para_data in day_schedule.items():
                formatted_date = format_date(date)
                msg += f"<i>Дата:</i> {formatted_date}\n"
                for para, details in para_data.items():
                    # msg += f"<i>Пара {para}:</i>\n"
                    msg += f"<i>Время:</i> {details['Время']}\n"
                    msg += f"<i>Предмет:</i> {details['Предмет']}\n"
                    msg += f"<i>Преподаватель:</i> {details['Преподаватель']}\n"
                    msg += f"<i>Формат обучения:</i> {details['Формат обучения']}\n"
                    msg += f"<i>Дополнительная информация:</i> <u>{details['Дополнительная информация']}</u>\n\n"

        await bot.send_message(chat_id, msg, parse_mode='HTML')
    else:
        await bot.send_message(chat_id, "На текущую неделю расписания нет.")


# Функция для отправки красиво оформленного расписания
async def send_schedule(chat_id):
    today_schedule = get_today_schedule_from_data(student_schedule)
    if today_schedule:
        msg = "<b>Расписание на сегодня:</b>\n"
        for para, para_data in today_schedule.items():
            # msg += f"<u>Пара {para}:</u>\n"
            msg += f"<i>Время:</i> {para_data['Время']}\n" \
                   f"<i>Предмет:</i> {para_data['Предмет']}\n" \
                   f"<i>Преподаватель:</i> {para_data['Преподаватель']}\n" \
                   f"<i>Формат обучения:</i> {para_data['Формат обучения']}\n" \
                   f"<i>Дополнительная информация:</i> {para_data['Дополнительная информация']}\n\n"
        await bot.send_message(chat_id, msg, parse_mode='HTML')
    else:
        await bot.send_message(chat_id, "На сегодня расписания нет.")


def format_date(date_str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    return date_obj.strftime("%d.%m.%Y")
