from dataclasses import dataclass


@dataclass
class Student:
    student_id: int
    full_name: str
    group_name: str
    room_id: int | None
    user_id: int
    # Дополнительные служебные поля для удобного отображения в интерфейсе
    room_number: int | None = None
    login: str | None = None