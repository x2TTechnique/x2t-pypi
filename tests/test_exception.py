import unittest
from x2t.exception import handler


class TestError(unittest.TestCase):

    def test_error_exception(self):
        with self.assertRaises(ZeroDivisionError):
            self.raise_exception_division()
            self.raise_exception_combine_types()

    @handler(log=True, timing=True)
    def raise_exception_division(self):
        return 1 / 0

    @handler(log=True, timing=True)
    def raise_exception_combine_types(self):
        return "a" + True


if __name__ == '__main__':
    unittest.main()
