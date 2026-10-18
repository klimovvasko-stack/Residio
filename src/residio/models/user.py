from dataclasses import dataclass


@dataclass
class User:
    user_id: int
    login: str
    password: str
    user_role: int
    # Дополнительное служебное поле для названия роли ('Administrator' / 'Student')
    role_name: str | None = None