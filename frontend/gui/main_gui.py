# frontend/gui/main_gui.py

import tkinter as tk
from tkinter import messagebox
from core.carbon_engine.carbon_calculator import CarbonCalculator

carbon_tracker = CarbonCalculator()

class StarSonPOSApp:
    def __init__(self, master):
        self.master = master
        master.title("StarSon POS - Eco Receipt")
        master.geometry("400x420")
        self.items = []

        # Title
        tk.Label(master, text="StarSon POS", font=("Helvetica", 18, "bold")).pack(pady=10)

        # Item entry
        self.item_entry = tk.Entry(master)
        self.item_entry.pack()
        tk.Button(master, text="Add Item", command=self.add_item).pack(pady=5)

        # SMS and Email Checkboxes
        self.send_sms = tk.IntVar()
        self.send_email = tk.IntVar()
        tk.Checkbutton(master, text="Send SMS", variable=self.send_sms).pack()
        tk.Checkbutton(master, text="Send Email", variable=self.send_email).pack()

        # Secondary recipient options
        self.sms2_label = tk.Label(master, text="Second SMS Recipient (optional):")
        self.sms2_entry = tk.Entry(master)
        self.email2_label = tk.Label(master, text="Second Email Recipient (optional):")
        self.email2_entry = tk.Entry(master)

        self.send_sms.trace("w", self.toggle_sms2)
        self.send_email.trace("w", self.toggle_email2)

        # Finalize button
        tk.Button(master, text="Finalize Purchase", command=self.finalize_purchase).pack(pady=20)

        # Summary label
        self.summary = tk.Label(master, text="", fg="green")
        self.summary.pack()

    def toggle_sms2(self, *args):
        if self.send_sms.get():
            self.sms2_label.pack()
            self.sms2_entry.pack()
        else:
            self.sms2_label.pack_forget()
            self.sms2_entry.pack_forget()

    def toggle_email2(self, *args):
        if self.send_email.get():
            self.email2_label.pack()
            self.email2_entry.pack()
        else:
            self.email2_label.pack_forget()
            self.email2_entry.pack_forget()

    def add_item(self):
        item = self.item_entry.get()
        if item:
            self.items.append(item)
            self.item_entry.delete(0, tk.END)
            messagebox.showinfo("Item Added", f"{item} added.")
        else:
            messagebox.showwarning("Input Error", "Please enter an item.")

    def finalize_purchase(self):
        if not self.items:
            messagebox.showwarning("Empty", "No items added.")
            return

        carbon_tracker.record_digital_receipt()
        summary = carbon_tracker.get_summary()

        receipt = f"Items: {', '.join(self.items)}\n"
        receipt += f"Trees Saved: {summary['trees_saved']}\n"
        receipt += f"Carbon Credits: {summary['carbon_credits']}\n"

        if self.send_sms.get():
            receipt += "Receipt sent via SMS.\n"
        if self.send_email.get():
            receipt += "Receipt sent via Email.\n"

        self.summary.config(text=receipt)
        self.items.clear()

if __name__ == "__main__":
    root = tk.Tk()
    app = StarSonPOSApp(root)
    root.mainloop()
