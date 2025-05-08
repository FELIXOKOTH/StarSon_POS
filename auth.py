import json
import hashlib

def load_users(filepath="data/users.json"):
    with open(filepath, 'r') as file:
        return json.load(file)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(username, password):
    users = load_users()
    hashed = hash_password(password)
    user = next((u for u in users if u["username"] == username and u["password"] == hashed), None)
    return user