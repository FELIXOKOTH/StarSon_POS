"""
carbon_engine.py
Utility to estimate environmental impact of digital receipts.
"""

def calculate_trees_saved(receipts_avoided: int) -> float:
    """
    Estimate the number of trees saved based on the number of digital receipts issued.
    
    Assumption: 1 tree = 8333 receipts (industry estimate)
    """
    TREES_PER_RECEIPT = 1 / 8333
    trees_saved = receipts_avoided * TREES_PER_RECEIPT
    return round(trees_saved, 4)


def estimate_carbon_avoided(receipts_avoided: int) -> float:
    """
    Estimate the CO2 emissions avoided by issuing digital instead of paper receipts.
    
    Assumption: 1 paper receipt = 2.5 grams CO2.
    """
    CO2_PER_RECEIPT_GRAMS = 2.5
    total_grams = receipts_avoided * CO2_PER_RECEIPT_GRAMS
    total_kg = total_grams / 1000  # convert grams to kilograms
    return round(total_kg, 3)


def generate_carbon_report(receipts_avoided: int) -> dict:
    """
    Generate a carbon report summarizing receipts saved, trees saved, and CO2 avoided.
    """
    return {
        "receipts_avoided": receipts_avoided,
        "trees_saved": calculate_trees_saved(receipts_avoided),
        "carbon_avoided_kg": estimate_carbon_avoided(receipts_avoided)
    }


# Example usage (for testing only)
if __name__ == "__main__":
    test = generate_carbon_report(1500)
    print(test)
