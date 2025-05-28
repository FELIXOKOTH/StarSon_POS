# backend/admin/admin_panel.py

import tkinter as tk
from tkinter import ttk
import random  # This is just for simulation

class AdminPanel:
    def __init__(self, master):
        self.master = master
        master.title("Admin Control Panel")
        master.geometry("600x400")

        self.tree = ttk.Treeview(master)
        self.tree['columns'] = ('ID', 'Item', 'Amount', 'Carbon Saved')

        self.tree.column('#0', width=0, stretch=tk.NO)
        self.tree.column('ID', anchor=tk.W, width=100)
        self.tree.column('Item', anchor=tk.W, width=200)
        self.tree.column('Amount', anchor=tk.W, width=100)
        self.tree.column('Carbon Saved', anchor=tk.W, width=120)

        self.tree.heading('#0', text='', anchor=tk.W)
        self.tree.heading('ID', text='Transaction ID', anchor=tk.W)
        self.tree.heading('Item', text='Item', anchor=tk.W)
        self.tree.heading('Amount', text='Amount', anchor=tk.W)
        self.tree.heading('Carbon Saved', text='Carbon Saved (kg)', anchor=tk.W)

        self.tree.pack(pady=20)

        # Generate random data for the table (simulating transactions)
        for i in range(10):
            self.tree.insert('', 'end', values=(f"T{i+1}", f"Item {i+1}", f"${random.randint(10, 100)}", f"{random.randint(1, 10)}"))

if __name__ == "__main__":
    root = tk.Tk()
    admin_panel = AdminPanel(root)
    root.mainloop()
