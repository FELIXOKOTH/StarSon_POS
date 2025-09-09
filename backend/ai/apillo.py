import random

class Apillo:
    def __init__(self):
        self.name = "Apillo"

    def generate_daily_summary(self, transactions):
        total_sales = sum(t['amount'] for t in transactions.values() if t['status'] == 'completed')
        num_transactions = len(transactions)
        completed_transactions = sum(1 for t in transactions.values() if t['status'] == 'completed')

        return {
            "total_sales": total_sales,
            "transaction_count": num_transactions,
            "completed_transactions": completed_transactions,
            "summary_statement": f"Apillo's Summary: Today saw {num_transactions} transactions totaling {total_sales} KES, with {completed_transactions} successfully completed."
        }

    def calculate_environmental_impact(self, transactions):
        digital_receipts = sum(1 for t in transactions.values() if t['status'] == 'completed')
        # Environmental benefits of digital receipts (approximations)
        return {
            "digital_receipts": digital_receipts,
            "estimated_carbon_reduction_kg": round(digital_receipts * 0.005, 4), # 5g CO2 per paper receipt
            "water_saved_liters": round(digital_receipts * 0.1, 4),      # 100ml water per paper receipt
            "waste_diverted_kg": round(digital_receipts * 0.0006, 4),     # 0.6g per paper receipt
        }

    def calculate_social_impact(self, environmental_impact):
        # Social impact linked to environmental savings (e.g., community fund)
        give_back_rate = 0.50 # 50 KES per digital receipt
        community_give_back = environmental_impact['digital_receipts'] * give_back_rate
        return {
            "community_give_back_kes": community_give_back,
            "program_description": "Donation to local environmental cleanup initiatives."
        }

    # --- NEW: Corporate ESG Metrics ---
    def calculate_corporate_esg_profile(self, transactions):
        supply_chain_transparency = self._get_supply_chain_transparency(transactions)
        diversity_and_inclusion = self._get_diversity_and_inclusion_score(transactions)

        return {
            "supply_chain_transparency": supply_chain_transparency,
            "diversity_and_inclusion": diversity_and_inclusion
        }

    def _get_supply_chain_transparency(self, transactions):
        # Simulate checking if transactions are linked to certified suppliers
        certified_transactions = sum(1 for t in transactions.values() if t.get('details', {}).get('supplier_certified', False))
        total_transactions = len(transactions)
        
        if total_transactions == 0:
            score = 0
        else:
            score = (certified_transactions / total_transactions) * 100
        
        return {
            "certified_fair_trade_percentage": round(score, 2),
            "description": "Percentage of transactions linked to certified fair-trade suppliers."
        }

    def _get_diversity_and_inclusion_score(self, transactions):
        # Simulate assessing business ownership for a D&I score
        # In a real app, this would come from merchant data
        ownership_scores = [t.get('details', {}).get('ownership_diversity_score', 5) for t in transactions.values()]
        
        if not ownership_scores:
            average_score = 0
        else:
            average_score = sum(ownership_scores) / len(ownership_scores)
            
        return {
            "average_ownership_diversity_score": round(average_score, 2), # Score out of 10
            "description": "Average diversity & inclusion score based on business ownership (e.g., women-owned, minority-owned)."
        }

    def get_sustainability_insights(self, environmental_impact, social_impact, corporate_esg=None):
        # Generate a qualitative insight based on the data
        insight = "Today's sustainability efforts are strong. The shift to digital receipts is reducing our environmental footprint."
        
        if corporate_esg:
            if corporate_esg['supply_chain_transparency']['certified_fair_trade_percentage'] > 50:
                insight += " The high percentage of fair-trade suppliers is commendable."
            if corporate_esg['diversity_and_inclusion']['average_ownership_diversity_score'] > 7:
                insight += " The business ecosystem shows strong diversity and inclusion."
        
        return {"esg_insight": insight}
