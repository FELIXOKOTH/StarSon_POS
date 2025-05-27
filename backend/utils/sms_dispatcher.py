import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

def send_sms_receipt(phone_number, receipt_id, total_amount, items_list, date):
    """
    Sends a readable receipt summary with a PDF link via SMS.
    """
    # Format item list as comma-separated
    items_str = ', '.join(items_list)

    # SMS body
    message_body = (
        f"StarSon POS Receipt\n"
        f"Tx: #{receipt_id} | Total: KES {total_amount}\n"
        f"Items: {items_str}\n"
        f"Date: {date}\n"
        f"PDF: https://donkaunda.com/receipts/{receipt_id}.pdf"
    )

    # Twilio credentials
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    twilio_number = os.getenv("TWILIO_PHONE_NUMBER")

    # Send the message
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=message_body,
        from_=twilio_number,
        to=phone_number
    )

    return message.sid
