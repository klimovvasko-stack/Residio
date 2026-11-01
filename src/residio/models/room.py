from dataclasses import dataclass # библиотека генерирует для класса базовые методы


@dataclass
class Room: 
    room_id: int    # первичный ключ 
    number: int     # номер комнаты в общежитии
    floor: int      # этаж
    capacity: int   # вместимость комнаты 