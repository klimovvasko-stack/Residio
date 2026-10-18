from services.auth_service import ADMIN_ROLE_ID, STUDENT_ROLE_ID
from ui.auth import login, register_student
from ui.admin_menu import admin_menu
from ui.student_menu import student_menu


def main():
    while True:
        print("\n====================================")
        print("   Система общежития «Residio»")
        print("====================================")
        print("1. Войти в систему")
        print("2. Регистрация студента")
        print("0. Выход из программы")

        choice = input("Выберите действие: ").strip()

        if choice == "1":
            user = login()
            if user:
                if user.user_role == ADMIN_ROLE_ID:
                    admin_menu(user)
                elif user.user_role == STUDENT_ROLE_ID:
                    student_menu(user)
        elif choice == "2":
            register_student()
        elif choice == "0":
            print("Работа завершена. До свидания!")
            break
        else:
            print("Неверная команда, выберите 1, 2 или 0.")


if __name__ == "__main__":
    main()