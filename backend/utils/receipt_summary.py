import datetime
import uuid
from utils.carbon_engine import CarbonEngine

# Initialize the carbon engine tracker
carbon_tracker = CarbonEngine()

def generate_receipt_summary(transaction_data):
    receipt_id = str(uuid.uuid4())
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Example structure of transaction_data:
    # {
    #   "items": [{"name": "Item A", "price": 100}, {"name": "Item B", "price": 50}],
    #   "total": 150,
    #   "payment_method": "M-PESA"
    # }

    items = transaction_data.get("items", [])
    total = transaction_data.get("total", 0)
    payment_method = transaction_data.get("payment_method", "Unknown")

    # Calculate tree savings
    trees_saved = carbon_tracker.log_receipt(1)

    summary = {
        "receipt_id": receipt_id,
        "timestamp": timestamp,
        "items": items,
        "total": total,
        "payment_method": payment_method,
        "trees_saved": trees_saved
    }

    log_receipt(summary)
    return summary

def log_receipt(summary):
    with open("logs/receipt_log.json", "a") as f:
        f.write(str(summary) + "\n")

# For direct testing
if __name__ == "__main__":
    sample_data = {
        "items": [
            {"name": "Green Coffee", "price": 300},
            {"name": "Eco Bag", "price": 150}
        ],
        "total": 450,
        "payment_method": "Card"
    }

    receipt = generate_receipt_summary(sample_data)
    print(receipt)
