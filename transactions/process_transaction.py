
import os
import argparse
from dotenv import load_dotenv

def process_cash_transaction(amount):
    """
    Processes a cash transaction.
    """
    print(f"Processing cash transaction of {amount}...")
    # Add your cash processing logic here
    print("Cash transaction processed successfully.")

def process_mpesa_transaction(amount, client_name):
    """
    Processes an M-Pesa transaction.
    """
    print(f"Processing M-Pesa transaction of {amount} for {client_name}...")
    
    # Load client-specific M-Pesa credentials from .env file
    client_env_path = os.path.join("clients", client_name, ".env")
    load_dotenv(dotenv_path=client_env_path)
    
    mpesa_type = os.getenv("MPESA_TYPE")
    mpesa_shortcode = os.getenv("MPESA_SHORTCODE")
    mpesa_key = os.getenv("MPESA_KEY")
    mpesa_secret = os.getenv("MPESA_SECRET")
    
    print(f"M-Pesa Type: {mpesa_type}")
    print(f"M-Pesa Shortcode: {mpesa_shortcode}")
    
    # Add your M-Pesa processing logic here
    print("M-Pesa transaction processed successfully.")

def process_card_transaction(amount):
    """
    Processes a card transaction.
    """
    print(f"Processing card transaction of {amount}...")
    # Add your card processing logic here
    print("Card transaction processed successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a payment transaction.")
    parser.add_argument("client_name", type=str, help="The name of the client.")
    parser.add_argument("amount", type=float, help="The transaction amount.")
    
    args = parser.parse_args()
    
    # Load the client's payment method from their .env file
    client_env_path = os.path.join("clients", args.client_name, ".env")
    load_dotenv(dotenv_path=client_env_path)
    
    payment_method = os.getenv("PAYMENT_METHOD")
    
    if payment_method == 'cash':
        process_cash_transaction(args.amount)
    elif payment_method == 'mpesa':
        process_mpesa_transaction(args.amount, args.client_name)
    elif payment_method == 'card':
        process_card_transaction(args.amount)
    else:
        print(f"Error: Invalid payment method '{payment_method}' for client '{args.client_name}'.")
