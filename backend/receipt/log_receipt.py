import csv

CSV_LOG_FILE = "receipt_log.csv"

def append_csv_log(receipt_id, method):
    file_exists = os.path.exists(CSV_LOG_FILE)
    with open(CSV_LOG_FILE, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(["receipt_id", "method", "timestamp"])
        writer.writerow([receipt_id, method, datetime.now().isoformat()])
