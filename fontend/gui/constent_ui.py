import tkinter as tk
from tkinter import messagebox
import datetime
import os

LOG_FILE = "user_consent_log.txt"

def submit_consent():
    name = customer_name.get().strip()
    if not name:
        messagebox.showwarning("Input Required", "Please enter your name.")
        return

    if consent_var.get():
        save_user_consent(name)
        messagebox.showinfo("Consent", "Thank you for accepting our data policy.")
        root.destroy()
    else:
        messagebox.showwarning("Consent Required", "You must accept the data policy to proceed.")

def save_user_consent(name):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    record = f"{name} accepted on: {timestamp}\n"

    with open(LOG_FILE, "a") as file:
        file.write(record)

# UI Setup
root = tk.Tk()
root.title("StarSon POS - Customer Onboarding")
root.geometry("450x250")
root.configure(bg="white")

tk.Label(root, text="Customer Name", font=("Arial", 12), bg="white").pack(pady=5)
customer_name = tk.Entry(root, font=("Arial", 12), width=30)
customer_name.pack(pady=5)

consent_var = tk.BooleanVar()
tk.Checkbutton(
    root,
    text="I agree to the Data Privacy Policy and consent to the use of my information for POS operations.",
    variable=consent_var,
    wraplength=400,
    bg="white",
    font=("Arial", 10)
).pack(pady=10)

tk.Button(root, text="Continue", command=submit_consent, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=10)

root.mainloop()

