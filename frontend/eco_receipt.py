def calculate_trees_saved(receipts_count):
    paper_per_receipt = 0.0002  # Approximate trees per standard receipt
    trees_saved = receipts_count * paper_per_receipt
    return round(trees_saved, 4)

receipt_footer = f"Trees saved with this receipt: {calculate_trees_saved(1)}"
print(receipt_footer)