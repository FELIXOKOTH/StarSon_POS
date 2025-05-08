from fpdf import FPDF
import os

def generate_pdf_receipt(receipt_data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for key, value in receipt_data.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)
    output_path = f"receipts/generated/receipt_{receipt_data['receipt_no']}.pdf"
    pdf.output(output_path)
    return output_path
