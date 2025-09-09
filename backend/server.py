import datetime
import io
import json
import os
import qrcode
import urllib.request
import time

from flask import Flask, request, jsonify, render_template, send_from_directory, session, redirect, url_for, send_file

# Provider Imports
from backend.integrations.daraja import SafaricomAPI
from backend.providers.mpesa import SafaricomMpesaProvider

# Apillo AI Agent Import
from backend.ai.apillo import Apillo
from backend.ai.translator import ApilloTranslator

# Automated Reporting
from backend.reporting import start_reporting_thread

# --- Modular Feature Imports ---
from backend.integrations.miti_pesa import MitiPesaConnector
from backend.ecommerce.shopify_connector import ShopifyConnector
from backend.ecommerce.woocommerce_connector import WooCommerceConnector

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = os.urandom(24)

apillo_agent = Apillo()
apillo_translator = ApilloTranslator()
transactions = {}

# --- Firebase & Subscription Config ---
FIREBASE_FUNCTION_URL = "https://us-central1-your-project-id.cloudfunctions.net/logTransaction"
merchant_subscriptions = {
    'analytics_pro': True,
    'global_reach': True,
    'miti_pesa': False,
    'ecommerce': False
}

# --- Localization (i18n) Setup ---
def get_locale():
    lang = session.get('language')
    if not lang:
        lang = request.accept_languages.best_match(apillo_translator.get_supported_languages().keys())
    if not lang:
        lang = 'en'
    return lang

@app.context_processor
def inject_i18n():
    def _(text_key):
        return apillo_translator.translate(text_key, get_locale())
    
    return dict(
        _=_,
        current_lang=get_locale(),
        supported_languages=apillo_translator.get_supported_languages()
    )

# --- Dormant Module Initialization ---
miti_pesa_connector = None
if merchant_subscriptions.get('miti_pesa'):
    miti_pesa_connector = MitiPesaConnector(api_key="DUMMY_KEY_FOR_NOW")

ecommerce_connector = None
if merchant_subscriptions.get('ecommerce'):
    pass

# --- Authentication & Onboarding ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        with open('users.json', 'r') as f:
            users_data = json.load(f)

        user_info = users_data.get(username)
        is_valid = False
        
        if user_info:
            # New structure: user_info is a dict with a password
            if isinstance(user_info, dict) and user_info.get('password') == password:
                is_valid = True
            # Old structure: user_info is the password string itself (for backward compatibility)
            elif isinstance(user_info, str) and user_info == password:
                is_valid = True

        if is_valid:
            session['logged_in'] = True
            session['username'] = username
            session['language'] = 'en' # Default to English on login

            # If the user profile is incomplete, send to setup wizard
            if isinstance(user_info, dict) and not user_info.get('profile_complete', False):
                return redirect(url_for('setup_wizard'))

            return redirect(url_for('index'))
        else:
            error_msg = apillo_translator.translate('login_error', get_locale())
            return render_template('login.html', error=error_msg)
            
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        business_name = request.form['business_name']
        username = request.form['username'] # This is the email
        password = request.form['password']

        with open('users.json', 'r+') as f:
            users_data = json.load(f)
            if username in users_data:
                error_msg = apillo_translator.translate('username_exists_error', get_locale()) # You will need to add this key
                return render_template('register.html', error=error_msg)

            # Create the new user with the detailed, tiered structure
            users_data[username] = {
                "password": password,
                "business_name": business_name,
                "status": "pending", # Account awaits manual activation
                "subscription_tier": "Basic",
                "subscription_expiry_date": None,
                "profile_complete": False, # Onboarding wizard not completed
                "branches": [],
                "logo_url": None,
                "tax_id": None,
                "receipt_config": {
                    "email_from": None,
                    "sms_provider": None,
                    "sms_api_key": None
                }
            }
            
            f.seek(0)
            json.dump(users_data, f, indent=4)
            f.truncate()

        # Log the new user in and start the onboarding process
        session['logged_in'] = True
        session['username'] = username
        session['language'] = 'en'
        return redirect(url_for('setup_wizard'))

    return render_template('register.html')

@app.route('/setup_wizard')
def setup_wizard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    # This is a placeholder for the multi-step onboarding process
    # In the future, this will render `setup_wizard.html`
    return f"""<h1>Welcome, {session.get('username')}!</h1>
               <p>Your account setup is not yet complete.</p>
               <p>Your account is currently PENDING ACTIVATION by our team.</p>
               <p>(This page will become a multi-step setup wizard)</p>
               <a href="{url_for('index')}">Continue to Dashboard (Limited Access)</a>"""


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/set_language/<lang>')
def set_language(lang):
    if lang in apillo_translator.get_supported_languages():
        session['language'] = lang
    return redirect(request.referrer or url_for('index'))

# --- NEW: QR Code Generation Endpoint ---
@app.route('/generate_qr')
def generate_qr():
    """Generates a QR code image from the provided data parameter."""
    data = request.args.get('data', '')
    if not data:
        # Return a small, blank pixel if no data is provided
        return send_file(io.BytesIO(b'''\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'''), mimetype='image/png')

    img = qrcode.make(data)
    buf = io.BytesIO()
    img.save(buf)
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

# --- Frontend Rendering ---
@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    # Load user data to get business name and status
    merchant_name = "StarSon"
    with open('users.json', 'r') as f:
        users_data = json.load(f)
    
    user_info = users_data.get(session['username'])
    
    # Handle new user structure
    if isinstance(user_info, dict):
        merchant_name = user_info.get('business_name', 'Unnamed Business')
        if not user_info.get('profile_complete', False):
            return redirect(url_for('setup_wizard')) # Force completion of wizard
    
    # Handle legacy admin user
    elif session['username'] == 'admin':
        merchant_name = "Bright Arm Enterprise"

    return render_template('admin_dashboard.html', subs=merchant_subscriptions, merchant_name=merchant_name)


# --- Backend AI & Analytics API Endpoints ---

@app.route("/api/predict_inventory", methods=['POST'])
def api_predict_inventory():
    if not merchant_subscriptions.get('analytics_pro'):
        return jsonify({"error": "Analytics Pro subscription required."}), 403
    data = request.json
    predictions = apillo_agent.get_inventory_predictions(data['sales_data'], data['current_stock'])
    return jsonify(predictions)

@app.route("/api/forecast_sales", methods=['POST'])
def api_forecast_sales():
    if not merchant_subscriptions.get('analytics_pro'):
        return jsonify({"error": "Analytics Pro subscription required."}), 403
    data = request.json
    forecast = apillo_agent.get_sales_forecast(data['sales_data'])
    return jsonify(forecast)

@app.route("/api/segment_customers", methods=['POST'])
def api_segment_customers():
    if not merchant_subscriptions.get('analytics_pro'):
        return jsonify({"error": "Analytics Pro subscription required."}), 403
    data = request.json
    segments = apillo_agent.get_customer_segments(data['customer_data'])
    return jsonify(segments)

# --- Core Transaction & Module Endpoints ---

@app.route('/log_transaction', methods=['POST'])
def log_transaction():
    transaction = request.json
    transaction_id = f"txn_{int(time.time())}"
    transactions[transaction_id] = transaction
    if miti_pesa_connector and miti_pesa_connector.is_active:
        impact = apillo_agent.calculate_environmental_impact({transaction_id: transaction})
        carbon_reduction = impact.get('estimated_carbon_reduction_kg', 0)
        if carbon_reduction > 0:
            miti_pesa_connector.issue_carbon_credits(session['username'], carbon_reduction)
    return jsonify({"status": "success", "transaction_id": transaction_id}), 201

@app.route("/api/miti_pesa/balance")
def get_miti_pesa_balance():
    if not miti_pesa_connector or not miti_pesa_connector.is_active:
        return jsonify({"status": "dormant", "message": "MITI Pesa subscription is not active."}), 403
    balance = miti_pesa_connector.get_credit_balance(session['username'])
    return jsonify(balance)

@app.route("/api/ecommerce/sync", methods=['POST'])
def sync_ecommerce():
    if not ecommerce_connector:
        return jsonify({"status": "dormant", "message": "E-commerce integration is not active."}), 403
    return jsonify({"status": "inactive", "message": "Sync logic not implemented yet."})


# --- Public & Static Routes ---

@app.route('/public/esg_dashboard')
def public_esg_dashboard():
    return render_template('public_dashboard.html', esg_goals={})

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('../static', path)

if __name__ == '__main__':
    start_reporting_thread(apillo_agent, transactions)
    app.run(host='0.0.0.0', port=8080, threaded=True)
