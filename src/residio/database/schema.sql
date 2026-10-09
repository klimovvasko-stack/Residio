    PRAGMA foreign_keys = ON;

    -- Удаление старой структуры (сначала зависимые таблицы)
    DROP TABLE IF EXISTS students;
    DROP TABLE IF EXISTS users;
    DROP TABLE IF EXISTS rooms;
    DROP TABLE IF EXISTS user_roles;

    -- Справочник ролей
    CREATE TABLE user_roles (
        user_role_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    );

    -- Комнаты
    CREATE TABLE rooms (
        room_id INTEGER PRIMARY KEY AUTOINCREMENT,
        number INTEGER NOT NULL UNIQUE,
        floor INTEGER NOT NULL,
        capacity INTEGER NOT NULL
    );

    -- Пользователи
    CREATE TABLE users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        login TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        user_role INTEGER NOT NULL,
        FOREIGN KEY (user_role)
            REFERENCES user_roles (user_role_id)
    );

    -- Студенты
    CREATE TABLE students (
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

    -- Роли
    INSERT INTO user_roles (name) VALUES
        ('Administrator'),
        ('Student');

    -- Комнаты
    INSERT INTO rooms (number, floor, capacity) VALUES
        (101, 1, 2),
        (102, 1, 3),
        (201, 2, 2),
        (202, 2, 4);

    -- Пользователи (user_role: 1 = Administrator, 2 = Student)
    INSERT INTO users (login, password, user_role) VALUES
        ('admin', 'admin123', 1),
        ('ivanov', 'pass1', 2),
        ('smirnov', 'pass2', 2),
        ('petrova', 'pass3', 2),
        ('kuznetsova', 'pass4', 2),
        ('sidorov', 'pass5', 2),
        ('volkova', 'pass6', 2);

    -- Студенты (room_id = NULL, если студент пока не заселён)
    INSERT INTO students (full_name, group_name, room_id, user_id) VALUES
        ('Иванов Иван Сергеевич', 'ИВТ-101', 1, 2),
        ('Смирнов Дмитрий Павлович', 'ИВТ-101', 1, 3),
        ('Петрова Анна Олеговна', 'ИВТ-102', 3, 4),
        ('Кузнецова Мария Игоревна', 'ИВТ-102', 3, 5),
        ('Сидоров Пётр Андреевич', 'ИВТ-103', 2, 6),
        ('Волкова Елена Дмитриевна', 'ИВТ-102', NULL, 7);