import os
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))

def send_email_with_pdf(to_email, pdf_path):
    msg = EmailMessage()
    msg['Subject'] = 'Your StarSon POS Receipt'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg.set_content("Attached is your receipt in PDF format.")

    with open(pdf_path, 'rb') as f:
        file_data = f.read()
        file_name = os.path.basename(pdf_path)
        msg.add_attachment(file_data, maintype='application', subtype='pdf', filename=file_name)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
