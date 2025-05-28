
import sqlite3
import bcrypt
 
conn = sqlite3.connect('starson_pos.db')
cursor = conn.cursor()

def check_login(username_input, password_input):
    cursor.execute("SELECT password FROM users WHERE username = ?", (username_input,))
    user = cursor.fetchone()
    
    if user and bcrypt.checkpw(password_input.encode('utf-8'), user[0]):
        return "Login successful"
    return "Invalid credentials"

# Example usage:
# print(check_login('admin', 'YourLegacy1994'))
