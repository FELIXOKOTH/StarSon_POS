import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from reportlab.pdfgen import canvas
import os

# Sample data (replace with backend/API data in future)
sample_data = [
    {"Date": "2025-05-01", "Item": "Milk", "Qty": 3, "Price": 150},
    {"Date": "2025-05-02", "Item": "Bread", "Qty": 2, "Price": 100},
    {"Date": "2025-05-03", "Item": "Soda", "Qty": 4, "Price": 300}
]

def generate_report_file(data, format):
    df = pd.DataFrame(data)

    file_path = filedialog.asksaveasfilename(
        defaultextension=f".{format.lower()}",
        filetypes=[(f"{format} files", f"*.{format.lower()}")]
    )

    if not file_path:
        return

    try:
        if format == "PDF":
            c = canvas.Canvas(file_path)
            c.setFont("Helvetica", 12)
            c.drawString(100, 800, "StarSon POS Sales Report")
            y = 770
            for row in data:
                line = f"{row['Date']} | {row['Item']} | Qty: {row['Qty']} | KES {row['Price']}"
                c.drawString(80, y, line)
                y -= 20
            c.save()

        elif format == "Excel":
            df.to_excel(file_path, index=False)

        elif format == "CSV":
            df.to_csv(file_path, index=False)

        messagebox.showinfo("Success", f"{format} report saved to:\n{file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate {format} report:\n{str(e)}")

# GUI Layout
def start_report_gui():
    root = tk.Tk()
    root.title("StarSon POS - Report Generator")
    root.geometry("400x250")
    root.resizable(False, False)

    tk.Label(root, text="Export Sales Report", font=("Arial", 14)).pack(pady=20)

    tk.Button(root, text="Export as PDF", width=20, command=lambda: generate_report_file(sample_data, "PDF")).pack(pady=5)
    tk.Button(root, text="Export as Excel", width=20, command=lambda: generate_report_file(sample_data, "Excel")).pack(pady=5)
    tk.Button(root, text="Export as CSV", width=20, command=lambda: generate_report_file(sample_data, "CSV")).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    start_report_gui()

