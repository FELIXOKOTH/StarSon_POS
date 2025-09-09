import random
import json
import os

class Apillo:
    def __init__(self):
        self.name = "Apillo"
        self.product_catalog = self._load_product_catalog()

    def _load_product_catalog(self):
        try:
            # Correctly locate the data file relative to the backend directory
            base_dir = os.path.dirname(os.path.abspath(__file__))
            catalog_path = os.path.join(base_dir, '..', 'data', 'product_catalog.json')
            with open(catalog_path, 'r') as f:
                return json.load(f).get('products', [])
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Warning: Could not load product catalog: {e}")
            return []

    def generate_daily_summary(self, transactions):
        # This function remains unchanged
        total_sales = sum(t['amount'] for t in transactions.values() if t['status'] == 'completed')
        num_transactions = len(transactions)
        completed_transactions = sum(1 for t in transactions.values() if t['status'] == 'completed')

        return {
            "total_sales": total_sales,
            "transaction_count": num_transactions,
            "completed_transactions": completed_transactions,
            "summary_statement": f"Apillo's Summary: Today saw {num_transactions} transactions totaling {total_sales} KES, with {completed_transactions} successfully completed."
        }

    # --- UPDATED: Granular Environmental Impact ---
    def calculate_environmental_impact(self, transactions):
        digital_receipts = 0
        total_carbon_footprint = 0
        total_water_usage = 0
        recyclable_items = 0
        total_items = 0

        for txn in transactions.values():
            if txn['status'] == 'completed':
                digital_receipts += 1
                # Simulate items in a transaction
                purchased_product_ids = txn.get('details', {}).get('product_ids', [])
                
                for item_id in purchased_product_ids:
                    product = next((p for p in self.product_catalog if p['id'] == item_id), None)
                    if product:
                        total_items += 1
                        total_carbon_footprint += product['esg_metrics'].get('carbon_footprint_kg', 0)
                        total_water_usage += product['esg_metrics'].get('water_usage_l', 0)
                        if product['esg_metrics'].get('recyclable_packaging', False):
                            recyclable_items += 1
        
        # Add impact from digital receipts as a baseline
        total_carbon_footprint += digital_receipts * 0.005 # 5g CO2 per paper receipt avoided
        total_water_usage += digital_receipts * 0.1      # 100ml water per paper receipt avoided

        return {
            "digital_receipts": digital_receipts,
            "product_level_carbon_footprint_kg": round(total_carbon_footprint, 4),
            "product_level_water_usage_l": round(total_water_usage, 4),
            "recyclable_packaging_percentage": round((recyclable_items / total_items) * 100, 2) if total_items > 0 else 0,
        }

    # --- All other methods (social impact, corporate ESG, etc.) remain unchanged ---
    def calculate_social_impact(self, environmental_impact):
        # This can be enhanced later to tie into product-level metrics
        give_back_rate = 0.50 # 50 KES per digital receipt
        community_give_back = environmental_impact['digital_receipts'] * give_back_rate
        return {
            "community_give_back_kes": community_give_back,
            "program_description": "Donation to local environmental cleanup initiatives."
        }

    def calculate_corporate_esg_profile(self, transactions):
        # Unchanged
        supply_chain_transparency = self._get_supply_chain_transparency(transactions)
        diversity_and_inclusion = self._get_diversity_and_inclusion_score(transactions)

        return {
            "supply_chain_transparency": supply_chain_transparency,
            "diversity_and_inclusion": diversity_and_inclusion
        }

    def _get_supply_chain_transparency(self, transactions):
        # Unchanged
        certified_transactions = sum(1 for t in transactions.values() if t.get('details', {}).get('supplier_certified', False))
        total_transactions = len(transactions)
        score = (certified_transactions / total_transactions) * 100 if total_transactions > 0 else 0
        return {
            "certified_fair_trade_percentage": round(score, 2),
            "description": "Percentage of transactions linked to certified fair-trade suppliers."
        }

    def _get_diversity_and_inclusion_score(self, transactions):
        # Unchanged
        ownership_scores = [t.get('details', {}).get('ownership_diversity_score', 5) for t in transactions.values()]
        average_score = sum(ownership_scores) / len(ownership_scores) if ownership_scores else 0
        return {
            "average_ownership_diversity_score": round(average_score, 2),
            "description": "Average diversity & inclusion score based on business ownership."
        }

    def get_sustainability_insights(self, environmental_impact, social_impact, corporate_esg=None):
        # Updated to reflect new metrics
        insight = f"Today's {environmental_impact['digital_receipts']} digital transactions significantly reduced our footprint. The total carbon impact was {environmental_impact['product_level_carbon_footprint_kg']} kg, and we saved {environmental_impact['product_level_water_usage_l']} liters of water."
        
        if environmental_impact['recyclable_packaging_percentage'] > 75:
            insight += " Excellent use of recyclable packaging."

        if corporate_esg:
            if corporate_esg['supply_chain_transparency']['certified_fair_trade_percentage'] > 50:
                insight += " The high percentage of fair-trade suppliers is commendable."
        
        return {"esg_insight": insight}
