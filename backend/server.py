
import datetime
import io
import json
from flask import Flask, request, jsonify, render_template_string, send_file, render_template
import os
import qrcode
import random

# Provider Imports
from backend.integrations.daraja import SafaricomAPI
from backend.providers.mpesa import SafaricomMpesaProvider

# --- AI Agent Import ---
from backend.ai.apillo import Apillo

app = Flask(__name__)

# --- Instantiate the AI Agent ---
apillo_agent = Apillo()

# --- Provider and Transaction Setup ---
transactions = {}

# --- Load Product Catalog ---
def load_product_catalog():
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        catalog_path = os.path.join(base_dir, '..', 'data', 'product_catalog.json')
        with open(catalog_path, 'r') as f:
            return json.load(f).get('products', [])
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Warning: Could not load product catalog: {e}")
        return []

product_catalog = load_product_catalog()

# Safaricom credentials (placeholders)
CONSUMER_KEY = os.environ.get("SAFARICOM_CONSUMER_KEY", "YOUR_KEY_HERE")
CONSUMER_SECRET = os.environ.get("SAFARICOM_CONSUMER_SECRET", "YOUR_SECRET_HERE")
SHORTCODE = os.environ.get("SAFARICOM_SHORTCODE", "174379")
PASSKEY = os.environ.get("SAFARICOM_PASSKEY", "YOUR_PASSKEY_HERE")

try:
    saf_api = SafaricomAPI(CONSUMER_KEY, CONSUMER_SECRET, SHORTCODE, PASSKEY)
    PAYMENT_PROVIDERS = {"safaricom_mpesa": SafaricomMpesaProvider(saf_api)}
except RuntimeError as e:
    print(f"CRITICAL: Safaricom API init failed: {e}")
    saf_api = None
    PAYMENT_PROVIDERS = {}

# --- Frontend Routes ---
@app.route('/')
def index():
    # Internal dashboard - unchanged
    return render_template('internal_dashboard.html', saf_api_available=(saf_api is not None))

@app.route('/public_esg_dashboard')
def public_esg_dashboard():
    # Render the new public-facing dashboard template
    return render_template('public_dashboard.html')


# --- Backend API Endpoints ---

@app.route('/initiate_payment', methods=['POST'])
def initiate_payment_route():
    # Unchanged
    pass # Keep existing logic

@app.route('/confirm_manual_payment', methods=['POST'])
def confirm_manual_route():
    data = request.get_json()
    txn_id = data.get("txn_id")
    if not txn_id or txn_id not in transactions:
        return jsonify({"error": "Transaction not found"}), 404
    
    transactions[txn_id]['status'] = 'completed'
    transactions[txn_id]['details']['confirmation_time'] = datetime.datetime.now().isoformat()
    
    # --- NEW: Simulate product purchases for granular ESG data ---
    if product_catalog:
        num_products_to_add = random.randint(1, 3)
        purchased_ids = [random.choice(product_catalog)['id'] for _ in range(num_products_to_add)]
        transactions[txn_id]['details']['product_ids'] = purchased_ids

    # Add corporate ESG data as before
    transactions[txn_id]['details']['supplier_certified'] = random.choice([True, False])
    transactions[txn_id]['details']['ownership_diversity_score'] = random.randint(1, 10)

    return jsonify({"status": "confirmed", "details": transactions[txn_id]['details']})

@app.route('/apillo/daily_summary')
def get_daily_summary_route():
    # Unchanged
    pass # Keep existing logic

# --- UPDATED: ESG Report now uses granular data ---
@app.route('/apillo/esg_report')
def get_esg_report_route():
    try:
        # The Apillo agent now handles the new granular calculations internally
        environmental_impact = apillo_agent.calculate_environmental_impact(transactions)
        social_impact = apillo_agent.calculate_social_impact(environmental_impact)
        corporate_esg = apillo_agent.calculate_corporate_esg_profile(transactions)
        sustainability_insight = apillo_agent.get_sustainability_insights(environmental_impact, social_impact, corporate_esg)

        return jsonify({
            "environmental_impact": environmental_impact,
            "social_impact": social_impact,
            "corporate_esg": corporate_esg,
            "sustainability_insight": sustainability_insight
        })
    except Exception as e:
        print(f"Apillo ESG Error: {e}")
        return jsonify({"error": "Apillo encountered an error generating the ESG report."}), 500

@app.route('/apillo/public_esg_data')
def get_public_esg_data_route():
    try:
        # This endpoint provides the data specifically for the public dashboard
        environmental_impact = apillo_agent.calculate_environmental_impact(transactions)
        social_impact = apillo_agent.calculate_social_impact(environmental_impact)
        sustainability_insight = apillo_agent.get_sustainability_insights(environmental_impact, social_impact)

        return jsonify({
            "environmental_impact": environmental_impact,
            "social_impact": social_impact,
            "sustainability_insight": sustainability_insight
        })
    except Exception as e:
        return jsonify({"error": "Could not generate public ESG data."}), 500

# All other routes remain the same...

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True)

