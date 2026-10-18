from models.room import Room
from repositories import room_repository, student_repository


def get_all_rooms() -> list[Room]:
    return room_repository.get_all()


def get_room_by_id(room_id: int) -> Room:
    room = room_repository.get_by_id(room_id)
    if not room:
        raise Exception("Комната не найдена")
    return room


def get_room_occupancy(room_id: int) -> int:
    students = student_repository.get_by_room_id(room_id)
    return len(students)


def is_room_available(room_id: int) -> bool:
    room = get_room_by_id(room_id)
    occupied = get_room_occupancy(room_id)
    return occupied < room.capacity


def get_available_rooms() -> list[tuple[Room, int]]:
    """Возвращает список (комната, кол-во проживающих) только для комнат со свободными местами."""
    result = []
    for room in room_repository.get_all():
        occupied = get_room_occupancy(room.room_id)
        if occupied < room.capacity:
            result.append((room, occupied))
    return result


def create_room(number: int, floor: int, capacity: int) -> int:
    if number <= 0:
        raise Exception("Номер комнаты должен быть положительным числом")
    if floor <= 0:
        raise Exception("Этаж должен быть положительным числом")
    if capacity <= 0:
        raise Exception("Вместимость комнаты должна быть больше нуля")

    if room_repository.get_by_number(number):
        raise Exception(f"Комната №{number} уже существует")

    return room_repository.create(number, floor, capacity)


def update_room(room_id: int, number: int, floor: int, capacity: int):
    room = get_room_by_id(room_id)

    if number <= 0:
        raise Exception("Номер комнаты должен быть положительным числом")
    if floor <= 0:
        raise Exception("Этаж должен быть положительным числом")
    if capacity <= 0:
        raise Exception("Вместимость комнаты должна быть больше нуля")

    existing = room_repository.get_by_number(number)
    if existing and existing.room_id != room.room_id:
        raise Exception(f"Комната №{number} уже существует")

    occupied = get_room_occupancy(room_id)
    if capacity < occupied:
        raise Exception(
            f"Нельзя уменьшить вместимость до {capacity}: в комнате уже проживает {occupied} чел."
        )

    room_repository.update(room_id, number, floor, capacity)


def delete_room(room_id: int):
    get_room_by_id(room_id)
    occupied = get_room_occupancy(room_id)
    if occupied > 0:
        raise Exception(
            f"Нельзя удалить комнату: в ней проживает {occupied} студ. Сначала выселите их."
        )
    room_repository.delete(room_id)