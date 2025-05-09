
# StarSon POS Email Receipt Module

This module enables **automated email delivery of PDF-format receipts** for transactions conducted via StarSon POS. It is designed to operate in the **backend by default**, ensuring seamless receipt distribution to customers without user intervention.

## Key Features

- **Automated PDF generation** for every transaction.
- **Secure email delivery** using SMTP with environment variable configuration.
- **Default backend activation**, requiring no manual trigger.
- **Scalable** and ready for international deployment.
- **Data privacy and encryption** measures embedded for security compliance.

## Setup Guide

1. **Clone or upload this module** into your StarSon POS backend directory.
2. **Create a `.env` file** using the provided `.env.example` template.
3. Set your email service credentials and configurations:
   ```
   EMAIL_HOST=smtp.yourprovider.com
   EMAIL_PORT=587
   EMAIL_HOST_USER=your_email@example.com
   EMAIL_HOST_PASSWORD=your_email_password
   EMAIL_USE_TLS=True
   ```
4. **Ensure Python dependencies** are installed:
   ```bash
   pip install reportlab python-dotenv
   ```

## Usage

Once configured:
- Every time a receipt is generated at the frontend, the backend automatically sends a PDF copy to the customer's email.
- Optionally, SMS can be configured to contain a secure PDF download link.

## Security Tips

- Use **App Passwords** or **OAuth Tokens** instead of plain-text passwords where possible.
- Ensure `.env` is excluded from public repositories by adding it to `.gitignore`.
- Use email providers with rate-limiting and spam protection.

## Folder Structure

```
email_receipt/
├── send_email.py
├── generate_pdf.py
├── .env.example
└── README.md
```

## Author

**StarSon POS - BRIGHT_ARM ENTERPRISE**  
Website: [www.brightarm.co.ke](https://www.brightarm.co.ke)
