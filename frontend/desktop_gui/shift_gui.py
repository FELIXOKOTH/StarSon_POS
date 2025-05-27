import tkinter as tk
from tkinter import messagebox
import shift_manager
from utils.language_switcher import LanguageSwitcher

class ShiftApp:
    def __init__(self, root):
        self.root = root
        self.root.title("StarSon POS | Shift Panel")
        self.cashier_id = tk.StringVar()
        self.language = LanguageSwitcher("en")

        self.build_ui()

    def build_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text=self.language.get("select_language")).pack()
        lang_option = tk.StringVar(value="en")
        lang_menu = tk.OptionMenu(self.root, lang_option, "en", "sw", command=self.change_language)
        lang_menu.pack(pady=5)

        tk.Label(self.root, text=self.language.get("cashier_id")).pack(pady=5)
        tk.Entry(self.root, textvariable=self.cashier_id).pack(pady=5)

        tk.Button(self.root, text=self.language.get("start_shift"), command=self.start_shift).pack(pady=5)
        tk.Button(self.root, text=self.language.get("break_shift"), command=self.break_shift).pack(pady=5)
        tk.Button(self.root, text=self.language.get("end_break"), command=self.resume_shift).pack(pady=5)
        tk.Button(self.root, text=self.language.get("end_shift"), command=self.end_shift).pack(pady=5)
        tk.Button(self.root, text=self.language.get("report"), command=self.report).pack(pady=5)

    def change_language(self, lang_code):
        self.language.set_language(lang_code)
        self.build_ui()

    def start_shift(self):
        shift_manager.start_shift(self.cashier_id.get())
        messagebox.showinfo("Info", "Shift started successfully.")

    def break_shift(self):
        shift_manager.break_shift(self.cashier_id.get())
        messagebox.showinfo("Info", "Break started.")

    def resume_shift(self):
        shift_manager.resume_shift(self.cashier_id.get())
        messagebox.showinfo("Info", "Break ended.")

    def end_shift(self):
        try:
            sales_total = float(input("Enter total sales amount: "))
            shift_manager.end_shift(self.cashier_id.get(), sales_total)
            messagebox.showinfo("Info", "Shift ended.")
        except ValueError:
            messagebox.showerror("Error", "Enter valid number.")

    def report(self):
        shift_manager.get_shift_report()

if __name__ == "__main__":
    root = tk.Tk()
    app = ShiftApp(root)
    root.mainloop()

