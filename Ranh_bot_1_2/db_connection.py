import sqlite3
from datetime import datetime

class StudentDB:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS students
                     (user_id INTEGER PRIMARY KEY, msg_time TEXT)''')
        self.conn.commit()

    def add_student_info(self, user_id, msg_text):
        msg_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        c = self.conn.cursor()

        # Проверяем, существует ли запись с таким user_id
        c.execute("SELECT COUNT(*) FROM students WHERE user_id=?", (user_id,))
        result = c.fetchone()
        if result[0] > 0:
            # Если запись существует, обновляем ее
            c.execute("UPDATE students SET msg_time=? WHERE user_id=?", (msg_time, user_id))
        else:
            # Если записи нет, вставляем новую
            c.execute("INSERT INTO students (user_id, msg_time) VALUES (?, ?)", (user_id, msg_time))

        self.conn.commit()

    def check_user_exist(self, user_id):
        c = self.conn.cursor()
        c.execute("SELECT COUNT(*) FROM students WHERE user_id=?", (user_id,))
        result = c.fetchone()
        return result[0] > 0

    def get_all_user_ids(self):
        c = self.conn.cursor()
        c.execute("SELECT user_id FROM students")
        user_ids = [row[0] for row in c.fetchall()]  # Преобразуем результат в список int
        return user_ids

    def close(self):
        self.conn.close()

# Пример использования класса:
if __name__ == "__main__":
    db = StudentDB("students.db")
    user_id = 12345  # Замените на фактический user_id
    db.add_student_info(user_id=user_id, msg_text='тестовый пользователь')
    if db.check_user_exist(user_id):
        print(f"Пользователь с user_id {user_id} существует в базе данных.")
    else:
        print(f"Пользователь с user_id {user_id} не найден в базе данных.")

    db.close()
