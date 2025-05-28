from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
from datetime import datetime

def generate_pdf_receipt(receipt_data, customer_name, output_dir="receipts"):
    """
    Generates a PDF receipt using ReportLab and saves it locally.

    Args:
        receipt_data (dict): Data containing items and total.
        customer_name (str): Customer's name for receipt header.
        output_dir (str): Directory to save PDF receipts.

    Returns:
        str: Path to the generated PDF file.
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"receipt_{customer_name.replace(' ', '_')}_{timestamp}.pdf"
    file_path = os.path.join(output_dir, filename)

    # Start building PDF
    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4
    y = height - 50

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "StarSon POS - Digital Receipt")
    y -= 20
    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"Customer: {customer_name}")
    y -= 15
    c.drawString(50, y, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    y -= 30

    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "Item")
    c.drawString(250, y, "Quantity")
    c.drawString(350, y, "Price")
    y -= 15

    c.setFont("Helvetica", 10)
    for item in receipt_data["items"]:
        c.drawString(50, y, item["name"])
        c.drawString(250, y, str(item["qty"]))
        c.drawString(350, y, f"KES {item['price']}")
        y -= 15
        if y < 100:
            c.showPage()
            y = height - 50

    y -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, f"Total: KES {receipt_data['total']}")
    y -= 30
    c.setFont("Helvetica-Oblique", 8)
    c.drawString(50, y, "Thank you for choosing StarSon POS. Save trees. Go digital.")

    c.save()
    return file_path
