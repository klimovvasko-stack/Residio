from dataclasses import dataclass


@dataclass
class Student:
    student_id: int             # идентификатор студента 
    full_name: str              # имя студнета 
    group_name: str             # греппа студента
    room_id: int | None         # ключ связывающий студнета и комнату (может не быть)
    user_id: int                # ключ связывабщий с учетными данными 

    # Дополнительные служебные поля для удобного отображения в интерфейсе
    # Для того, чтобы при выводе информации лишний раз не обращаться к бд
    room_number: int | None = None
    login: str | None = None