# core/security/auth.py
import hashlib

class AuthSystem:
    def __init__(self):
        self.users = {"admin": self._hash_password("StarSon@2025")}

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def validate_user(self, username, password):
        hashed = self._hash_password(password)
        return self.users.get(username) == hashed

    def add_user(self, username, password):
        self.users[username] = self._hash_password(password)
