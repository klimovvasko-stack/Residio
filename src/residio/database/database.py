import sqlite3
from pathlib import Path

# База всегда будет создаваться и открываться в папке residio
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "residio.db"

SCHEMA_SQL = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS user_roles (
    user_role_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS rooms (
    room_id INTEGER PRIMARY KEY AUTOINCREMENT,
    number INTEGER NOT NULL UNIQUE,
    floor INTEGER NOT NULL,
    capacity INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    login TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    user_role INTEGER NOT NULL,
    FOREIGN KEY (user_role)
        REFERENCES user_roles (user_role_id)
);

CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    group_name TEXT NOT NULL,
    room_id INTEGER,
    user_id INTEGER NOT NULL UNIQUE,
    FOREIGN KEY (room_id)
        REFERENCES rooms (room_id),
    FOREIGN KEY (user_id)
        REFERENCES users (user_id)
);

INSERT INTO user_roles (name) VALUES
    ('Administrator'),
    ('Student');

INSERT INTO rooms (number, floor, capacity) VALUES
    (101, 1, 2),
    (102, 1, 3),
    (201, 2, 2),
    (202, 2, 4);

INSERT INTO users (login, password, user_role) VALUES
    ('admin', 'admin123', 1),
    ('ivanov', 'pass1', 2),
    ('smirnov', 'pass2', 2),
    ('petrova', 'pass3', 2),
    ('kuznetsova', 'pass4', 2),
    ('sidorov', 'pass5', 2),
    ('volkova', 'pass6', 2);

INSERT INTO students (full_name, group_name, room_id, user_id) VALUES
    ('Иванов Иван Сергеевич', 'ИВТ-101', 1, 2),
    ('Смирнов Дмитрий Павлович', 'ИВТ-101', 1, 3),
    ('Петрова Анна Олеговна', 'ИВТ-102', 3, 4),
    ('Кузнецова Мария Игоревна', 'ИВТ-102', 3, 5),
    ('Сидоров Пётр Андреевич', 'ИВТ-103', 2, 6),
    ('Волкова Елена Дмитриевна', 'ИВТ-102', NULL, 7);
"""


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")

    # Проверяем, есть ли в базе таблица users. Если нет — создаём и заполняем!
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    if cur.fetchone() is None:
        conn.executescript(SCHEMA_SQL)
        conn.commit()

    return conn