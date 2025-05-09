import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from reportlab.pdfgen import canvas
import os

# Sample Data (to be fetched from backend via core in real scenario)
sample_data = [
    {"Date": "2025-05-01", "Item": "Milk", "Qty": 3, "Price": 150},
    {"Date": "2025-05-02", "Item": "Bread", "Qty": 2, "Price": 100},
    {"Date": "2025-05-03", "Item": "Soda", "Qty": 4, "Price": 300}
]

def generate_report(format):
    df = pd.DataFrame(sample_data)

    file_path = filedialog.asksaveasfilename(
        defaultextension=f".{format.lower()}",
        filetypes=[(format, f"*.{format.lower()}")]
    )
    
    if not file_path:
        return

    try:
        if format == "PDF":
            c = canvas.Canvas(file_path)
            c.drawString(100, 800, "StarSon POS Sales Report")
            y = 750
            for row in sample_data:
                line = f"{row['Date']} - {row['Item']} - Qty: {row['Qty']} - KES {row['Price']}"
                c.drawString(80, y, line)
                y -= 20
            c.save()
        elif format == "Excel":
            df.to_excel(file_path, index=False)
        elif format == "CSV":
            df.to_csv(file_path, index=False)

        messagebox.showinfo("Success", f"{format} report generated successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate {format} report.\n{str(e)}")

# GUI Setup
root = tk.Tk()
root.title("StarSon POS - Report Generator")
root.geometry("400x300")

tk.Label(root, text="Generate Sales Report", font=("Arial", 14)).pack(pady=20)

tk.Button(root, text="Export as PDF", command=lambda: generate_report("PDF")).pack(pady=5)
tk.Button(root, text="Export as Excel", command=lambda: generate_report("Excel")).pack(pady=5)
tk.Button(root, text="Export as CSV", command=lambda: generate_report("CSV")).pack(pady=5)

root.mainloop()
