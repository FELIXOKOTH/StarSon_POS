import json
import os

RECEIPT_LOG_FILE = "receipt_log.json"
TREE_SAVED_RATIO = 8500  # Receipts per tree

def load_receipt_log():
    if not os.path.exists(RECEIPT_LOG_FILE):
        return set()
    with open(RECEIPT_LOG_FILE, "r") as f:
        return set(json.load(f))

def save_receipt_log(receipt_ids):
    with open(RECEIPT_LOG_FILE, "w") as f:
        json.dump(list(receipt_ids), f)

class TreeSaver:
    def __init__(self):
        self.digital_receipts = load_receipt_log()

    def log_receipt(self, receipt_id, method):
        if method in ['sms', 'email', 'both'] and receipt_id not in self.digital_receipts:
            self.digital_receipts.add(receipt_id)
            save_receipt_log(self.digital_receipts)

    def trees_saved(self):
        return round(len(self.digital_receipts) / TREE_SAVED_RATIO, 4)

    def total_digital_receipts(self):
        return len(self.digital_receipts)
