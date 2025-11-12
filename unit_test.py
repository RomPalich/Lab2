import unittest
from unittest.mock import Mock, patch
from Lab2 import PasswordValidator


class TestPasswordValidator(unittest.TestCase):
    """Unit-тесты для PasswordValidator"""

    def setUp(self):

        """Подготовка тестового окружения"""

        self.validator = PasswordValidator()

    def test_validate_password_length(self):

        """Тест проверки длины пароля"""

        # Слишком короткий пароль
        is_valid, errors = self.validator.validate_password("Short1!")
        self.assertFalse(is_valid)
        self.assertIn("Минимум 8 символов", errors)

        # Достаточно длинный пароль
        is_valid, errors = self.validator.validate_password("LongEnough123!")
        self.assertTrue(is_valid)

    def test_validate_password_lowercase(self):

        """Тест проверки строчных букв"""

        # Нет строчных букв
        is_valid, errors = self.validator.validate_password("NOLOWERCASE123!")
        self.assertFalse(is_valid)
        self.assertIn("Минимум 1 строчная буква", errors)

        # Есть строчные буквы
        is_valid, errors = self.validator.validate_password("HasLowercase123!")
        self.assertTrue(is_valid)

    def test_validate_password_uppercase(self):

        """Тест проверки заглавных букв"""

        # Нет заглавных букв
        is_valid, errors = self.validator.validate_password("nouppercase123!")
        self.assertFalse(is_valid)
        self.assertIn("Минимум 1 заглавная буква", errors)

        # Есть заглавные буквы
        is_valid, errors = self.validator.validate_password("HasUppercase123!")
        self.assertTrue(is_valid)

    def test_validate_password_digit(self):

        """Тест проверки цифр"""

        # Нет цифр
        is_valid, errors = self.validator.validate_password("NoDigitsHere!")
        self.assertFalse(is_valid)
        self.assertIn("Минимум 1 цифра", errors)

        # Есть цифры
        is_valid, errors = self.validator.validate_password("HasDigits123!")
        self.assertTrue(is_valid)

    def test_validate_password_special_chars(self):

        """Тест проверки специальных символов"""

        # Нет специальных символов
        is_valid, errors = self.validator.validate_password("NoSpecial123")
        self.assertFalse(is_valid)
        self.assertIn("Минимум 1 специальный символ", errors)

        # Есть специальные символы
        test_special_chars = ["@", "$", "!", "%", "*", "?", "&", "+", "#", "_"]
        for char in test_special_chars:
            password = f"Password123{char}"
            is_valid, errors = self.validator.validate_password(password)
            self.assertTrue(is_valid, f"Пароль с символом '{char}' должен быть валидным")

    def test_validate_password_strong(self):

        """Тест надежных паролей"""

        self.assertTrue(self.validator.is_strong_password("True123feng!?"), "Пароль должен быть надежный")
        self.assertTrue(self.validator.is_strong_password("NiCik_goodDay123"), "Пароль должен быть надежный")
        self.assertTrue(self.validator.is_strong_password("SaM1y_Umn1y_chuvak?"), "Пароль должен быть надежный")
        self.assertTrue(self.validator.is_strong_password("CAt_My_l1kies"), "Пароль должен быть надежный")

    def test_validate_password_weak(self):

        """Тест ненадежных паролей"""

        self.assertFalse(self.validator.is_strong_password("Bad2!"), "Пароль должен быть ненадежный")
        self.assertFalse(self.validator.is_strong_password("12322078"), "Пароль должен быть ненадежный")
        self.assertFalse(self.validator.is_strong_password("FHEHF_EFhe"), "Пароль должен быть ненадежный")
        self.assertFalse(self.validator.is_strong_password("123123123"), "Пароль должен быть ненадежный")
        self.assertFalse(self.validator.is_strong_password("helloworld"), "Пароль должен быть ненадежный")

    def test_find_passwords_in_text(self):

        """Тест поиска паролей в тексте"""

        test_text = """
        Вот несколько паролей: EwwwqqP@ss1, weak123, 
        еще один WASD$pass2, и просто текст.
        Короткий1! не должен быть найден, а NiceP@ss3 должен.
        Password_true_123 должен быть найден.
        """

        passwords = self.validator.find_passwords_in_text(test_text)
        expected_passwords = ["EwwwqqP@ss1", "WASD$pass2", "NiceP@ss3", "Password_true_123"]

        self.assertEqual(len(passwords), len(expected_passwords))
        for expected in expected_passwords:
            self.assertIn(expected, passwords)

    def test_find_passwords_from_nonexistent_file(self):
        """Тест обработки отсутствующего файла"""
        passwords = self.validator.find_passwords_from_file("nonexistent_file.txt")
        self.assertEqual(passwords, [])

    def test_file(self):
        # Тестирование поиска паролей в файле
        test_txt = """wefhhEFhhhe1231!ef ef12ehfeh_ehfDhefjjeq hefhh123A?e whdfwhh qhwdhh1F231!@ef jehfhehfEG123"""
        # Создание временного файла для тестирования
        with open('password.txt', 'w', encoding='utf-8') as f:
            f.write(test_txt)

        # Поиск паролей в файле
        pws = self.validator.find_passwords_from_file('password.txt')

        # Проверка результатов
        self.assertEqual(len(pws), 4)
        self.assertIn("wefhhEFhhhe1231!ef", pws)
        self.assertIn("ef12ehfeh_ehfDhefjjeq", pws)
        self.assertIn("hefhh123A?e", pws)
        self.assertIn("qhwdhh1F231!@ef", pws)
        self.assertNotIn("whdfwhh", pws)
        self.assertNotIn("jehfhehfEG123", pws)


if __name__ == '__main__':
    # Запуск всех тестов
    unittest.main()