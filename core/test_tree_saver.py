import unittest
import os
import json
from core.tree_saver import TreeSaver, RECEIPT_LOG_FILE

class TestTreeSaver(unittest.TestCase):

    def setUp(self):
        # Ensure the log file doesn't exist before a test
        if os.path.exists(RECEIPT_LOG_FILE):
            os.remove(RECEIPT_LOG_FILE)

    def tearDown(self):
        # Clean up the log file after a test
        if os.path.exists(RECEIPT_LOG_FILE):
            os.remove(RECEIPT_LOG_FILE)

    def test_tree_saver(self):
        saver = TreeSaver()
        self.assertEqual(saver.total_digital_receipts(), 0)
        self.assertEqual(saver.trees_saved(), 0)

        saver.log_receipt("receipt1", "email")
        self.assertEqual(saver.total_digital_receipts(), 1)
        self.assertEqual(saver.trees_saved(), 0.0001)

        # Test that logging the same receipt again doesn't change the count
        saver.log_receipt("receipt1", "email")
        self.assertEqual(saver.total_digital_receipts(), 1)
        self.assertEqual(saver.trees_saved(), 0.0001)

        saver.log_receipt("receipt2", "sms")
        self.assertEqual(saver.total_digital_receipts(), 2)
        self.assertEqual(saver.trees_saved(), 0.0002)

        # Test persistence
        saver2 = TreeSaver()
        self.assertEqual(saver2.total_digital_receipts(), 2)
        self.assertEqual(saver2.trees_saved(), 0.0002)


if __name__ == '__main__':
    unittest.main()
