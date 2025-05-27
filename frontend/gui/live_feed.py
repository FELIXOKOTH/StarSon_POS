import tkinter as tk
import threading
import time
import random

class LiveFeedApp:
    def __init__(self, root):
        self.root = root
        self.root.title("StarSon POS | Live Feed")
        self.root.geometry("500x300")

        tk.Label(root, text="Live Feed Updates", font=("Arial", 14)).pack(pady=10)

        self.feed_box = tk.Text(root, height=12, wrap='word', bg="#f0f0f0")
        self.feed_box.pack(padx=10, pady=5, fill='both', expand=True)

        self.running = True
        self.update_thread = threading.Thread(target=self.simulate_feed)
        self.update_thread.start()

    def simulate_feed(self):
        updates = [
            "New transaction: KES 1,200",
            "Digital receipt sent to +254712345678",
            "Technician login: tech123",
            "Shift started by cashier_01",
            "Eco report updated: 0.12 trees saved",
            "New user registered: officer456",
            "System check: All modules active"
        ]
        while self.running:
            msg = random.choice(updates)
            self.feed_box.insert(tk.END, f"{time.strftime('%H:%M:%S')} - {msg}\n")
            self.feed_box.see(tk.END)
            time.sleep(5)  # Update every 5 seconds

    def stop(self):
        self.running = False
        self.update_thread.join()

if __name__ == "__main__":
    root = tk.Tk()
    app = LiveFeedApp(root)
    root.protocol("WM_DELETE_WINDOW", lambda: (app.stop(), root.destroy()))
    root.mainloop()
