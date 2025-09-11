import random

class AnalyticsEngine:
    def __init__(self, transactions=None):
        """
        Initializes the Analytics Engine.
        Args:
            transactions (dict): A dictionary of transaction data.
        """
        self.transactions = transactions if transactions is not None else {}

    def get_transaction_data(self):
        """Returns the transaction data."""
        return self.transactions

    def predict_inventory(self, sales_data, current_stock):
        # Dummy implementation for demonstration
        predictions = {}
        for item_id, stock in current_stock.items():
            predictions[item_id] = {"predicted_demand": stock * 1.5, "recommendation": "Restock"}
        return predictions

    def forecast_sales(self, sales_data):
        # Dummy implementation
        return {"next_month_forecast": sum(item['total_sales'] for item in sales_data) * 1.2}

    def segment_customers(self, customer_data):
        # Dummy implementation
        segments = {"high_value": [], "medium_value": [], "low_value": []}
        for customer in customer_data:
            if customer['total_spent'] > 1000:
                segments['high_value'].append(customer['id'])
            elif customer['total_spent'] > 200:
                segments['medium_value'].append(customer['id'])
            else:
                segments['low_value']
        return segments
