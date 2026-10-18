from models.user import User
from services import student_service, room_service


def student_menu(user: User):
    while True:
        print(f"\n===== Личный кабинет студента ({user.login}) =====")
        print("1. Мой профиль и комната")
        print("2. Мои соседи по комнате")
        print("3. Список свободных комнат в общежитии")
        print("0. Выход из аккаунта")

        choice = input("Выберите действие: ").strip()

        try:
            if choice == "1":
                student = student_service.get_student_by_user_id(user.user_id)
                room_str = f"Комната №{student.room_number}" if student.room_number else "Пока не заселён"
                print("\n--- Мои данные ---")
                print(f"ФИО:    {student.full_name}")
                print(f"Группа: {student.group_name}")
                print(f"Статус: {room_str}")

            elif choice == "2":
                student = student_service.get_student_by_user_id(user.user_id)
                if not student.room_id:
                    print("Вы пока не заселены ни в одну комнату.")
                else:
                    residents = student_service.get_students_in_room(student.room_id)
                    print(f"\nПроживающие в комнате №{student.room_number}:")
                    for r in residents:
                        you_mark = " (Вы)" if r.student_id == student.student_id else ""
                        print(f"- {r.full_name} (гр. {r.group_name}){you_mark}")

            elif choice == "3":
                available = room_service.get_available_rooms()
                if not available:
                    print("Свободных мест в общежитии сейчас нет.")
                else:
                    print("\nКомнаты со свободными местами:")
                    for room, occupied in available:
                        print(
                            f"Комната №{room.number} (Этаж {room.floor}) — "
                            f"свободно мест: {room.capacity - occupied} из {room.capacity}"
                        )

            elif choice == "0":
                break
            else:
                print("Неверная команда.")

        except Exception as e:
            print(f"Ошибка: {e}")