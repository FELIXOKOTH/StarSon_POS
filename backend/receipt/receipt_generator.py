from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import qrcode
import os
from datetime import datetime
from io import BytesIO

def generate_pdf_receipt(receipt_data, customer_name, reference_url=None, output_dir="receipts"):
    """
    Generates a thermal-sized PDF receipt with QR code and eco-stats.

    Args:
        receipt_data (dict): Includes 'items' (list of dicts) and 'total'.
        customer_name (str): Name to appear on receipt.
        reference_url (str): Optional. URL to be encoded in QR code.
        output_dir (str): Folder where receipts will be saved.

    Returns:
        str: Full path to the generated receipt file.
    """
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = customer_name.replace(" ", "_")
    filename = f"receipt_{safe_name}_{timestamp}.pdf"
    filepath = os.path.join(output_dir, filename)

    # Define 80mm receipt width and height
    receipt_width = 80 * mm
    line_height = 15
    content_lines = len(receipt_data["items"]) + 10
    receipt_height = (content_lines * line_height) + 100  # points

    c = canvas.Canvas(filepath, pagesize=(receipt_width, receipt_height))
    y = receipt_height - 20

    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(receipt_width / 2, y, "StarSon POS - Eco Receipt")
    y -= 20

    c.setFont("Helvetica", 9)
    c.drawString(10, y, f"Customer: {customer_name}")
    y -= 12
    c.drawString(10, y, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    y -= 20

    c.setFont("Helvetica-Bold", 9)
    c.drawString(10, y, "Item")
    c.drawString(110, y, "Qty")
    c.drawString(150, y, "Price")
    y -= 15

    c.setFont("Helvetica", 9)
    for item in receipt_data["items"]:
        c.drawString(10, y, item["name"][:20])
        c.drawString(110, y, str(item["qty"]))
        c.drawString(150, y, f"KES {item['price']}")
        y -= 12

    y -= 10
    c.setFont("Helvetica-Bold", 10)
    c.drawString(10, y, f"Total: KES {receipt_data['total']}")
    y -= 20

    # 🌳 Tree-saving stats (estimate: 1 paper receipt = 0.00012 trees)
    trees_saved = round(len(receipt_data["items"]) * 0.00012, 5)
    c.setFont("Helvetica-Oblique", 8)
    c.drawCentredString(receipt_width / 2, y, f"🌱 You saved approximately {trees_saved} trees")
    y -= 10

    c.drawCentredString(receipt_width / 2, y, "Thank you for using StarSon POS")
    y -= 10
    c.drawCentredString(receipt_width / 2, y, "Save Trees 🌳 | Go Digital 🧾")
    y -= 30

    # 📱 Add QR code if URL is provided
    if reference_url:
        qr = qrcode.make(reference_url)
        buffer = BytesIO()
        qr.save(buffer)
        buffer.seek(0)
        qr_image = ImageReader(buffer)
        c.drawImage(qr_image, receipt_width / 2 - 40, y - 60, width=80, height=80)
        y -= 70
        c.setFont("Helvetica", 6)
        c.drawCentredString(receipt_width / 2, y, "Scan to view receipt online")

    c.save()
    return filepath
