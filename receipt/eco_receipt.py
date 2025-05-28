def calculate_trees_saved(receipts_count):
    """
    Estimate how many trees are saved by issuing digital receipts.
    Approximation: 1 paper receipt = 0.0002 trees.
    """
    TREES_PER_RECEIPT = 0.0002
    trees_saved = receipts_count * TREES_PER_RECEIPT
    return round(trees_saved, 4)

def estimate_carbon_avoided(receipts_count):
    """
    Estimate the amount of CO₂ emissions avoided.
    Approximation: 1 paper receipt = 2.5 grams of CO₂.
    """
    CO2_PER_RECEIPT_GRAMS = 2.5
    total_grams = receipts_count * CO2_PER_RECEIPT_GRAMS
    total_kg = total_grams / 1000  # Convert to kilograms
    return round(total_kg, 3)

def generate_eco_receipt_footer(receipts_count):
    trees = calculate_trees_saved(receipts_count)
    carbon = estimate_carbon_avoided(receipts_count)
    
    footer = (
        f"🌱 Eco Receipt Summary 🌍\n"
        f"Receipts issued: {receipts_count}\n"
        f"Trees saved: {trees}\n"
        f"CO₂ avoided: {carbon} kg\n"
        f"Thank you for going green with StarSon POS 💚"
    )
    return footer

# Example for one receipt
if __name__ == "__main__":
    print(generate_eco_receipt_footer(1))
