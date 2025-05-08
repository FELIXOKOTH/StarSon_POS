import sqlite3
from datetime import datetime

# Database setup
conn = sqlite3.connect('starson_pos.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS shifts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cashier_id TEXT,
    shift_start TEXT,
    shift_end TEXT,
    break_start TEXT,
    break_end TEXT,
    sales_total REAL DEFAULT 0.0
)
''')
conn.commit()

# Functions to handle shifts
def start_shift(cashier_id):
    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("INSERT INTO shifts (cashier_id, shift_start) VALUES (?, ?)", (cashier_id, start_time))
    conn.commit()
    print(f"Shift started for {cashier_id} at {start_time}")

def break_shift(cashier_id):
    break_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("UPDATE shifts SET break_start = ? WHERE cashier_id = ? AND shift_end IS NULL", (break_time, cashier_id))
    conn.commit()
    print(f"Break started for {cashier_id} at {break_time}")

def resume_shift(cashier_id):
    resume_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("UPDATE shifts SET break_end = ? WHERE cashier_id = ? AND shift_end IS NULL", (resume_time, cashier_id))
    conn.commit()
    print(f"Break ended for {cashier_id} at {resume_time}")

def end_shift(cashier_id, sales_total):
    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("UPDATE shifts SET shift_end = ?, sales_total = ? WHERE cashier_id = ? AND shift_end IS NULL", (end_time, sales_total, cashier_id))
    conn.commit()
    print(f"Shift ended for {cashier_id} at {end_time}")

def get_shift_report():
    cursor.execute("SELECT * FROM shifts ORDER BY id DESC")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

# Example usage (Uncomment to test)
# start_shift("cashier001")
# break_shift("cashier001")
# resume_shift("cashier001")
# end_shift("cashier001", 3500.00)
# get_shift_report()
