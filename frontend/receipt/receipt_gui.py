import tkinter as tk
from tkinter import messagebox
from receipt_generator import generate_pdf_receipt

class ReceiptGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("StarSon POS - Receipt Generator")
        self.root.geometry("400x400")

        self.items = []

        tk.Label(root, text="Customer Name").pack()
        self.name_entry = tk.Entry(root)
        self.name_entry.pack()

        tk.Label(root, text="Item Name").pack()
        self.item_entry = tk.Entry(root)
        self.item_entry.pack()

        tk.Label(root, text="Quantity").pack()
        self.qty_entry = tk.Entry(root)
        self.qty_entry.pack()

        tk.Label(root, text="Price (KES)").pack()
        self.price_entry = tk.Entry(root)
        self.price_entry.pack()

        tk.Button(root, text="Add Item", command=self.add_item).pack(pady=5)

        tk.Label(root, text="Payment Method").pack()
        self.payment_method = tk.StringVar(value="cash")
        methods = ["cash", "mpesa", "card", "credit", "mixed"]
        for method in methods:
            tk.Radiobutton(root, text=method.capitalize(), variable=self.payment_method, value=method).pack(anchor="w")

        tk.Button(root, text="Generate Receipt", command=self.generate_receipt).pack(pady=10)

        self.items_display = tk.Text(root, height=6)
        self.items_display.pack()

    def add_item(self):
        item_name = self.item_entry.get()
        qty = self.qty_entry.get()
        price = self.price_entry.get()

        if not item_name or not qty or not price:
            messagebox.showerror("Error", "Please fill all item fields.")
            return

        try:
            qty = int(qty)
            price = float(price)
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity or price.")
            return

        self.items.append({"name": item_name, "qty": qty, "price": price})
        self.items_display.insert(tk.END, f"{item_name} x{qty} @KES {price}\n")

        self.item_entry.delete(0, tk.END)
        self.qty_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)

    def generate_receipt(self):
        if not self.items:
            messagebox.showerror("Error", "No items added.")
            return

        customer_name = self.name_entry.get().strip()
        if not customer_name:
            messagebox.showerror("Error", "Enter customer name.")
            return

        total = sum(item["qty"] * item["price"] for item in self.items)

        receipt_data = {
            "items": self.items,
            "total": round(total, 2),
            "payment_method": self.payment_method.get()
        }

        pdf_path = generate_pdf_receipt(receipt_data, customer_name)

        messagebox.showinfo("Success", f"Receipt saved:\n{pdf_path}")
        self.reset_form()

    def reset_form(self):
        self.items.clear()
        self.items_display.delete("1.0", tk.END)
        self.name_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ReceiptGUI(root)
    root.mainloop()
