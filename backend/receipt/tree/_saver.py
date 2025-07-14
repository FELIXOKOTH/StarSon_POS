import os
from datetime import datetime

class TreeSaver:
    def __init__(self, log_dir="logs"):
        os.makedirs(log_dir, exist_ok=True)
        self.log_file = os.path.join(log_dir, "receipt_log.txt")

    def log_receipt(self, receipt_id, method="pdf"):
        with open(self.log_file, "a") as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"{timestamp}, Receipt ID: {receipt_id}, Method: {method}\n")
