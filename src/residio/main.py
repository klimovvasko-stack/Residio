# импорт зависимых файлов
from services.auth_service import ADMIN_ROLE_ID, STUDENT_ROLE_ID
from ui.auth import login, register_student
from ui.admin_menu import admin_menu
from ui.student_menu import student_menu
from ui.utils import clear_screen, pause


def main():
    while True:
        clear_screen()
        # выбор действия пользователя 
        print("====================================")
        print("   Система общежития «Residio»")
        print("====================================")
        print("1. Войти в систему")
        print("2. Регистрация студента")
        print("0. Выход из программы")

        choice = input("Выберите действие: ").strip()

        if choice == "1":  # вход в систему 
            user = login()  # выводит окно входа в систему и возвращает тип User
            if user: 
                if user.user_role == ADMIN_ROLE_ID:  # проверка на роль пользователя 
                    admin_menu(user)  # вывод меню администратора 
                elif user.user_role == STUDENT_ROLE_ID:
                    student_menu(user)  # вывод меню студента 
            else:
                pause()
        elif choice == "2":  # регистрация студента 
            clear_screen()
            register_student()  # меню регистрации студента 
            pause()
        elif choice == "0":  # завершение программы 
            print("Работа завершена. До свидания!")
            break
        else: 
            print("Неверная команда, выберите 1, 2 или 0.")
            pause()


if __name__ == "__main__":
    main()
