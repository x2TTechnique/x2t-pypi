import unittest
from x2t.exception import ErrorHandler


class TestError(unittest.TestCase):

    def test_error_exception(self):
        with self.assertRaises(ZeroDivisionError):
            self.raise_exception_division()
            self.raise_exception_combine_types()

    @ErrorHandler.exception(log=False)
    def raise_exception_division(self):
        return 1 / 0

    @ErrorHandler.exception(log=False)
    def raise_exception_combine_types(self):
        return "a" + True


if __name__ == '__main__':
    unittest.main()
