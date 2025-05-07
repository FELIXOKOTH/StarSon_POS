# backend/api/receipt_handler.py
import datetime

class ReceiptHandler:
    def __init__(self, store_name):
        self.store_name = store_name

    def generate_receipt(self, items, total, customer, channels):
        now = datetime.datetime.now()
        receipt = {
            "store": self.store_name,
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M:%S"),
            "items": items,
            "total": total,
            "customer": customer,
            "channels": channels
        }
        return receipt

    def send_sms(self, phone, receipt):
        # Simulate sending SMS
        print(f"SMS sent to {phone}:\n{receipt}")

    def send_email(self, email, receipt):
        # Simulate sending email
        print(f"Email sent to {email}:\n{receipt}")

    def send_receipt(self, receipt, phone=None, email=None):
        if 'sms' in receipt['channels'] and phone:
            self.send_sms(phone, receipt)
        if 'email' in receipt['channels'] and email:
            self.send_email(email, receipt)
