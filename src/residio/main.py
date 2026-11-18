# импорт зависимых файлов
from services.auth_service import ADMIN_ROLE_ID, STUDENT_ROLE_ID
from ui.auth import show_login_screen, show_registration_form
from ui.admin_menu import show_admin_panel
from ui.student_menu import show_student_panel
from ui.utils import clear_console, wait_for_enter


def main():
    while True:
        clear_console()
        # выбор действия пользователя 
        print("====================================")
        print("   Система общежития «Residio»")
        print("====================================")
        print("1. Войти в систему")
        print("2. Регистрация студента")
        print("0. Выход из программы")

        choice = input("Выберите действие: ").strip()

        if choice == "1":  # вход в систему 
            user = show_login_screen()  # выводит окно входа в систему и возвращает тип User
            if user: 
                if user.user_role == ADMIN_ROLE_ID:  # проверка на роль пользователя 
                    show_admin_panel(user)  # вывод меню администратора 
                elif user.user_role == STUDENT_ROLE_ID:
                    show_student_panel(user)  # вывод меню студента 
            else:
                wait_for_enter()
        elif choice == "2":  # регистрация студента 
            clear_console()
            show_registration_form()  # меню регистрации студента 
            wait_for_enter()
        elif choice == "0":  # завершение программы 
            print("Работа завершена. До свидания!")
            break
        else: 
            print("Неверная команда, выберите 1, 2 или 0.")
            wait_for_enter()


if __name__ == "__main__":
    main()
