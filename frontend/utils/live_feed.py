# frontend/live_feed.py

import tkinter as tk
from tkinter import messagebox

class LiveFeedApp:
    def __init__(self, master):
        self.master = master
        master.title("Live Feed - StarSon POS")
        master.geometry("500x300")

        self.feed_display = tk.Listbox(master, height=15, width=50)
        self.feed_display.pack(pady=20)

        # Simulating live updates
        self.feed_display.insert(tk.END, "Starting Live Feed...")
        self.add_feed_item("Transaction ID: T001 - Item: Rice - $50 - Carbon Saved: 5kg")
        self.add_feed_item("Transaction ID: T002 - Item: Beans - $30 - Carbon Saved: 3kg")

    def add_feed_item(self, text):
        self.feed_display.insert(tk.END, text)
        self.feed_display.yview(tk.END)  # Auto-scroll to bottom

if __name__ == "__main__":
    root = tk.Tk()
    live_feed_app = LiveFeedApp(root)
    root.mainloop()
