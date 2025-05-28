"""
secure_setup.py
Security configuration for StarSon POS frontend.
Handles encryption, API key management, integrity checks, and environment setup.
"""

import os
import hashlib
import base64
from cryptography.fernet import Fernet

# 1. Generate or Load Encryption Key
def load_or_create_key(key_file="secure/secret.key"):
    if not os.path.exists(key_file):
        os.makedirs(os.path.dirname(key_file), exist_ok=True)
        key = Fernet.generate_key()
        with open(key_file, 'wb') as f:
            f.write(key)
        print("[✓] Encryption key created.")
    else:
        with open(key_file, 'rb') as f:
            key = f.read()
        print("[✓] Encryption key loaded.")
    return key

# 2. Initialize Fernet Encryption
def get_cipher():
    key = load_or_create_key()
    return Fernet(key)

# 3. Encrypt sensitive data
def encrypt_data(data: str) -> str:
    cipher = get_cipher()
    encrypted = cipher.encrypt(data.encode())
    return encrypted.decode()

# 4. Decrypt sensitive data
def decrypt_data(token: str) -> str:
    cipher = get_cipher()
    decrypted = cipher.decrypt(token.encode())
    return decrypted.decode()

# 5. File Integrity Check (e.g. for critical scripts)
def generate_file_hash(filepath: str) -> str:
    with open(filepath, "rb") as f:
        file_data = f.read()
    return hashlib.sha256(file_data).hexdigest()

def verify_file_integrity(filepath: str, expected_hash: str) -> bool:
    return generate_file_hash(filepath) == expected_hash

# 6. API Key Handling
def store_api_key(api_key: str, path="secure/api.key"):
    encrypted = encrypt_data(api_key)
    with open(path, "w") as f:
        f.write(encrypted)
    print("[✓] API key stored securely.")

def load_api_key(path="secure/api.key") -> str:
    if not os.path.exists(path):
        raise FileNotFoundError("API key file not found.")
    with open(path, "r") as f:
        encrypted_key = f.read()
    return decrypt_data(encrypted_key)

# Run test if needed
if __name__ == "__main__":
    test_secret = "example@123"
    encrypted = encrypt_data(test_secret)
    decrypted = decrypt_data(encrypted)
    print("Original:", test_secret)
    print("Encrypted:", encrypted)
    print("Decrypted:", decrypted)
