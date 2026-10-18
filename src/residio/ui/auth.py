from models.user import User
from services import auth_service


def login() -> User | None:
    print("\n--- Вход в систему ---")
    login_value = input("Логин: ")
    password_value = input("Пароль: ")

    user = auth_service.authenticate(login_value, password_value)
    if not user:
        print("Неверный логин или пароль")
        return None

    print(f"Добро пожаловать, {user.login} ({user.role_name})!")
    return user


def register_student():
    print("\n--- Регистрация нового студента ---")
    login_value = input("Придумайте логин: ")
    password_value = input("Придумайте пароль: ")
    full_name = input("ФИО студента: ")
    group_name = input("Учебная группа (например, ИВТ-101): ")

    try:
        student_id = auth_service.register_student(
            login=login_value,
            password=password_value,
            full_name=full_name,
            group_name=group_name
        )
        print(f"Студент успешно зарегистрирован (ID: {student_id})!")
    except Exception as e:
        print(f"Ошибка при регистрации: {e}")


def add_admin():
    print("\n--- Добавление администратора ---")
    login_value = input("Логин нового администратора: ")
    password_value = input("Пароль: ")

    try:
        user_id = auth_service.create_admin(login_value, password_value)
        print(f"Администратор успешно создан (ID: {user_id})!")
    except Exception as e:
        print(f"Ошибка: {e}")