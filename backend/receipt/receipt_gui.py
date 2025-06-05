import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from receipt_generator import generate_pdf_receipt
from tree_saver import TreeSaver

class ReceiptGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("StarSon POS - Receipt Generator")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        # TreeSaver instance
        self.treesaver = TreeSaver()

        # UI Elements
        tk.Label(root, text="Customer Name:", font=("Arial", 12)).pack(pady=5)
        self.entry_customer = tk.Entry(root, font=("Arial", 12))
        self.entry_customer.pack(pady=5)

        tk.Label(root, text="Payment Method:", font=("Arial", 12)).pack(pady=5)
        self.payment_method = tk.StringVar(value="Cash")
        tk.OptionMenu(root, self.payment_method, "Cash", "M-Pesa", "Card", "Bank Transfer").pack(pady=5)

        tk.Button(root, text="Generate Receipt", command=self.generate_receipt, font=("Arial", 12), bg="#4CAF50", fg="white").pack(pady=15)

    def generate_receipt(self):
        customer_name = self.entry_customer.get().strip()
        if not customer_name:
            messagebox.showwarning("Missing Info", "Please enter the customer's name.")
            return

        # Example cart data – in practice, retrieve from POS cart logic
        receipt_data = {
            "items": [
                {"name": "Milk", "qty": 2, "price": 100},
                {"name": "Bread", "qty": 1, "price": 50}
            ],
            "total": 250,
            "payment_method": self.payment_method.get()
        }

        try:
            pdf_path = generate_pdf_receipt(receipt_data, customer_name)

            # Log for tree tracking
            receipt_id = f"{customer_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            self.treesaver.log_receipt(receipt_id, method='pdf')

            messagebox.showinfo("Success", f"PDF Receipt saved:\n{pdf_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate receipt.\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ReceiptGUI(root)
    root.mainloop()
