from tkinter import Tk, Label
from constant_ui import TITLE_FONT, PRIMARY_COLOR, BACKGROUND_COLOR

# Example
root = Tk()
label = Label(root, text="welcome", font=TITLE_FONT, bg=BACKGROUND_COLOR, fg=PRIMARY_COLOR)
label.pack(pady=10)
