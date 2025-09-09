import random
import json
import os

class Apillo:
    def __init__(self):
        self.name = "Apillo"
        self.product_esg_data = self._load_product_data()

    def _load_product_data(self):
        try:
            # Correctly locate the data file relative to this script
            dir_path = os.path.dirname(os.path.realpath(__file__))
            data_path = os.path.join(dir_path, '..', 'data', 'product_esg_data.json')
            with open(data_path, 'r') as f:
                return {p['product_id']: p for p in json.load(f)['products']}
        except (IOError, json.JSONDecodeError) as e:
            print(f"Warning: Could not load product ESG data: {e}")
            return {}

    def generate_daily_summary(self, transactions):
        # This method is unchanged
        # ...
        pass

    def calculate_environmental_impact(self, transactions):
        # Existing calculation for digital receipts
        digital_receipts = sum(1 for t in transactions.values() if t['status'] == 'completed')
        impact = {
            "digital_receipts": digital_receipts,
            "estimated_carbon_reduction_kg": round(digital_receipts * 0.005, 4),
            "water_saved_liters": round(digital_receipts * 0.1, 4),
            "waste_diverted_kg": round(digital_receipts * 0.0006, 4),
            # --- NEW: Granular Metrics ---
            "granular_carbon_footprint_kg": 0,
            "granular_water_usage_l": 0,
            "itemized_impact": []
        }

        # --- NEW: Calculation for per-product impact ---
        for txn_id, txn in transactions.items():
            if txn['status'] == 'completed' and 'items' in txn.get('details', {}):
                for item in txn['details']['items']:
                    product_id = item.get('product_id')
                    quantity = item.get('quantity', 1)
                    
                    if product_id in self.product_esg_data:
                        product_data = self.product_esg_data[product_id]
                        carbon = product_data['carbon_footprint_kg_per_unit'] * quantity
                        water = product_data['water_usage_l_per_unit'] * quantity

                        impact['granular_carbon_footprint_kg'] += carbon
                        impact['granular_water_usage_l'] += water
                        impact['itemized_impact'].append({
                            "product_name": product_data['name'],
                            "quantity": quantity,
                            "carbon_footprint_kg": round(carbon, 4),
                            "water_usage_l": round(water, 4)
                        })
        
        impact['granular_carbon_footprint_kg'] = round(impact['granular_carbon_footprint_kg'], 4)
        impact['granular_water_usage_l'] = round(impact['granular_water_usage_l'], 4)
        
        return impact

    def calculate_social_impact(self, environmental_impact):
        # This method is unchanged
        # ...
        pass

    def calculate_corporate_esg_profile(self, transactions):
        # This method is unchanged
        # ...
        pass

    def get_sustainability_insights(self, environmental_impact, social_impact, corporate_esg=None):
        # Updated to include granular insights
        insight = "Today's sustainability efforts are strong. The shift to digital receipts is reducing our environmental footprint."
        
        if environmental_impact.get('granular_carbon_footprint_kg', 0) > 0:
            insight += f" The detailed product tracking reveals a carbon footprint of {environmental_impact['granular_carbon_footprint_kg']} kg and water usage of {environmental_impact['granular_water_usage_l']} L."

        if corporate_esg:
            # Unchanged corporate insights
            pass
        
        return {"esg_insight": insight}
