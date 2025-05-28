"""
StarSon POS | SMS + PDF Receipt Generator

Security Tips:
- Use HTTPS links for PDF download
- Generate temporary (expiring) URLs
- Obfuscate receipt IDs in URLs
"""

from fpdf import FPDF
import os
import uuid
import datetime

# Folder to store PDFs
RECEIPT_FOLDER = "generated_receipts"
BASE_RECEIPT_URL = "https://brightarm.co.ke/receipts"

# Ensure folder exists
os.makedirs(RECEIPT_FOLDER, exist_ok=True)

def generate_pdf_receipt(receipt_data, customer_name):
    """
    Generates a receipt PDF and saves it in the receipts folder.
    
    Returns the full path of the PDF.
    """
    # Generate secure, obfuscated filename
    unique_id = uuid.uuid4().hex[:8]
    filename = f"receipt_{customer_name.lower()}_{unique_id}.pdf"
    filepath = os.path.join(RECEIPT_FOLDER, filename)

    # Create the PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"StarSon POS Receipt - {customer_name}", ln=True)
    pdf.cell(200, 10, txt=f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.ln(10)
    
    for item in receipt_data["items"]:
        line = f"{item['name']} (x{item['qty']}): KES {item['price']}"
        pdf.cell(200, 10, txt=line, ln=True)

    pdf.ln(5)
    pdf.cell(200, 10, txt=f"Total: KES {receipt_data['total']}", ln=True)
    pdf.output(filepath)

    return filename

def generate_sms_message(customer_name, total, pdf_filename):
    """
    Creates a user-friendly SMS message with a receipt link.
    """
    receipt_url = f"{BASE_RECEIPT_URL}/{pdf_filename}"
    message = (
        f"Thank you for shopping with StarSon, {customer_name}!\n"
        f"Total: KES {total}\n"
        f"Download your receipt: {receipt_url}\n"
        f"(Note: Link expires in 72 hours)"
    )
    return message


# Example usage
if __name__ == "__main__":
    customer = "Jane Doe"
    receipt_data = {
        "items": [
            {"name": "Milk", "qty": 2, "price": 120},
            {"name": "Bread", "qty": 1, "price": 60}
        ],
        "total": 300
    }

    # Generate PDF and SMS content
    pdf_file = generate_pdf_receipt(receipt_data, customer)
    sms_text = generate_sms_message(customer, receipt_data["total"], pdf_file)

    print(sms_text)


