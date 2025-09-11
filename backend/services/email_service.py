# backend/services/email_service.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- CORRECTLY CONFIGURED EMAIL SETTINGS ---
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USER = "okotieya404@gmail.com"  # Your Gmail address
EMAIL_PASSWORD = "jxrl zswf rmad dhyb"  # Your Gmail App Password

def send_setup_email(recipient_email, setup_link):
    """
    Sends an email to a new user with their account setup link.
    """
    # This check is now correctly structured
    if EMAIL_USER == "your_email@gmail.com" or EMAIL_PASSWORD == "your_app_password":
        print("--- EMAIL SENDING IS NOT CONFIGURED ---")
        print("This is a fallback message. The system is using placeholder credentials.")
        print(f"Recipient: {recipient_email}")
        print(f"Setup Link: {setup_link}")
        return

    try:
        # Create the email message
        message = MIMEMultipart("alternative")
        message["Subject"] = "Set Up Your Account"
        message["From"] = EMAIL_USER
        message["To"] = recipient_email

        text = f"""Hi,\n\nWelcome! Please set up your account by clicking the following link:\n{setup_link}\n\nThanks,"""

        html = f"""\
        <html>
            <body>
                <p>Hi,<br><br>
                Welcome! Please set up your account by clicking the link below:<br>
                <a href=\"{setup_link}\">Set Up Your Account</a><br><br>
                Thanks!
                </p>
            </body>
        </html>
        """

        # Attach both plain text and HTML versions
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        message.attach(part1)
        message.attach(part2)

        # Send the email
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()  # Secure the connection
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_USER, recipient_email, message.as_string())
        
        print(f"Setup email sent successfully to {recipient_email}")

    except Exception as e:
        print(f"Failed to send email: {e}")
