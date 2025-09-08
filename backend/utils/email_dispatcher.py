
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))

def send_email_receipt(to_email, customer_name, receipt_number, pdf_path):
    msg = EmailMessage()
    msg['Subject'] = f'StarSon POS Receipt #{receipt_number}'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email

    # HTML content
    html_content = f"""
    <html>
    <body>
        <div style="font-family: Arial, sans-serif; padding: 10px;">
            <h2 style="color: #2b7a78;">StarSon POS Receipt</h2>
            <p>Hello {customer_name},</p>
            <p>Thank you for your purchase. Please find your receipt attached as a PDF.</p>
            <p>Receipt No: <strong>{receipt_number}</strong></p>
            <p>For more, visit <a href="https://www.brightarm.co.ke">StarSon POS</a></p>
        </div>
    </body>
    </html>
    """
    msg.set_content("Your email client does not support HTML.")
    msg.add_alternative(html_content, subtype='html')

    # Attach PDF
    with open(pdf_path, 'rb') as f:
        msg.add_attachment(f.read(), maintype='application', subtype='pdf', filename=f'receipt_{receipt_number}.pdf')

    # Send email
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
