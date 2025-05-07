# core/carbon_engine/carbon_calculator.py

class CarbonCalculator:
    def __init__(self):
        self.paper_saved = 0

    def record_digital_receipt(self):
        self.paper_saved += 1

    def calculate_tree_savings(self):
        # UN estimate: 8333 receipts = 1 tree
        return round(self.paper_saved / 8333, 4)

    def calculate_carbon_credits(self):
        # Approx 0.059 kg CO₂ saved per paper receipt
        # 1 carbon credit = 1000 kg CO₂
        total_kg_saved = self.paper_saved * 0.059
        credits = total_kg_saved / 1000
        return round(credits, 6)

    def get_summary(self):
        return {
            "paper_saved": self.paper_saved,
            "trees_saved": self.calculate_tree_savings(),
            "carbon_credits": self.calculate_carbon_credits()
        }
