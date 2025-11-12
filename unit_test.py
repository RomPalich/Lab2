import unittest
from Lab2 import PasswordValidator


class TestPasswordValidator(unittest.TestCase):

    def setUp(self):

        self.validator = PasswordValidator()

    def test_validate_password_no_length(self):

        is_valid = self.validator.validate_password("Short1!")
        self.assertFalse(is_valid)

    def test_validate_password_length(self):

        is_valid = self.validator.validate_password("LongEnough123!")
        self.assertTrue(is_valid)

    def test_validate_password_no_lowercase(self):

        is_valid = self.validator.validate_password("NOLOWERCASE123!")
        self.assertFalse(is_valid)

    def test_validate_password_lowercase(self):

        is_valid = self.validator.validate_password("HasLowercase123!")
        self.assertTrue(is_valid)

    def test_validate_password_no_uppercase(self):

        is_valid = self.validator.validate_password("nouppercase123!")
        self.assertFalse(is_valid)

    def test_validate_password_uppercase(self):

        is_valid = self.validator.validate_password("Uppercase123!")
        self.assertTrue(is_valid)

    def test_validate_password_no_digit(self):

        is_valid = self.validator.validate_password("NoDigits!")
        self.assertFalse(is_valid)

    def test_validate_password_digit(self):

        is_valid = self.validator.validate_password("Digits123!")
        self.assertTrue(is_valid)

    def test_validate_password_no_special_chars(self):

        is_valid = self.validator.validate_password("NoSpecial123")
        self.assertFalse(is_valid)

    def test_validate_password_special_chars(self):

        test_special_chars = ["@", "$", "!", "%", "*", "?", "&", "+", "#", "_"]
        for char in test_special_chars:
            password = f"Password123{char}"
            is_valid = self.validator.validate_password(password)
            self.assertTrue(is_valid, f"Пароль с символом '{char}' должен быть валидным")

    def test_validate_password_strong(self):

        self.assertTrue(self.validator.validate_password("True123feng!?"), "Пароль должен быть надежный")

    def test_validate_password_no_strong(self):

        self.assertFalse(self.validator.validate_password("Bad2!"), "Пароль должен быть ненадежный")

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

    def test_file(self):
        # Тестирование поиска паролей в файле

        test_txt = """wefhhEFhhhe1231!ef ef12ehfeh_ehfDhefjjeq hefhh123A?e whdfwhh qhwdhh1F231!@ef jehfhehfEG123"""

        # Создание временного файла для тестирования

        with open('password.txt', 'w', encoding='utf-8') as f:
            f.write(test_txt)

        # Поиск паролей в файле

        passwords = self.validator.find_passwords_from_file('password.txt')

        # Проверка результатов

        self.assertEqual(len(passwords), 4)
        self.assertIn("wefhhEFhhhe1231!ef", passwords)
        self.assertIn("ef12ehfeh_ehfDhefjjeq", passwords)
        self.assertIn("hefhh123A?e", passwords)
        self.assertIn("qhwdhh1F231!@ef", passwords)
        self.assertNotIn("whdfwhh", passwords)
        self.assertNotIn("jehfhehfEG123", passwords)


if __name__ == '__main__':
    # Запуск всех тестов
    unittest.main()