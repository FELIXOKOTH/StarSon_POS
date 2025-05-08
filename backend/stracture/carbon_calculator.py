# core/carbon_calculator.py

def calculate_carbon_savings(paper_receipts_saved):
    """
    Each paper receipt avoided saves approx 0.03kg CO2
    """
    co2_saved = paper_receipts_saved * 0.03
    return {
        "receipts_saved": paper_receipts_saved,
        "co2_saved_kg": round(co2_saved, 4)
    }
