# StarSon POS - Frontend GUI (Tkinter)
import tkinter as tk
from tkinter import messagebox

class StarSonPOSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("StarSon POS - Eco Receipt System")
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.root, text="StarSon POS", font=("Helvetica", 18)).pack(pady=10)

        tk.Button(self.root, text="Send Receipt (SMS Only)", command=self.send_sms).pack(pady=5)
        tk.Button(self.root, text="Send Receipt (Email Only)", command=self.send_email).pack(pady=5)
        tk.Button(self.root, text="Send Both (SMS + Email)", command=self.send_both).pack(pady=5)

    def send_sms(self):
        messagebox.showinfo("Receipt", "Receipt sent via SMS.")

    def send_email(self):
        messagebox.showinfo("Receipt", "Receipt sent via Email.")

    def send_both(self):
        messagebox.showinfo("Receipt", "Receipt sent via both SMS and Email.")

if __name__ == "__main__":
    root = tk.Tk()
    app = StarSonPOSApp(root)
    root.mainloop()
