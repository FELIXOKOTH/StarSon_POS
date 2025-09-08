
from backend.utils.email_dispatcher import send_email_receipt

def send_receipt_email(to_email, customer_name, receipt_number, pdf_path):
    try:
        send_email_receipt(to_email, customer_name, receipt_number, pdf_path)
        return "Email sent successfully"
    except Exception as e:
        return f"Failed to send email: {e}"
