
import os
import json
import base64
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

TOKEN_FILE_PATH = "backend/token.txt"
ENCRYPTED_PROVIDER_FILE = "backend/providers.enc"
EXPECTED_TOKEN = os.getenv("SECURE_TOKEN")

def read_token_from_file():
    if os.path.exists(TOKEN_FILE_PATH):
        with open(TOKEN_FILE_PATH, 'r') as file:
            return file.read().strip()
    return None

fernet_key = Fernet.generate_key()
cipher = Fernet(fernet_key)

def encrypt_providers():
    provider_map = {
        "safaricom": "safaricom_gateway",
        "airtel": "airtel_gateway",
        "telkom": "telkom_gateway",
        "gmail": "smtp.gmail.com",
        "yahoo": "smtp.mail.yahoo.com"
    }
    encrypted = cipher.encrypt(json.dumps(provider_map).encode())
    with open(ENCRYPTED_PROVIDER_FILE, 'wb') as file:
        file.write(encrypted)
    print("Provider configuration encrypted and saved.")

def get_provider(customer_input):
    token_file = read_token_from_file()
    if token_file != EXPECTED_TOKEN:
        raise PermissionError("Invalid secure token. Access denied.")

    with open(ENCRYPTED_PROVIDER_FILE, 'rb') as file:
        encrypted_data = file.read()
    decrypted_data = cipher.decrypt(encrypted_data)
    provider_map = json.loads(decrypted_data.decode())

    input_lower = customer_input.lower()
    for key in provider_map:
        if key in input_lower:
            return provider_map[key]

    return "default_gateway"

if __name__ == "__main__":
    try:
        user_input = input("Enter customer contact (e.g., 0722... or email): ")
        selected = get_provider(user_input)
        print(f"Selected provider: {selected}")
    except Exception as e:
        print(f"Access Error: {e}")
