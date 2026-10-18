from models.user import User
from repositories import user_repository, student_repository

ADMIN_ROLE_ID = 1
STUDENT_ROLE_ID = 2


def authenticate(login: str, password: str) -> User | None:
    login = login.strip()
    password = password.strip()

    if not login or not password:
        return None

    user = user_repository.get_by_login(login)
    if not user or user.password != password:
        return None

    return user


def register_student(
    login: str,
    password: str,
    full_name: str,
    group_name: str
) -> int:
    login = login.strip()
    password = password.strip()
    full_name = full_name.strip()
    group_name = group_name.strip()

    if not login:
        raise Exception("Логин не может быть пустым")
    if not password:
        raise Exception("Пароль не может быть пустым")
    if not full_name:
        raise Exception("ФИО студента не может быть пустым")
    if not group_name:
        raise Exception("Название группы не может быть пустым")

    if user_repository.get_by_login(login):
        raise Exception(f"Пользователь с логином '{login}' уже существует")

    # Сначала создаём аккаунт пользователя с ролью Student (2)
    user_id = user_repository.create(login, password, STUDENT_ROLE_ID)
    # Затем создаём профиль студента (пока без комнаты: room_id = None)
    student_id = student_repository.create(full_name, group_name, None, user_id)
    return student_id


def create_admin(login: str, password: str) -> int:
    login = login.strip()
    password = password.strip()

    if not login:
        raise Exception("Логин не может быть пустым")
    if not password:
        raise Exception("Пароль не может быть пустым")

    if user_repository.get_by_login(login):
        raise Exception(f"Пользователь с логином '{login}' уже существует")

    return user_repository.create(login, password, ADMIN_ROLE_ID)