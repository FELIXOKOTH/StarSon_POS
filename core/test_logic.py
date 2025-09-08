import unittest
from core.logic import calculate_total

class TestLogic(unittest.TestCase):

    def test_calculate_total(self):
        items = [{'price': 10}, {'price': 20}, {'price': 30}]
        self.assertEqual(calculate_total(items), 60)

if __name__ == '__main__':
    unittest.main()
