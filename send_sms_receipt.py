"""
StarSon POS SMS + PDF Receipt Generator
Security Tips:
- Use HTTPS links for PDF download
- Generate temporary (expiring) URLs
- Obfuscate receipt IDs in URLs
"""

from fpdf import FPDF

# PDF generation function
def generate_pdf(receipt_data, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in receipt_data:
        pdf.cell(200, 10, txt=line, ln=True)
    pdf.output(filename)

# Simulate SMS content
receipt_url = "https://brightarm.co.ke/receipts/starson_receipt_abc123.pdf"
sms_message = f"""
Thank you for shopping with StarSon.
Total: KES 300
Download receipt: {receipt_url}
(Note: Link expires in 72 hours)
"""
print(sms_message)
