
import datetime
import json

class Apillo:
    """
    An independent AI agent for business and ESG (Environmental, Social, Governance) analytics.
    Apillo can be embedded into existing systems to provide insights on sustainability
    and operational efficiency by processing transaction data.
    """

    def __init__(self):
        # In a real-world scenario, this could load configuration, API keys, or pre-trained models.
        pass

    def _call_llm_api(self, prompt, data_packet):
        """
        Simulates a call to a Large Language Model for intelligent insights.
        """
        print("--- Data Packet prepared for Apillo ---")
        print(json.dumps(data_packet, indent=2))
        print("\n--- Prompt sent to Apillo ---")
        print(prompt)
        
        # --- Simulated Apillo Response ---
        if "ESG" in prompt:
            insight = f"The reduction of {data_packet['estimated_carbon_reduction_kg']:.4f} kg of CO2e is a significant step. To improve further, consider partnering with a local environmental group to amplify your impact. Your {data_packet['digital_receipts']} digital receipts show strong customer adoption of your green initiatives."
            return {"esg_insight": insight}
        else:
            peak_hour = max(data_packet.get("sales_by_hour", {}), key=data_packet.get("sales_by_hour", {}).get)
            insight = f"Today's peak activity was around {peak_hour}:00. Preparing for this time tomorrow could enhance customer flow. The {data_packet['eco_metrics']['digital_receipts_issued']} digital receipts are a great sustainability achievement!"
            return {"operational_insight": insight}

    def _process_transactions(self, transactions_dict):
        """
        Internal method to process raw transaction logs into a structured summary.
        """
        summary = {
            "report_date": datetime.date.today().isoformat(),
            "total_sales": 0.0,
            "transaction_count": 0,
            "payment_methods": {},
            "sales_by_hour": {f"{h:02}": 0 for h in range(24)},
            "digital_receipts": 0
        }

        for txn_id, txn_data in transactions_dict.items():
            if txn_data.get("status") != "completed":
                continue
            
            summary["transaction_count"] += 1
            summary["total_sales"] += float(txn_data.get("amount", 0))

            provider_key = txn_data.get("provider", "unknown")
            if "manual" not in provider_key:
                summary["digital_receipts"] += 1
            else:
                provider_key = f"manual_{txn_data.get('details', {}).get('method', 'unknown').lower()}"

            summary["payment_methods"][provider_key] = summary["payment_methods"].get(provider_key, 0) + 1
            
            try:
                confirm_time = datetime.datetime.fromisoformat(txn_data["details"]["confirmation_time"])
                hour_str = f"{confirm_time.hour:02}"
                summary["sales_by_hour"][hour_str] += 1
            except (KeyError, ValueError, IndexError):
                pass
        
        return summary

    def calculate_environmental_impact(self, transactions_dict):
        """
        Calculates key environmental metrics based on transaction data.
        This is a core function for the ESG/Climate Tool capability.
        """
        processed_data = self._process_transactions(transactions_dict)
        digital_receipts = processed_data['digital_receipts']

        # Placeholder calculations for environmental impact:
        # - Trees Saved: Based on industry estimates for paper production.
        # - Carbon Reduction: Based on reduced paper production & printing energy.
        trees_saved = round(digital_receipts * 0.0001, 5)
        carbon_reduction_kg = round(digital_receipts * 0.0015, 4) # (1g paper + 0.5g energy)/receipt

        return {
            "digital_receipts": digital_receipts,
            "trees_saved_estimate": trees_saved,
            "estimated_carbon_reduction_kg": carbon_reduction_kg
        }

    def get_sustainability_insights(self, environmental_data):
        """
        Provides actionable ESG insights based on environmental metrics.
        """
        prompt = f"""
        You are Apillo, a specialized ESG and Climate analytics AI.
        Analyze the provided JSON data, which contains environmental impact metrics from a company's operations.
        Provide one brief, actionable insight to help them improve their sustainability efforts. The tone should be professional and encouraging.
        """
        return self._call_llm_api(prompt, environmental_data)

    def generate_daily_summary(self, transactions_dict):
        """
        Generates a combined business and eco-report for the POS dashboard.
        """
        processed_data = self._process_transactions(transactions_dict)
        eco_metrics = self.calculate_environmental_impact(transactions_dict)
        
        full_summary = {
            **processed_data,
            "eco_metrics": eco_metrics
        }

        prompt = f"""
        You are Apillo, an expert business analyst AI for StarSon POS.
        Provide one brief, actionable operational insight from the daily sales JSON data.
        Your tone should be futuristic and concise.
        """

        operational_insight = self._call_llm_api(prompt, full_summary)['operational_insight']
        
        return {
            "summary_title": "Apillo's End-of-Day Business Summary",
            "key_metric": f"Total Sales: KES {full_summary['total_sales']:.2f} from {full_summary['transaction_count']} transactions.",
            "actionable_insight": operational_insight,
            "raw_data": full_summary
        }
