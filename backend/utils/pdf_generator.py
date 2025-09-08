
from reportlab.lib.pagesize import letter
from reportlab.pdfgen import canvas
import os

def generate_pdf(file_path, title, lines):
  c = canvas.Canvas(file_path, pagesize=letter)
  c.drawString(100, 750, title)
  y = 730
  for line in lines:
    c.drawString(100, y, line)
    y -= 20
  c.save()
  return file_path

def generate_receipt_pdf(receipt_id, amount, customer_name):
  file_path = f"static/receipts_{receipt_id}.pdf"
  title = f"Receipt ID: {receipt_id}"
  lines = [
      f"Customer: {customer_name}",
      f"Amount: KES{amount}",
      "Thank you for using StarSon POS"
  ]
  return generate_pdf(file_path, title, lines)

