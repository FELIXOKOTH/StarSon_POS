
import datetime
import uuid
from backend.utils.carbon_engine import generate_carbon_report
from backend.utils.logger import log_receipt

def generate_receipt_summary(transaction_data):
    receipt_id = str(uuid.uuid4())
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    items = transaction_data.get("items", [])
    total = transaction_data.get("total", 0)
    payment_method = transaction_data.get("payment_method", "Unknown")

    # Calculate tree savings
    carbon_report = generate_carbon_report(1)

    summary = {
        "receipt_id": receipt_id,
        "timestamp": timestamp,
        "items": items,
        "total": total,
        "payment_method": payment_method,
        "carbon_footprint": carbon_report
    }

    log_receipt(summary)
    return summary

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
