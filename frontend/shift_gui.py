import tkinter as tk
from tkinter import messagebox
import shift_manager  # This assumes shift_manager.py is in the same directory

class ShiftApp:
    def __init__(self, root):
        self.root = root
        self.root.title("StarSon POS | Shift Panel")
        self.cashier_id = tk.StringVar()

        tk.Label(root, text="Cashier ID:").pack(pady=5)
        tk.Entry(root, textvariable=self.cashier_id).pack(pady=5)

        tk.Button(root, text="Start Shift", command=self.start_shift).pack(pady=5)
        tk.Button(root, text="Start Break", command=self.break_shift).pack(pady=5)
        tk.Button(root, text="End Break", command=self.resume_shift).pack(pady=5)
        tk.Button(root, text="End Shift", command=self.end_shift).pack(pady=5)
        tk.Button(root, text="Shift Report", command=self.report).pack(pady=5)

    def start_shift(self):
        shift_manager.start_shift(self.cashier_id.get())
        messagebox.showinfo("Shift Started", "Shift started successfully.")

    def break_shift(self):
        shift_manager.break_shift(self.cashier_id.get())
        messagebox.showinfo("Break Started", "Break started.")

    def resume_shift(self):
        shift_manager.resume_shift(self.cashier_id.get())
        messagebox.showinfo("Break Ended", "Break ended.")

    def end_shift(self):
        try:
            sales_total = float(input("Enter total sales amount: "))
            shift_manager.end_shift(self.cashier_id.get(), sales_total)
            messagebox.showinfo("Shift Ended", "Shift ended and logged.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")

    def report(self):
        shift_manager.get_shift_report()

if __name__ == "__main__":
    root = tk.Tk()
    app = ShiftApp(root)
    root.mainloop()
