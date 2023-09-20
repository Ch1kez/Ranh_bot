import asyncio
from task_send import task_send_schedule_at_specific_times
from aiogram import Bot, Dispatcher
from db_connection import StudentDB
from aiogram.utils import executor
from config import BOT_TOKEN

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
loop = asyncio.get_event_loop()

# Создаем объект для работы с базой данных
db = StudentDB("students.db")

if __name__ == '__main__':
    from handlers import *
    asyncio.run(task_send_schedule_at_specific_times())
    executor.start_polling(dp, skip_updates=True)
