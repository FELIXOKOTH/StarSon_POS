from utils.carbon_engine import CarbonEngine

carbon_tracker = CarbonEngine
trees_saved = carbon_tracker.log_receipt(receipt_count=1)

print(f"Trees Saved:{trees_saved}")
