import re
import unittest


def check_string_re(test_string):
    """
    Подстрока начинается с левой скобки
    и продолжается до конца строки.
    """
    test_pattern = re.compile('\(+[(\w]*\Z')
    checked_string = re.sub(test_pattern, '', test_string)
    return checked_string


def check_string(test_string):
    """
    Левая скобка всегда левее правой.
    """
    while True:
        left_index = test_string.rfind('(')
        if left_index == -1:
            break
        right_index = test_string.rfind(')')
        if left_index > right_index:
            test_string = test_string[:left_index]
        else:
            break
    return test_string


class TestCheckString(unittest.TestCase):
    def test_check_string_re_1(self):
        self.assertEqual(check_string_re('esdfd((esdf)(esdf'), 'esdfd((esdf)')

    def test_check_string_re_2(self):
        self.assertEqual(check_string_re('esdfd((esdf)(esd)f'), 'esdfd((esdf)(esd)f')

    def test_check_string_re_3(self):
        self.assertEqual(check_string_re('esdfd))esdfe))sdf'), 'esdfd))esdfe))sdf')

    def test_check_string_re_4(self):
        self.assertEqual(check_string_re('esdfd((esdfe((sdf'), 'esdfd')

    def test_check_string_re_5(self):
        self.assertEqual(check_string_re(''), '')

    def test_check_string_1(self):
        self.assertEqual(check_string('esdfd((esdf)(esdf'), 'esdfd((esdf)')

    def test_check_string_2(self):
        self.assertEqual(check_string('esdfd((esdf)(esd)f'), 'esdfd((esdf)(esd)f')

    def test_check_string_3(self):
        self.assertEqual(check_string('esdfd))esdfe))sdf'), 'esdfd))esdfe))sdf')

    def test_check_string_4(self):
        self.assertEqual(check_string('esdfd((esdfe((sdf'), 'esdfd')

    def test_check_string_5(self):
        self.assertEqual(check_string(''), '')


if __name__ == '__main__':
    unittest.main(verbosity=2)
