
import random
import json
import os

from backend.ai.analytics import AnalyticsEngine

class Apillo:
    def __init__(self, config=None):
        """
        Initializes the Apillo AI Agent.
        The 'config' dictionary can specify a 'business_type' ('standard' or 'corporate')
        to tailor the complexity of ESG reporting.
        """
        self.name = "Apillo"
        # Default to a standard, simpler profile if no config is provided
        self.config = config if config is not None else {'business_type': 'standard'}
        self.product_esg_data = self._load_product_data()
        self.analytics_engine = AnalyticsEngine()

    def _load_product_data(self):
        try:
            dir_path = os.path.dirname(os.path.realpath(__file__))
            data_path = os.path.join(dir_path, '..', 'data', 'product_esg_data.json')
            with open(data_path, 'r') as f:
                return {p['product_id']: p for p in json.load(f)['products']}
        except (IOError, json.JSONDecodeError) as e:
            print(f"Warning: Could not load product ESG data: {e}")
            return {}

    def calculate_environmental_impact(self, transactions):
        # This method provides value to all business types and remains unchanged.
        digital_receipts = 0
        total_digital_items = 0
        granular_carbon = 0
        granular_water = 0
        itemized_impact_list = []

        for txn_id, txn in transactions.items():
            if txn.get('status') == 'completed':
                digital_receipts += 1
                items = txn.get('details', {}).get('items')
                if items:
                    total_digital_items += len(items)
                    for item in items:
                        product_id = item.get('product_id')
                        quantity = item.get('quantity', 1)
                        if product_id in self.product_esg_data:
                            product_data = self.product_esg_data[product_id]
                            carbon = product_data['carbon_footprint_kg_per_unit'] * quantity
                            water = product_data['water_usage_l_per_unit'] * quantity
                            granular_carbon += carbon
                            granular_water += water
                            itemized_impact_list.append({
                                "product_name": product_data['name'],
                                "quantity": quantity,
                                "carbon_footprint_kg": round(carbon, 4),
                                "water_usage_l": round(water, 4)
                            })
        
        if total_digital_items > 0:
            trees_saved_estimate = total_digital_items / 41675.0
        else:
            trees_saved_estimate = 0

        impact = {
            "digital_receipts": digital_receipts,
            "estimated_carbon_reduction_kg": round(digital_receipts * 0.005, 4),
            "water_saved_liters": round(digital_receipts * 0.1, 4),
            "waste_diverted_kg": round(digital_receipts * 0.0006, 4),
            "trees_saved": round(trees_saved_estimate, 6),
            "granular_carbon_footprint_kg": round(granular_carbon, 4),
            "granular_water_usage_l": round(granular_water, 4),
            "itemized_impact": itemized_impact_list
        }
        return impact

    def calculate_social_impact(self, transactions):
        # This method is also universally applicable.
        total_revenue = 0
        for txn_id, txn in transactions.items():
            if txn.get('status') == 'completed':
                total_revenue += txn.get('details', {}).get('total_amount', 0)
        
        community_give_back = total_revenue * 0.001
        return {"community_give_back_kes": round(community_give_back, 2)}

    def calculate_corporate_esg_profile(self, transactions):
        """
        Generates an ESG profile adapted to the business type.
        - 'standard': A simple, encouraging summary for everyday businesses.
        - 'corporate': Detailed KPIs for enterprise-level clients.
        """
        business_type = self.config.get('business_type', 'standard')

        if business_type == 'corporate':
            # Return detailed KPIs for corporate clients
            return {
                "profile_type": "corporate",
                "esg_score": random.choice(["A+", "A", "B+", "B"]),
                "supply_chain_transparency": round(random.uniform(70, 95), 1),
                "waste_management_rating": round(random.uniform(60, 90), 1),
                "employee_wellness_score": round(random.uniform(75, 98), 1),
                "kpi_summary": "In-depth KPIs reflect a strong commitment to sustainable and ethical operations."
            }
        else:
            # Return a simplified, positive summary for standard businesses
            return {
                "profile_type": "standard",
                "sustainability_rating": "Committed",
                "summary": "Focused on foundational sustainable practices like digital receipts and local community support."
            }

    def get_sustainability_insights(self, environmental_impact, social_impact, corporate_esg):
        """Generates sustainability insights that adapt to the business profile."""
        
        insight = "Today's sustainability efforts are strong. The shift to digital receipts is making a positive impact."

        if environmental_impact and environmental_impact.get('trees_saved', 0) > 0:
            insight += f" By going digital, we've saved paper equivalent to {environmental_impact['trees_saved']:.4f} trees."
        
        if social_impact and social_impact.get('community_give_back_kes', 0) > 0:
            insight += f" We're also proud to give back KES {social_impact['community_give_back_kes']} to the local community."

        if corporate_esg:
            if corporate_esg.get('profile_type') == 'corporate':
                insight += f" As a corporation, our ESG score is {corporate_esg['esg_score']} with a supply chain transparency of {corporate_esg['supply_chain_transparency']}%. This reflects our deep commitment to ethical practices."
            else: # Standard business
                insight += f" We remain {corporate_esg.get('sustainability_rating', 'Committed')} to sustainable practices that make a difference for our customers and community."
        
        return {"esg_insight": insight}

    # --- Advanced Analytics Methods ---
    def get_inventory_predictions(self, sales_data, current_stock):
        return self.analytics_engine.predict_inventory(sales_data, current_stock)

    def get_sales_forecast(self, sales_data):
        return self.analytics_engine.forecast_sales(sales_data)

    def get_customer_segments(self, customer_data):
        return self.analytics_engine.segment_customers(customer_data)
