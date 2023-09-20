from datetime import datetime

def get_today_schedule_from_data(schedule_data):
    today = datetime.now().strftime("%Y-%m-%d")

    if "Третья неделя" in schedule_data:
        week_schedule = schedule_data["Третья неделя"]
        for day, day_schedule in week_schedule.items():
            if today in day_schedule:
                return day_schedule[today]
    return None

# Функция для преобразования даты в удобный вид
def format_date(date_str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    return date_obj.strftime("%d.%m.%Y")

# Функция для получения расписания на текущую неделю

async def get_week_schedule_from_data(schedule_data):
    today = datetime.now().strftime("%Y-%m-%d")

    if "Третья неделя" in schedule_data:
        week_schedule = schedule_data["Третья неделя"]
        return week_schedule  # Просто возвращаем расписание на текущую неделю

    return None