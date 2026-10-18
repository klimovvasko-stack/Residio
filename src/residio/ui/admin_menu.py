from models.user import User
from services import room_service, student_service
from ui.auth import add_admin, register_student


def admin_menu(user: User):
    while True:
        print(f"\n===== Меню администратора ({user.login}) =====")
        print("1. Управление комнатами")
        print("2. Управление студентами и заселением")
        print("3. Добавить нового администратора")
        print("0. Выход из аккаунта")

        choice = input("Выберите действие: ").strip()
        if choice == "1":
            rooms_menu()
        elif choice == "2":
            students_menu()
        elif choice == "3":
            add_admin()
        elif choice == "0":
            break
        else:
            print("Неверная команда, попробуйте снова.")


def rooms_menu():
    while True:
        print("\n--- Управление комнатами ---")
        print("1. Список всех комнат")
        print("2. Список свободных комнат")
        print("3. Посмотреть жильцов комнаты")
        print("4. Добавить комнату")
        print("5. Изменить комнату")
        print("6. Удалить комнату")
        print("0. Назад")

        choice = input("Выберите действие: ").strip()

        try:
            if choice == "1":
                rooms = room_service.get_all_rooms()
                print("\nСписок всех комнат:")
                for r in rooms:
                    occupied = room_service.get_room_occupancy(r.room_id)
                    print(
                        f"ID: {r.room_id} | Комната №{r.number} | "
                        f"Этаж: {r.floor} | Занято мест: {occupied}/{r.capacity}"
                    )

            elif choice == "2":
                available = room_service.get_available_rooms()
                if not available:
                    print("Свободных комнат нет.")
                else:
                    print("\nКомнаты со свободными местами:")
                    for r, occupied in available:
                        print(
                            f"Комната №{r.number} (Этаж {r.floor}) — "
                            f"свободно мест: {r.capacity - occupied} из {r.capacity}"
                        )

            elif choice == "3":
                room_id = int(input("Введите ID комнаты: "))
                room = room_service.get_room_by_id(room_id)
                residents = student_service.get_students_in_room(room_id)
                print(f"\nЖильцы комнаты №{room.number}:")
                if not residents:
                    print("В комнате никто не проживает.")
                for s in residents:
                    print(f"- {s.full_name} (группа {s.group_name}, ID: {s.student_id})")

            elif choice == "4":
                number = int(input("Номер комнаты: "))
                floor = int(input("Этаж: "))
                capacity = int(input("Вместимость (чел.): "))
                room_service.create_room(number, floor, capacity)
                print(f"Комната №{number} успешно добавлена!")

            elif choice == "5":
                room_id = int(input("ID комнаты для изменения: "))
                number = int(input("Новый номер комнаты: "))
                floor = int(input("Новый этаж: "))
                capacity = int(input("Новая вместимость: "))
                room_service.update_room(room_id, number, floor, capacity)
                print("Данные комнаты обновлены!")

            elif choice == "6":
                room_id = int(input("ID комнаты для удаления: "))
                room_service.delete_room(room_id)
                print("Комната удалена!")

            elif choice == "0":
                break
            else:
                print("Неверная команда.")

        except ValueError:
            print("Ошибка: необходимо ввести целое число!")
        except Exception as e:
            print(f"Ошибка: {e}")


def students_menu():
    while True:
        print("\n--- Управление студентами ---")
        print("1. Список всех студентов")
        print("2. Зарегистрировать нового студента")
        print("3. Заселить / переселить студента в комнату")
        print("4. Выселить студента из комнаты")
        print("5. Изменить данные студента (ФИО, группа)")
        print("6. Удалить студента")
        print("0. Назад")

        choice = input("Выберите действие: ").strip()

        try:
            if choice == "1":
                students = student_service.get_all_students()
                print("\nСписок студентов:")
                for s in students:
                    room_info = f"Комната №{s.room_number}" if s.room_number else "Не заселён"
                    print(
                        f"ID: {s.student_id} | {s.full_name} | "
                        f"Группа: {s.group_name} | {room_info} | Логин: {s.login}"
                    )

            elif choice == "2":
                register_student()

            elif choice == "3":
                student_id = int(input("Введите ID студента: "))
                room_number = int(input("Введите номер комнаты (например, 101): "))
                student_service.assign_room(student_id, room_number)
                print("Студент успешно заселён!")

            elif choice == "4":
                student_id = int(input("Введите ID студента для выселения: "))
                student_service.evict_student(student_id)
                print("Студент выселен из комнаты.")

            elif choice == "5":
                student_id = int(input("Введите ID студента: "))
                full_name = input("Новое ФИО: ")
                group_name = input("Новая группа: ")
                student_service.update_student_info(student_id, full_name, group_name)
                print("Данные студента обновлены!")

            elif choice == "6":
                student_id = int(input("Введите ID студента для удаления: "))
                student_service.delete_student(student_id)
                print("Студент и его учётная запись удалены.")

            elif choice == "0":
                break
            else:
                print("Неверная команда.")

        except ValueError:
            print("Ошибка: ID и номер комнаты должны быть числами!")
        except Exception as e:
            print(f"Ошибка: {e}")