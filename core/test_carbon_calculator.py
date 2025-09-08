import unittest
from core.carbon_calculator import CarbonCalculator

class TestCarbonCalculator(unittest.TestCase):

    def test_carbon_calculator(self):
        calculator = CarbonCalculator()
        calculator.record_digital_receipt()
        self.assertEqual(calculator.paper_saved, 1)
        self.assertEqual(calculator.calculate_tree_savings(), 0.0001)
        self.assertEqual(calculator.calculate_carbon_credits(), 0.000059)

if __name__ == '__main__':
    unittest.main()
