import tkinter as tk
from tkinter import messagebox

def submit_consent():
    if consent_var.get():
        # Save consent record (pseudo code below)
        save_user_consent(customer_name.get())
        messagebox.showinfo("Consent", "Thank you for accepting our data policy.")
    else:
        messagebox.showwarning("Consent Required", "You must accept the data policy to proceed.")

def save_user_consent(name):
    with open("user_consent_log.txt", "a") as file:
        file.write(f"{name} accepted on: {datetime.datetime.now()}\n")

import datetime
root = tk.Tk()
root.title("StarSon POS - Customer Onboarding")

tk.Label(root, text="Customer Name").pack()
customer_name = tk.Entry(root)
customer_name.pack()

consent_var = tk.BooleanVar()
consent_checkbox = tk.Checkbutton(
    root,
    text="I agree to the Data Privacy Policy and consent to the use of my information for POS operations.",
    variable=consent_var
)
consent_checkbox.pack(pady=10)

tk.Button(root, text="Continue", command=submit_consent).pack()

root.mainloop()
