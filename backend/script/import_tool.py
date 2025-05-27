import pandas as pd
import os
from utils.validator import validate_data

def import_data(file_path):
    if not os.path.exists(file_path):
        print(f"[ERROR] File not found: {file_path}")
        return

    try:
        if file_path.endswith(".xlsx") or file_path.endswith(".xls"):
            data = pd.read_excel(file_path)
        elif file_path.endswith(".csv"):
            data = pd.read_csv(file_path)
        else:
            print("[ERROR] Unsupported file format. Use .csv or .xlsx")
            return

        if validate_data(data):
            print("[SUCCESS] Import successful!")
            # Optionally save or process here
        else:
            print("[WARNING] Import failed. Data invalid.")

    except Exception as e:
        print(f"[ERROR] Failed to import: {e}")

if __name__ == "__main__":
    file = input("Enter file path (e.g., data/sample.csv): ").strip()
    import_data(file)

