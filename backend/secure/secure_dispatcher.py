import os
from cryptography.fernet import Fernet # type: ignore
from dotenv import load_dotenv # type: ignore

load_dotenv()

#load Fernet key from environment
FERNET_KEY = os.getenv("FERNET_KEY")
cipher= Fernet(FERNET_KEY.encode())

#Token file path
TOKEN_FILE_PATH = os.path.join(os.path.dirname(__file__), "token.txt")

def load_token():
  if not os.path.exists(TOKEN_FILE_PATH):
    return none # type: ignore
  with open(TOKEN_FILE_PATH, "r") as f:
    encrypted_token=f.read()
  return cipher.decrypt(encrypted_token.encode()).decode()

def save_token(token_value):
  encrypted_token = cipher.encrypt(token_value.encode()).decode()
  with open(TOKEN_FILE_PATH, "w") as f:
    f.write(encrypted_token)
