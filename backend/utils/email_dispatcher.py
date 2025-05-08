import smtplib
from email.message import EmailMessage
import os

def send_email_with_pdf(to_email, pdf_file):
    msg = EmailMessage()
    msg['Subject'] = 'Your StarSon POS Receipt'
    msg['From'] = os.getenv("EMAIL_USER")
    msg['To'] = to_email
    msg.set_content('Attached is your PDF receipt. Thank you for shopping with StarSon POS.')

    with open(pdf_file, 'rb') as f:
        file_data = f.read()
        msg.add_attachment(file_data, maintype='application', subtype='pdf', filename=os.path.basename(pdf_file))

    with smtplib.SMTP_SSL('smtp.example.com', 465) as smtp:
        smtp.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASS"))
        smtp.send_message(msg)
