import unittest
import os
import string
from belch import PasswordGenerator

class TestPasswordGenerator(unittest.TestCase):

    def setUp(self):
        self.pattern = "/C/c/d/e/?/@/&"
        self.generator = PasswordGenerator(self.pattern)

    def test_generate_single(self):
        password = self.generator.generate_single()
        self.assertEqual(len(password), 7)
        self.assertRegex(password[0], r'[A-Z]')
        self.assertRegex(password[1], r'[a-z]')
        self.assertRegex(password[2], r'\d')
        self.assertRegex(password[3], r'[!@#$%^&*(),.?":{}|<>_\-+/;\[\]]')  # Escaping the dash and brackets
        self.assertRegex(password[4], r'[A-Za-z\d!@#$%^&*(),.?":{}|<>_\-+/;\[\]]')
        self.assertRegex(password[5], r'[A-Za-z]')
        self.assertRegex(password[6], r'[A-Za-z\d]')

    def test_generate_multiple(self):
        passwords = self.generator.generate_multiple(100)
        self.assertEqual(len(passwords), 100)
        for password in passwords:
            self.assertEqual(len(password), 7)

    def test_calculate_combinations(self):
        combinations = self.generator.calculate_combinations()
        expected_combinations = (len(string.ascii_uppercase) * len(string.ascii_lowercase) * 
                                 len(string.digits) * len("!@#$%^&*(),.?\":{}|<>_-+/;[]") * 
                                 len(string.ascii_letters + string.digits + "!@#$%^&*(),.?\":{}|<>_-+/;[]") *
                                 len(string.ascii_uppercase + string.ascii_lowercase) *
                                 len(string.ascii_uppercase + string.ascii_lowercase + string.digits))
        self.assertEqual(combinations, expected_combinations)

    def test_no_duplicates_in_file(self):
        filename = 'test_passwords.txt'
        patterns = "/C/c/d/e/?/@/&"
        generator = PasswordGenerator(patterns)
        passwords = generator.generate_multiple(100)
        with open(filename, 'w') as f:
            for password in passwords:
                f.write(password + '\n')

        with open(filename, 'r') as f:
            lines = f.readlines()

        os.remove(filename)  # Clean up test file

        self.assertEqual(len(lines), len(set(lines)))

if __name__ == '__main__':
    unittest.main()
