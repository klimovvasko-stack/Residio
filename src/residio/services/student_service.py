from models.student import Student
from repositories import student_repository, room_repository, user_repository
from services import room_service


def get_all_students() -> list[Student]:
    return student_repository.get_all()


def get_student_by_id(student_id: int) -> Student:
    student = student_repository.get_by_id(student_id)
    if not student:
        raise Exception("Студент не найден")
    return student


def get_student_by_user_id(user_id: int) -> Student:
    student = student_repository.get_by_user_id(user_id)
    if not student:
        raise Exception("Профиль студента не найден")
    return student


def get_students_in_room(room_id: int) -> list[Student]:
    room_service.get_room_by_id(room_id)
    return student_repository.get_by_room_id(room_id)


def update_student_info(student_id: int, full_name: str, group_name: str):
    get_student_by_id(student_id)
    full_name = full_name.strip()
    group_name = group_name.strip()

    if not full_name:
        raise Exception("ФИО не может быть пустым")
    if not group_name:
        raise Exception("Группа не может быть пустой")

    student_repository.update(student_id, full_name, group_name)


def assign_room(student_id: int, room_number: int):
    """Заселение или переселение студента по номеру комнаты."""
    student = get_student_by_id(student_id)

    room = room_repository.get_by_number(room_number)
    if not room:
        raise Exception(f"Комната №{room_number} не найдена")

    if student.room_id == room.room_id:
        raise Exception(f"Студент уже заселён в комнату №{room_number}")

    if not room_service.is_room_available(room.room_id):
        raise Exception(f"В комнате №{room_number} нет свободных мест (вместимость: {room.capacity})")

    student_repository.update_room(student_id, room.room_id)


def evict_student(student_id: int):
    """Выселение студента из комнаты."""
    student = get_student_by_id(student_id)
    if student.room_id is None:
        raise Exception("Студент и так не заселён ни в одну комнату")

    student_repository.update_room(student_id, None)


def delete_student(student_id: int):
    """Удаление студента вместе с его учётной записью пользователя."""
    student = get_student_by_id(student_id)
    student_repository.delete(student_id)
    user_repository.delete(student.user_id)