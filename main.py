# main.py

from frontend.gui.main_gui import StarSonPOSApp
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    app = StarSonPOSApp(root)
    root.mainloop()
