import time
import threading
from datetime import datetime

# Apillo AI Agent Import
from backend.ai.apillo import Apillo

# --- Reporting Functions ---

def generate_esg_report_content(apillo_agent: Apillo, transactions: dict) -> str:
    """Generates the HTML content for the ESG report."""
    try:
        environmental_impact = apillo_agent.calculate_environmental_impact(transactions)
        social_impact = apillo_agent.calculate_social_impact(environmental_impact)
        sustainability_insight = apillo_agent.get_sustainability_insights(environmental_impact, social_impact)

        # Create a simple HTML structure for the report
        report_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Daily ESG Report</title>
            <style>
                body {{ font-family: sans-serif; margin: 2rem; }}
                .container {{ max-width: 800px; margin: auto; }}
                .panel {{ border: 1px solid #ccc; border-radius: 8px; padding: 1rem; margin-bottom: 2rem; }}
                h1, h2 {{ color: #28a745; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>ESG & Sustainability Report</h1>
                <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>

                <div class="panel">
                    <h2>Apillo's Insight</h2>
                    <p>{sustainability_insight['esg_insight']}</p>
                </div>

                <div class="panel">
                    <h2>Environmental Impact</h2>
                    <ul>
                        <li>CO2 Reduction (from digital receipts): {environmental_impact['estimated_carbon_reduction_kg']} kg</li>
                        <li>Water Saved (from digital receipts): {environmental_impact['water_saved_liters']} L</li>
                        <li>Waste Diverted (from paperless): {environmental_impact['waste_diverted_kg']} kg</li>
                        <li>Trees Saved: {environmental_impact['trees_saved']:.4f}</li>
                        <hr>
                        <li>Carbon Footprint (from products): {environmental_impact['granular_carbon_footprint_kg']} kg</li>
                        <li>Water Usage (from products): {environmental_impact['granular_water_usage_l']} L</li>
                    </ul>
                </div>

                <div class="panel">
                    <h2>Social Impact</h2>
                     <p>Community Give-Back (KES): {social_impact['community_give_back_kes']}</p>
                </div>

            </div>
        </body>
        </html>
        """
        return report_content

    except Exception as e:
        print(f"Error generating report content: {e}")
        return f"<p>Error generating report: {e}</p>"

def save_report_to_file(content: str):
    """Saves the report content to a timestamped HTML file."""
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f"esg_report_{timestamp}.html"
    with open(filename, 'w') as f:
        f.write(content)
    print(f"Successfully generated report: {filename}")


# --- Scheduler ---

def reporting_scheduler(apillo_agent: Apillo, transactions: dict, interval_seconds: int = 86400):
    """Runs the report generation task at a specified interval."""
    def task():
        print("Running daily ESG report generation...")
        report_content = generate_esg_report_content(apillo_agent, transactions)
        save_report_to_file(report_content)
        # Schedule the next run
        threading.Timer(interval_seconds, task).start()

    # Start the first run
    print(f"Scheduling ESG reports to run every {interval_seconds} seconds.")
    task() # Run once immediately, then schedule

def start_reporting_thread(apillo_agent: Apillo, transactions: dict):
    """Starts the reporting scheduler in a background thread."""
    scheduler_thread = threading.Thread(
        target=reporting_scheduler, 
        args=(apillo_agent, transactions), 
        daemon=True # Allows main thread to exit even if this thread is running
    )
    scheduler_thread.start()
