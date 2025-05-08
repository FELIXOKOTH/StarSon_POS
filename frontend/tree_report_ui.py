import tkinter as tk
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

        self.root.geometry("300x200")
        self.root.resizable(False, False)

        self.label = tk.Label(root, text="", font=("Arial", 14))
        self.label.pack(pady=20)

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
        self.label.configure(bg=theme["bg"], fg=theme["fg"])
        self.toggle_button.configure(bg=theme["bg"], fg=theme["fg"])

    def refresh_label(self):
        trees_saved = self.treesaver.calculate_trees_saved()
        self.label.config(text=f"Trees Saved: {trees_saved:.4f}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TreeReportApp(root)
    root.mainloop()
