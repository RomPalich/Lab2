import re

class PasswordValidator:
    """
    Класс для проверки и поиска надежных паролей.
    """

    def __init__(self):

        """ Регулярное выражение для проверки надежности пароля
        Требует: минимум 8 символов, хотя бы одну строчную букву, заглавную букву, цифру и специальный символ"""

        self.strong_password_regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&+#_])[A-Za-z\d@$!%*?&+#_]{8,}$')

        self.potential_password_regex = re.compile(r'[A-Za-z\d@$!%*?&+#_]{8,}')

    def validate_password(self, password: str) -> bool:

        """Быстрая проверка пароля."""

        return bool(self.strong_password_regex.match(password))

    def find_passwords_in_text(self, text: str):

        """Находит все надежные пароли в тексте."""

        strong_passwords = []

        for match in self.potential_password_regex.finditer(text):
            password = match.group()
            if self.validate_password(password):
                strong_passwords.append(password)

        return strong_passwords

    def find_passwords_from_file(self, filename: str):
        """Поиск паролей в текстовом файле."""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()
                return self.find_passwords_in_text(content)
        except FileNotFoundError:
            print(f"Файл {filename} не найден")
            return []
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
            return []


def main():
    """Основная функция программы."""
    validator = PasswordValidator()

    while True:
        print("\n" + "=" * 50)
        print("         ПРОВЕРКА НАДЕЖНЫХ ПАРОЛЕЙ")
        print("=" * 50)
        print("1. Проверить пароль")
        print("2. Найти пароли в тексте")
        print("3. Найти пароли в файле")
        print("4. Выход")
        print("-" * 50)

        choice = input("Выберите опцию (1-4): ").strip()

        if choice == '1':
            password = input("Введите пароль для проверки: ")
            is_valid = validator.validate_password(password)
            if is_valid:
                print(f"Пароль '{password}' НАДЕЖНЫЙ!")
            else:
                print(f"Пароль '{password}' НЕНАДЕЖНЫЙ:")

        elif choice == '2':
            text = input("Введите текст для анализа: ")
            passwords = validator.find_passwords_in_text(text)
            print(f"\nНайдено надежных паролей: {len(passwords)}")
            for password in passwords:
                print(f" - '{password}'")

        elif choice == '3':
            filename = input("Введите имя файла: ")
            passwords = validator.find_passwords_from_file(filename)
            if passwords:
                print(f"\nНайдено надежных паролей: {len(passwords)}")
                for password in passwords:
                    print(f" - '{password}'")
            else:
                print("\nНадежные пароли не найдены")

        elif choice == '4':
            print("Выход из программы...")
            break

        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()