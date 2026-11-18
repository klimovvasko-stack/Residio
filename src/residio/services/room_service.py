from models.room import Room
from repositories import room_repository, student_repository


def list_all_rooms() -> list[Room]:
    return room_repository.find_all_rooms()


def find_room_by_id(room_id: int) -> Room:
    room = room_repository.find_room_by_id(room_id)
    if not room:
        raise Exception("Комната не найдена")
    return room


def count_residents_in_room(room_id: int) -> int:
    students = student_repository.find_students_in_room(room_id)
    return len(students)


def check_room_has_free_spots(room_id: int) -> bool:
    room = find_room_by_id(room_id)
    occupied = count_residents_in_room(room_id)
    return occupied < room.capacity


def list_rooms_with_free_spots() -> list[tuple[Room, int]]:
    # Возвращает список только для комнат со свободными местами
    result = []
    for room in room_repository.find_all_rooms():
        occupied = count_residents_in_room(room.room_id)
        if occupied < room.capacity:
            result.append((room, occupied))
    return result


def add_new_room(number: int, floor: int, capacity: int) -> int:
    if number <= 0:
        raise Exception("Номер комнаты должен быть положительным числом")
    if floor <= 0:
        raise Exception("Этаж должен быть положительным числом")
    if capacity <= 0:
        raise Exception("Вместимость комнаты должна быть больше нуля")

    if room_repository.find_room_by_number(number):
        raise Exception(f"Комната №{number} уже существует")

    return room_repository.add_room(number, floor, capacity)


def edit_room_details(room_id: int, number: int, floor: int, capacity: int):
    room = find_room_by_id(room_id)

    if number <= 0:
        raise Exception("Номер комнаты должен быть положительным числом")
    if floor <= 0:
        raise Exception("Этаж должен быть положительным числом")
    if capacity <= 0:
        raise Exception("Вместимость комнаты должна быть больше нуля")

    existing = room_repository.find_room_by_number(number)
    if existing and existing.room_id != room.room_id:
        raise Exception(f"Комната №{number} уже существует")

    occupied = count_residents_in_room(room_id)
    if capacity < occupied:
        raise Exception(
            f"Нельзя уменьшить вместимость до {capacity}: в комнате уже проживает {occupied} чел."
        )

    room_repository.update_room(room_id, number, floor, capacity)


def remove_room(room_id: int):
    find_room_by_id(room_id)
    occupied = count_residents_in_room(room_id)
    if occupied > 0:
        raise Exception(
            f"Нельзя удалить комнату: в ней проживает {occupied} студ. Сначала выселите их."
        )
    room_repository.remove_room(room_id)
