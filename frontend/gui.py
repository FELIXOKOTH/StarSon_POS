import tkinter as tk
from tkinter import messagebox
from backend.auth import authenticate_user

def show_dashboard(role):
    window = tk.Tk()
    window.title("StarSon POS - Dashboard")
    label = tk.Label(window, text=f"Welcome to StarSon POS ({role.title()} Access)", font=("Arial", 14))
    label.pack()

    if role == "admin":
        tk.Button(window, text="View Reports").pack()
        tk.Button(window, text="Manage Users").pack()
    elif role == "cashier":
        tk.Button(window, text="Process Sale").pack()
    elif role == "manager":
        tk.Button(window, text="Inventory Reports").pack()
    else:
        tk.Label(window, text="Access Denied").pack()

    window.mainloop()

def login():
    def attempt():
        user = authenticate_user(entry_username.get(), entry_password.get())
        if user:
            login_window.destroy()
            show_dashboard(user["role"])
        else:
            messagebox.showerror("Error", "Invalid credentials")

    login_window = tk.Tk()
    login_window.title("StarSon POS - Login")

    tk.Label(login_window, text="Username").pack()
    entry_username = tk.Entry(login_window)
    entry_username.pack()

    tk.Label(login_window, text="Password").pack()
    entry_password = tk.Entry(login_window, show="*")
    entry_password.pack()

    tk.Button(login_window, text="Login", command=attempt).pack()
    login_window.mainloop()

if __name__ == "__main__":
    login()
