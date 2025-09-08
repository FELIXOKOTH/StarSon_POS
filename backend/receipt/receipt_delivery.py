
import os
from backend.utils.pdf_generator import generate_pdf_receipt
from backend.api.email_service import send_receipt_email
from backend.api.sms_service import send_sms_receipt
import qrcode

def generate_qr(receipt_path, qr_dir="qr_codes"):
    os.makedirs(qr_dir, exist_ok=True)
    filename = os.path.basename(receipt_path)
    download_url = f"https://yourdomain.com/receipts/{filename}"  # update with real hosting

    qr = qrcode.make(download_url)
    qr_path = os.path.join(qr_dir, f"{filename}.png")
    qr.save(qr_path)
    return qr_path, download_url

def generate_and_deliver(receipt_data, customer_name, email, phone):
    print("📄 Generating receipt PDF...")
    pdf_path = generate_pdf_receipt(receipt_data, customer_name)

    print("🔗 Generating QR code...")
    qr_path, receipt_url = generate_qr(pdf_path)

    print("📧 Sending Email...")
    send_receipt_email(email, customer_name, receipt_data['receipt_number'], pdf_path)

    print("📱 Sending SMS...")
    send_sms_receipt(phone, receipt_url)

    print(f"\n✅ Done. Receipt: {pdf_path} | QR: {qr_path}\n")
