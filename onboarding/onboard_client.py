
import os
import argparse

def create_client_env(client_name, payment_method='cash', mpesa_type=None, mpesa_shortcode=None, mpesa_key=None, mpesa_secret=None):
    """
    Creates a directory and a .env file for a new client with payment information.
    """
    client_dir = os.path.join("clients", client_name)
    os.makedirs(client_dir, exist_ok=True)

    env_content = f"""
# Client-specific environment variables for {client_name}
EMAIL_ADDRESS=
EMAIL_PASSWORD=
SMTP_SERVER=
SMTP_PORT=
SMS_API_KEY=
SMS_SENDER_ID=
KRA_API_KEY=

# Payment Configuration
PAYMENT_METHOD={payment_method}
"""

    if payment_method == 'mpesa':
        env_content += f"""
# M-Pesa Configuration
MPESA_TYPE={mpesa_type}
MPESA_SHORTCODE={mpesa_shortcode}
MPESA_KEY={mpesa_key}
MPESA_SECRET={mpesa_secret}
"""

    with open(os.path.join(client_dir, ".env"), "w") as f:
        f.write(env_content)

    print(f"Successfully created .env file for client: {client_name}")
    print(f"Payment method set to: {payment_method}")
    if payment_method == 'mpesa':
        print(f"M-Pesa type: {mpesa_type}")
        print(f"M-Pesa shortcode: {mpesa_shortcode}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Onboard a new client for StarSon POS.")
    parser.add_argument("client_name", type=str, help="The name of the client to onboard.")
    parser.add_argument("--payment-method", type=str, default="cash", choices=['cash', 'mpesa', 'card'], help="The default payment method for the client.")
    parser.add_argument("--mpesa-type", type=str, choices=['paybill', 'till', 'send_money', 'pochi'], help="The M-Pesa account type.")
    parser.add_argument("--mpesa-shortcode", type=str, help="The M-Pesa shortcode (Paybill or Till number).")
    parser.add_argument("--mpesa-key", type=str, help="The M-Pesa API key.")
    parser.add_argument("--mpesa-secret", type=str, help="The M-Pesa API secret.")

    args = parser.parse_args()

    create_client_env(
        args.client_name,
        payment_method=args.payment_method,
        mpesa_type=args.mpesa_type,
        mpesa_shortcode=args.mpesa_shortcode,
        mpesa_key=args.mpesa_key,
        mpesa_secret=args.mpesa_secret
    )
