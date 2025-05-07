# main.py

import tkinter as tk
from frontend.gui.main_gui import StarSonPOSApp

def launch_app():
    root = tk.Tk()
    app = StarSonPOSApp(root)
    root.mainloop()

if __name__ == "__main__":
    launch_app()
