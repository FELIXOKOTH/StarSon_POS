import pandas as pd
from utils.validator import validate_data

def import_data(file_path):
    data = pd.read_csv(file_path)  # or use pd.read_excel for .xlsx
    if validate_data(data):
        print("Import successful!")
    else:
        print("Import failed. Data invalid.")

if __name__ == "__main__":
    file = input("Enter file path: ")
    import_data(file)
