from reportlab.lib.pagesize import letter
from reportlab.pdfgen import canvas
import os

def generate_pdf_receipt(receipt_id, amount, customer_name):
  file_path = f"static/receipts_{receipt_id}.pdf"
  c = canvas.Canvas(file_path, pagesize=letter)
  c.drawString(100, 750, f"Receipt ID: {receipt_id}")
  c.drawString(100, 730, f"Customer: {customer_name}")
  c.drawString(100, 710, f"Amount: KES{amount}")
  c.drawString(100, 690, "Thank you for using StarSon POS")
  c.save()
  return file_path
