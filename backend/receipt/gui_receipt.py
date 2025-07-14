import tkinter as tk
from tkinter import messagebox
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import qrcode
import smtplib
from email.message import EmailMessage
import os
import datetime

# === Configurable Email Details ===
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_SENDER = 'your_email@gmail.com'
EMAIL_PASSWORD = 'your_password'  # Consider using environment variable

# === PDF and QR Generator ===
def generate_pdf_receipt(customer_name, items, total_amount, receipt_id):
    filename = f"receipt_{receipt_id}.pdf"
    c = canvas.Canvas(filename, pagesize=A4)
    c.setFont("Helvetica", 12)
    c.drawString(50, 800, f"StarSon POS Receipt - ID: {receipt_id}")
    c.drawString(50, 780, f"Customer: {customer_name}")
    c.drawString(50, 760, f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")

    y = 730
    for item in items:
        c.drawString(60, y, f"- {item}")
        y -= 20

    c.drawString(50, y - 10, f"Total: KES {total_amount}")
    c.save()
    return filename

def generate_qr_code(data, receipt_id):
    qr = qrcode.make(data)
    qr_filename = f"qr_receipt_{receipt_id}.png"
    qr.save(qr_filename)
    return qr_filename

# === Email Sender ===
def send_email_receipt(to_email, pdf_path):
    msg = EmailMessage()
    msg['Subject'] = 'Your StarSon POS Receipt'
    msg['From'] = EMAIL_SENDER
    msg['To'] = to_email
    msg.set_content('Find your receipt attached.')

    with open(pdf_path, 'rb') as f:
        msg.add_attachment(f.read(), maintype='application', subtype='pdf', filename=os.path.basename(pdf_path))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)

# === Placeholder for SMS (you will replace with API like Twilio, Africa's Talking, etc.) ===
def send_sms_receipt(phone_number, download_link):
    print(f"SMS to {phone_number}: Your receipt is ready: {download_link}")

# === GUI Application ===
def submit_transaction():
    name = entry_name.get()
    email = entry_email.get()
    phone = entry_phone.get()
    items = entry_items.get("1.0", tk.END).strip().split('\n')
    total = entry_total.get()

    if not (name and email and phone and items and total):
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    receipt_id = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    pdf_path = generate_pdf_receipt(name, items, total, receipt_id)
    qr_path = generate_qr_code(f"https://yourdomain.com/receipts/{os.path.basename(pdf_path)}", receipt_id)

    send_email_receipt(email, pdf_path)
    send_sms_receipt(phone, f"https://yourdomain.com/receipts/{os.path.basename(pdf_path)}")

    messagebox.showinfo("Success", f"Receipt sent via email & SMS.\nQR saved as: {qr_path}")

# === GUI Setup ===
root = tk.Tk()
root.title("StarSon POS - Receipt Generator")
root.geometry("400x500")

tk.Label(root, text="Customer Name").pack()
entry_name = tk.Entry(root, width=50)
entry_name.pack()

tk.Label(root, text="Email").pack()
entry_email = tk.Entry(root, width=50)
entry_email.pack()

tk.Label(root, text="Phone Number").pack()
entry_phone = tk.Entry(root, width=50)
entry_phone.pack()

tk.Label(root, text="Items (one per line)").pack()
entry_items = tk.Text(root, width=50, height=5)
entry_items.pack()

tk.Label(root, text="Total Amount (KES)").pack()
entry_total = tk.Entry(root, width=50)
entry_total.pack()

tk.Button(root, text="Generate & Send Receipt", command=submit_transaction, bg="#00aa66", fg="white").pack(pady=20)

root.mainloop()
