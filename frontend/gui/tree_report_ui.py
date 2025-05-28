import tkinter as tk
from tkinter import messagebox
from tree_saver import TreeSaver

class TreeReportApp:
    def __init__(self, root):
        self.root = root
        self.root.title("StarSon POS - Trees Saved")
        self.treesaver = TreeSaver()

        self.current_theme = "light"
        self.themes = {
            "light": {"bg": "#f0f0f0", "fg": "#000"},
            "dark": {"bg": "#2c2c2c", "fg": "#fff"}
        }

        self.root.geometry("300x250")
        self.root.resizable(False, False)

        self.label = tk.Label(root, text="", font=("Arial", 14))
        self.label.pack(pady=10)

        self.entry_label = tk.Label(root, text="Receipts Avoided:", font=("Arial", 10))
        self.entry_label.pack()

        self.entry = tk.Entry(root)
        self.entry.insert(0, str(self.treesaver.receipts_avoided))  # default value
        self.entry.pack(pady=5)

        self.update_button = tk.Button(root, text="Update Trees Saved", command=self.update_trees)
        self.update_button.pack(pady=5)

        self.toggle_button = tk.Button(root, text="Switch Theme", command=self.toggle_theme)
        self.toggle_button.pack(pady=10)

        self.refresh_label()
        self.apply_theme()

    def toggle_theme(self):
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self.apply_theme()

    def apply_theme(self):
        theme = self.themes[self.current_theme]
        self.root.configure(bg=theme["bg"])
        widgets = [self.label, self.entry_label, self.entry, self.update_button, self.toggle_button]
        for widget in widgets:
            widget.configure(bg=theme["bg"], fg=theme["fg"])

    def refresh_label(self):
        trees_saved = self.treesaver.calculate_trees_saved()
        self.label.config(text=f"Trees Saved: {trees_saved:.4f}")

    def update_trees(self):
       try:
    new_value = int(self.entry.get())
    if new_value < 0:
        raise ValueError

    # Simulate batch logging
    current_ids = self.treesaver.digital_receipts
    new_ids = {f"SIMULATED_{i}" for i in range(len(current_ids), new_value)}
    for rid in new_ids:
        self.treesaver.log_receipt(rid, 'sms')  # Assuming 'sms' method for simplicity

    self.refresh_label()
except ValueError:
    messagebox.showerror("Input Error", "Please enter a valid non-negative number.")


if __name__ == "__main__":
    root = tk.Tk()
    app = TreeReportApp(root)
    root.mainloop()

