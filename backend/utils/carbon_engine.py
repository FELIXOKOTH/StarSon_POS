def calculate_trees_saved(receipts_avoided: int) -> float:
    """
    Estimate the number of trees saved based on the number of digital receipts issued.
    Assumption 8333 receipts = 1 tree (based on industry averages)
    """
    TREES_PER_RECEIPT = 1 / 8333  # one tree per 8333 paper receipts
    trees_saved = receipts_avoided * TREES_PER_RECEIPT
    return round(trees_saved, 4)

def estimate_carbon_avoided(receipts_avoided: int) -> float:
    """
    Estimate the carbon emissions avoided by using digital receipts.
    Assumption 1 paper receipt = 2.5 grams CO2.
    """
    CO2_PER_RECEIPT_GRAMS = 2.5
    total_grams = receipts_avoided * CO2_PER_RECEIPT_GRAMS
    total_kg = total_grams / 1000  # convert to kilograms
    return round(total_kg, 3)

def generate_carbon_report(receipts_avoided: int) -> dict:
    return {
        "receipts_avoided": receipts_avoided,
        "trees_saved": calculate_trees_saved(receipts_avoided),
        "carbon_avoided_kg": estimate_carbon_avoided(receipts_avoided)
    }
