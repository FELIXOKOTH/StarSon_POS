# from utils.carborn_engine import generate_carborn_report
# If the module is in the same directory, use:
# from carborn_engine import generate_carborn_report
# Or provide a mock function for demonstration:
def generate_carborn_report(receipts_avoided):
	# Mock implementation
	trees_saved = receipts_avoided * 0.00012
	carbon_avoided_kg = receipts_avoided * 0.0025
	return {
		'receipts_avoided': receipts_avoided,
		'trees_saved': round(trees_saved, 2),
		'carbon_avoided_kg': round(carbon_avoided_kg, 2)
	}

data = generate_carborn_report(receipts_avoided=1500)
print(data)
#Output: ('receipts_avoided': 1500.'trees_saved';0.18.'carbon_avoided_kg':3.75)
