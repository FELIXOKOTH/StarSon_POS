from tkinter import *
from tree_saver import TreeSaver

root = Tk()
root.title("Tree Saving Report")

tree_saver = TreeSaver()

frame = Frame(root)
frame.pack(padx=10, pady=10)

Label(frame, text="Digital Receipts Summary", font=("Arial", 14, "bold")).pack()
Label(frame, text=f"Total Digital Receipts: {tree_saver.total_digital_receipts()}").pack()
Label(frame, text=f"Estimated Trees Saved: {tree_saver.trees_saved()}").pack()

root.mainloop()
