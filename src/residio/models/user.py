from dataclasses import dataclass


@dataclass
class User:
    user_id: int                # первичный ключ 
    login: str                  # логин для входа в систему 
    password: str               # пароль для входа в систему 
    user_role: int              # внешний ключ для связи с ролью 

    # Дополнительное служебное поле для названия роли (Administrator / Student)
    role_name: str | None = None