
import json

def log_receipt(receipt_summary):
    with open("logs/receipt_log.json", "a") as f:
        f.write(json.dumps(receipt_summary) + "\n")
