
from utils.sms_sender import send_sms

def dispatch_receipt_sms(phone_number, customer_name, receipt_id, download_url):
    """
    Send SMS to notify user that their receipt is ready with a link to download the PDF.
    """

    sms_message = f"""Hello {customer_name},

Thank you for shopping with us. Your receipt #{receipt_id} is ready.

You can download your full PDF receipt here:
{download_url}

- StarSon POS"""

    try:
        send_sms(phone_number, sms_message)
        print(f"SMS sent successfully to {phone_number}")
    except Exception as e:
        print(f"Failed to send SMS: {e}")
