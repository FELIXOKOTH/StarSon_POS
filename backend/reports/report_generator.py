# backend/reports/report_generator.py
import datetime

class ReportGenerator:
    def __init__(self):
        self.logs = []

    def log_transaction(self, receipt):
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "total": receipt["total"],
            "channels": receipt["channels"],
            "customer": receipt["customer"]
        }
        self.logs.append(entry)

    def generate_daily_report(self):
        today = datetime.datetime.now().date()
        report = [log for log in self.logs if datetime.datetime.fromisoformat(log["timestamp"]).date() == today]
        return report

    def summarize_savings(self):
        paper_saved = len(self.logs)  # Each digital receipt = 1 paper saved
        trees_saved = paper_saved / 8333  # ~8333 receipts = 1 tree saved (UN estimate)
        return {"receipts": paper_saved, "trees_saved": round(trees_saved, 4)}
