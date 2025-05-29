
import sqlite3
import bcrypt

conn = sqlite3.connect('starson_pos.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
''')

plain_password = 'YourLegacy1994'
hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt())

try:
    cursor.execute('''
        INSERT INTO users (username, password, role)
        VALUES (?, ?, ?)
    ''', ('admin', hashed_password, 'admin'))
    conn.commit()
    print("Admin user created successfully.")
except sqlite3.IntegrityError:
    print("Admin user already exists.")

conn.close()
