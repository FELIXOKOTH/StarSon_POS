import datetime
import io
from flask import Flask, request, jsonify, render_template, send_from_directory
import os
import qrcode

# Provider Imports
from backend.integrations.daraja import SafaricomAPI
from backend.providers.mpesa import SafaricomMpesaProvider

# Apillo AI Agent Import
from backend.ai.apillo import Apillo

app = Flask(__name__, template_folder='../templates', static_folder='../static')

apillo_agent = Apillo()
transactions = {}

# Safaricom credentials setup (unchanged)
# ...

# --- Frontend Rendering ---
@app.route('/')
def index():
    """Renders the main admin dashboard from a template file."""
    return render_template('admin_dashboard.html', saf_api_available=(saf_api is not None))

# --- Backend Endpoints ---

# The /initiate_payment and other routes are unchanged
# ...

# --- NEW: Public ESG Dashboard & Goal Setting ---

esg_goals = {
    "monthly_carbon_reduction_kg": 100,
    "monthly_water_saved_liters": 5000,
    "current_carbon_reduction": 45,
    "current_water_saved": 2100
}

@app.route('/public/esg_dashboard')
def public_esg_dashboard():
    try:
        environmental_impact = apillo_agent.calculate_environmental_impact(transactions)
        social_impact = apillo_agent.calculate_social_impact(environmental_impact)
        sustainability_insight = apillo_agent.get_sustainability_insights(environmental_impact, social_impact)
        
        # Add goal progress to the payload
        esg_goals['current_carbon_reduction'] = environmental_impact.get('granular_carbon_footprint_kg', 0)
        esg_goals['current_water_saved'] = environmental_impact.get('granular_water_usage_l', 0)

        return render_template('public_dashboard.html', 
                                 environmental_impact=environmental_impact,
                                 social_impact=social_impact,
                                 sustainability_insight=sustainability_insight,
                                 esg_goals=esg_goals) # Pass goals to the template
    except Exception as e:
        print(f"Public Dashboard Error: {e}")
        return "Error loading dashboard. Please check the server logs.", 500

# --- Static File Serving ---
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('../static', path)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True)
