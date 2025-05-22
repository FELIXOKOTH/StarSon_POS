from utils.pdf_generator import generate_pdf_receipt
from utils.email_dispatcher import send_email_with_pdf

def on_receipt_generated(receipt_data, customer_email):
    pdf_file = generate_pdf_receipt(receipt_data)
    send_email_with_pdf(to_email=customer_email, pdf_file=pdf_file)
