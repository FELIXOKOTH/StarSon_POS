import tkinter as tk

class ThemeSelector:
    def __init__(self, root):
        self.root = root
        self.theme = "light"  # default theme
        self.styles = {
            "light": {
                "bg": "#FFFFFF",
                "fg": "#000000",
                "button_bg": "#E0E0E0"
            },
            "dark": {
                "bg": "#2E2E2E",
                "fg": "#FFFFFF",
                "button_bg": "#4F4F4F"
            }
        }

    def apply_theme(self, widgets):
        style = self.styles[self.theme]
        self.root.configure(bg=style["bg"])
        for widget in widgets:
            widget.configure(
                bg=style.get("button_bg", style["bg"]),
                fg=style["fg"]
            )

    def toggle_theme(self, widgets):
        self.theme = "dark" if self.theme == "light" else "light"
        self.apply_theme(widgets)

# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    root.title("StarSon POS | Theme Selector")

    theme_handler = ThemeSelector(root)

    label = tk.Label(root, text="Welcome to StarSon POS")
    button = tk.Button(root, text="Toggle Theme", command=lambda: theme_handler.toggle_theme([label, button]))

    label.pack(pady=10)
    button.pack(pady=10)

    theme_handler.apply_theme([label, button])  # Apply default theme
    root.mainloop()
