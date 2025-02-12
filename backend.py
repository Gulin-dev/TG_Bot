import psycopg2
import logging
from tools.content import DB_CONFIG

def save_user_to_db(telegram_id, username):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO users (telegram_id, username, role_id)
            VALUES (%s, %s, 2)
            ON CONFLICT (telegram_id) DO UPDATE SET username = EXCLUDED.username
            """,
            (telegram_id, username),
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        logging.error(f"Ошибка при сохранении пользователя: {e}")

def get_user_role(telegram_id):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT role_id FROM users WHERE telegram_id = %s", (telegram_id,))
        role = cur.fetchone()
        cur.close()
        conn.close()

        if role:
            logging.info(f"Пользователь {telegram_id} имеет роль ID: {role[0]}")
            return role[0]
        else:
            logging.warning(f"Пользователь {telegram_id} не найден в БД, назначаем роль 2 (User)")
            return 2
    except Exception as e:
        logging.error(f"Ошибка при получении роли пользователя: {e}")
        return 2