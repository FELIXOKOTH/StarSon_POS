# backend/security/security.py

import hashlib

def hash_password(password):
    """Hash the user's password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(stored_hash, password):
    """Check if the entered password matches the stored hash."""
    return stored_hash == hash_password(password)

# For login functionality
def login(username, password):
    # Simulating stored data (replace with database in real implementation)
    stored_username = "admin"
    stored_password_hash = hash_password("admin123")

    if username == stored_username and check_password(stored_password_hash, password):
        return True
    else:
        return False

# Example login check
if __name__ == "__main__":
    username = input("Enter username: ")
    password = input("Enter password: ")

    if login(username, password):
        print("Login successful.")
    else:
        print("Login failed.")
