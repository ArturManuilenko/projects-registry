import unittest


class ApplicationTestCase(unittest.TestCase):
    def test_division(self) -> None:
        assert 3 == 9 / 3, "invalid division"
