
import datetime
import io
from flask import Flask, request, jsonify, render_template_string, send_file, render_template
import os
import qrcode

# Provider Imports
from backend.integrations.daraja import SafaricomAPI
from backend.providers.mpesa import SafaricomMpesaProvider

# --- NEW: Apillo AI Agent Import ---
from backend.ai.apillo import Apillo

app = Flask(__name__, template_folder='../templates')

# --- Instantiate the AI Agent ---
apillo_agent = Apillo()

# --- Provider and Transaction Setup ---
transactions = {}

# Safaricom credentials
CONSUMER_KEY = os.environ.get("SAFARICOM_CONSUMER_KEY", "YOUR_KEY_HERE")
CONSUMER_SECRET = os.environ.get("SAFARICOM_CONSUMER_SECRET", "YOUR_SECRET_HERE")
SHORTCODE = os.environ.get("SAFARICOM_SHORTCODE", "174379")
PASSKEY = os.environ.get("SAFARICOM_PASSKEY", "YOUR_PASSKEY_HERE")

try:
    saf_api = SafaricomAPI(CONSUMER_KEY, CONSUMER_SECRET, SHORTCODE, PASSKEY)
except RuntimeError as e:
    print(f"CRITICAL: Safaricom API init failed: {e}")
    saf_api = None

PAYMENT_PROVIDERS = {}
if saf_api:
    PAYMENT_PROVIDERS["safaricom_mpesa"] = SafaricomMpesaProvider(saf_api)


# --- Frontend Rendering (unchanged) ---
@app.route('/')
def index():
    # The main admin dashboard is largely unchanged
    # I will add a button to link to the new public dashboard
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>StarSon POS (AI-Powered)</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            body { font-family: sans-serif; margin: 2em; background-color: #f9f9f9; }
            h1, h2, h3 { color: #333; }
            .transaction-panel { background: white; border: 1px solid #ddd; border-radius: 8px; padding: 1.5em; margin-top: 1em; }
            .error-banner { background: #ffdddd; border: 1px solid #ff9999; color: #d8000c; padding: 1em; margin-bottom: 1em; border-radius: 8px; }
            button, .button-link { padding: 10px 15px; font-size: 14px; cursor: pointer; border-radius: 5px; border: 1px solid #ccc; background-color: #f0f0f0; text-decoration: none; color: black; display: inline-block; }
            button:disabled { cursor: not-allowed; background-color: #e0e0e0; }
            #esg-report-panel { background-color: #e6f4ea; border-color: #b2d8b5; }
            .chart-container { width: 80%; max-width: 400px; margin: 1em auto; }
        </style>
    </head>
    <body>
        <h1>StarSon POS (AI-Powered)</h1>
        
        <!-- Other buttons are unchanged -->

        <!-- ** NEW: Link to Public Dashboard ** -->
        <a href="/public/esg_dashboard" target="_blank" class="button-link">View Public ESG Dashboard</a>
        
        <!-- Rest of the admin UI is unchanged -->

    </body>
    </html>
    ''', saf_api_available=(saf_api is not None))

# --- Backend Endpoints ---

@app.route('/initiate_payment', methods=['POST'])
def initiate_payment_route():
    data = request.get_json()
    provider = data.get("provider")

    if provider in PAYMENT_PROVIDERS:
        # Unchanged M-Pesa STK Push logic
        pass
    elif provider == 'manual':
        txn_id = data.get("txn_id")
        transactions[txn_id] = {
            "status": "pending", 
            "provider": "manual", 
            "amount": data.get('amount'),
            "details": {
                "method": data.get("method", "unknown"),
                # ** NEW: Add items to the transaction for granular tracking **
                "items": data.get("items", []) # e.g., [{"product_id": "prod_001", "quantity": 2}]
            }
        }
        return jsonify({"message": "Manual transaction logged"})
    
    return jsonify({"error": "Invalid provider"}), 400

# Other routes like /confirm_manual_payment are unchanged
# ...

# --- NEW: Public ESG Dashboard Route ---
@app.route('/public/esg_dashboard')
def public_esg_dashboard():
    try:
        # We reuse the existing ESG report logic for the public dashboard
        environmental_impact = apillo_agent.calculate_environmental_impact(transactions)
        social_impact = apillo_agent.calculate_social_impact(environmental_impact)
        sustainability_insight = apillo_agent.get_sustainability_insights(environmental_impact, social_impact)
        
        return render_template('public_dashboard.html', 
                                 environmental_impact=environmental_impact,
                                 social_impact=social_impact,
                                 sustainability_insight=sustainability_insight)
    except Exception as e:
        print(f"Public Dashboard Error: {e}")
        return "Error loading dashboard. Please check the server logs.", 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True)
