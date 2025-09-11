from backend.ai.apillo import Apillo

class Chatbot:
    def __init__(self, apillo_agent: Apillo):
        self.apillo_agent = apillo_agent

    def get_response(self, user_query: str) -> str:
        """Generates a response to a user's ESG-related query."""
        user_query = user_query.lower()
        transactions = self.apillo_agent.analytics_engine.get_transaction_data()
        environmental_impact = self.apillo_agent.calculate_environmental_impact(transactions)
        social_impact = self.apillo_agent.calculate_social_impact(transactions)
        corporate_esg = self.apillo_agent.calculate_corporate_esg_profile(transactions)

        if "esg score" in user_query:
            if corporate_esg.get('profile_type') == 'corporate':
                return f"Our current ESG score is {corporate_esg['esg_score']}. This reflects our commitment to sustainable and ethical operations."
            else:
                return f"We are rated as '{corporate_esg.get('sustainability_rating')}' for our commitment to sustainability."
        elif "supply chain" in user_query or "transparency" in user_query:
             if corporate_esg.get('profile_type') == 'corporate':
                return f"We have a supply chain transparency of {corporate_esg['supply_chain_transparency']}%. We believe in being open about our sourcing and production."
             else:
                return "We are committed to working with ethical and transparent suppliers."
        elif "waste management" in user_query:
             if corporate_esg.get('profile_type') == 'corporate':
                return f"Our waste management rating is {corporate_esg['waste_management_rating']}%. We are actively working to minimize our environmental footprint."
             else:
                return "We are actively working to reduce waste and promote recycling."
        elif "environmental impact" in user_query:
            return f"Today, we've reduced CO2 by {environmental_impact['estimated_carbon_reduction_kg']} kg, saved {environmental_impact['water_saved_liters']} L of water, and saved the equivalent of {environmental_impact['trees_saved']} trees."
        elif "social impact" in user_query or "community" in user_query:
            return f"We are proud to contribute {social_impact['community_give_back_kes']} KES to our community give-back program today."
        else:
            return "I can answer questions about our sustainability efforts. What would you like to know?"
