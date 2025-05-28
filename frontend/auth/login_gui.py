import tkinter as tk
from tkinter import messagebox
from admin.admin_panel import check_login

def attempt_login():
    username = entry_username.get()
    password = entry_password.get()
    result = check_login(username, password)
    messagebox.showinfo("Login", result)

root = tk.Tk()
root.title("StarSon POS - Admin Login")

tk.Label(root, text="Username").pack()
entry_username = tk.Entry(root)
entry_username.pack()

tk.Label(root, text="Password").pack()
entry_password = tk.Entry(root, show="*")
entry_password.pack()

tk.Button(root, text="Login", command=attempt_login).pack()

root.mainloop()
