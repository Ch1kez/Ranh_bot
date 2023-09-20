

from datetime import datetime, timedelta
import logging
import asyncio
from student_schedule_data import student_schedule
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor

# Вставьте ваш токен от @BotFather
BOT_TOKEN = '5942243404:AAFduulHWieMebGvVI1T_Ygauz7EJn1dQXI'

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)
dp.middleware.setup(LoggingMiddleware())


def get_today_schedule(schedule_data):
    today = datetime.now().strftime("%Y-%m-%d")

    if "Вторая неделя" in schedule_data:
        week_schedule = schedule_data["Вторая неделя"]
        for day, day_schedule in week_schedule.items():
            if today in day_schedule:
                return day_schedule[today]

    return None


# Функция для отправки красиво оформленного расписания
async def send_schedule(chat_id):
    today_schedule = get_today_schedule(student_schedule)
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


# Функция для преобразования даты в удобный вид
def format_date(date_str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    return date_obj.strftime("%d.%m.%Y")


# Обработка команды /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply(
        '<b>Привет!</b>\nЯ бот для отправки расписания. \nНажми:\n<code>/schedule</code> и получи '
        'расписание на день\n<code>/week_schedule</code> для расписания на неделю. 😊',
        parse_mode='HTML')


# Обработка команды /schedule
@dp.message_handler(commands=['schedule'])
async def get_schedule(message: types.Message):
    chat_id = message.chat.id
    await send_schedule(chat_id)


# Обработка команды /week_schedule
@dp.message_handler(commands=['week_schedule'])
async def get_week_schedule(message: types.Message):
    chat_id = message.chat.id
    week_schedule = await get_week_schedule(student_schedule)

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


# Функция для получения расписания на текущую неделю
async def get_week_schedule(schedule_data):
    today = datetime.now().strftime("%Y-%m-%d")

    if "Вторая неделя" in schedule_data:
        week_schedule = schedule_data["Вторая неделя"]
        return week_schedule  # Просто возвращаем расписание на текущую неделю

    return None


if __name__ == '__main__':
    from aiogram import executor

    loop = asyncio.get_event_loop()
    executor.start_polling(dp, skip_updates=True)
