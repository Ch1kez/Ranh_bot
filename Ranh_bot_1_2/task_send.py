import asyncio
import schedule
from db_connection import StudentDB
from datetime import datetime
from handlers import send_schedule

# Время, когда нужно отправлять расписание
schedule_times = ["02:00-02:23", "14:30-15:30"]
db = StudentDB

async def send_schedule_at_specific_times():
    # while True:
    #     current_time = datetime.now().strftime("%H:%M")

        # if current_time in schedule_times:
            list_of_chat_ids = db.get_all_user_ids()
            for chat_id in list_of_chat_ids:
                await send_schedule(chat_id)

        # Заснуть на 1 минуту перед проверкой времени снова
        # await asyncio.sleep(60)

async def task_send_schedule_at_specific_times():
    # Здесь вставьте инициализацию бота и другие настройки

    # Задача для отправки в 9:10
    schedule.every().day.at("09:10").do(asyncio.run, send_schedule_at_specific_times)

    # Задача для отправки в 14:30
    schedule.every().day.at("14:30").do(asyncio.run, send_schedule_at_specific_times)

    # Пример задачи для отправки за 10 минут до времени из переменной
    # Здесь переменная next_time должна содержать желаемое время в формате HH:MM
    next_time = "02:46"
    schedule.every().day.at(next_time).do(asyncio.run, send_schedule_at_specific_times)

    while True:
        schedule.run_pending()
        await asyncio.sleep(1)
