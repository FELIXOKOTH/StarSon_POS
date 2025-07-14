import os
from datetime import datetime
import qrcode
from email.message import EmailMessage
import smtplib
import shutil

from generate_pdf import generate_pdf_receipt  # Assuming your function is saved as generate_pdf.py

# ====== Configuration ======
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "youremail@example.com"
EMAIL_PASSWORD = "yourpassword"  # Better: use os.environ["EMAIL_PASSWORD"]

# ====== QR Code Generator ======
def generate_qr(receipt_path, qr_dir="qr_codes"):
    os.makedirs(qr_dir, exist_ok=True)
    filename = os.path.basename(receipt_path)
    download_url = f"https://yourdomain.com/receipts/{filename}"  # update with real hosting

    qr = qrcode.make(download_url)
    qr_path = os.path.join(qr_dir, f"{filename}.png")
    qr.save(qr_path)
    return qr_path, download_url

# ====== Email Sender ======
def send_email(to_email, pdf_path):
    msg = EmailMessage()
    msg["Subject"] = "Your StarSon POS Digital Receipt"
    msg["From"] = EMAIL_SENDER
    msg["To"] = to_email
    msg.set_content("Your receipt is attached. Thank you for using StarSon POS.")

    with open(pdf_path, "rb") as f:
        msg.add_attachment(f.read(), maintype="application", subtype="pdf", filename=os.path.basename(pdf_path))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)
    print(f"✅ Email sent to {to_email}")

# ====== SMS Placeholder ======
def send_sms(phone_number, receipt_link):
    print(f"📲 SMS sent to {phone_number}: Download your receipt here: {receipt_link}")
    # You can integrate Twilio / Africa's Talking here

# ====== Combine All ======
def generate_and_deliver(receipt_data, customer_name, email, phone):
    print("📄 Generating receipt PDF...")
    pdf_path = generate_pdf_receipt(receipt_data, customer_name)

    print("🔗 Generating QR code...")
    qr_path, receipt_url = generate_qr(pdf_path)

    print("📧 Sending Email...")
    send_email(email, pdf_path)

    print("📱 Sending SMS...")
    send_sms(phone, receipt_url)

    print(f"\n✅ Done. Receipt: {pdf_path} | QR: {qr_path}\n")
