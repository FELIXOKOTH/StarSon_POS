
import datetime
import io
from flask import Flask, request, jsonify, render_template_string, send_file
import os
import qrcode

# Provider Imports
from backend.integrations.daraja import SafaricomAPI
from backend.providers.mpesa import SafaricomMpesaProvider

# --- NEW: Apillo AI Agent Import ---
from backend.ai.apillo import Apillo

app = Flask(__name__)

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


# --- Frontend Rendering ---
@app.route('/')
def index():
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>StarSon POS (AI-Powered)</title>
    <style>
        body { font-family: sans-serif; margin: 2em; background-color: #f9f9f9; }
        h1 { color: #333; }
        .transaction-panel { background: white; border: 1px solid #ddd; border-radius: 8px; padding: 1em; margin-top: 1em; }
        .error-banner { background: #ffdddd; border: 1px solid #ff9999; color: #d8000c; padding: 1em; margin-bottom: 1em; border-radius: 8px; }
        button { padding: 10px 15px; font-size: 14px; cursor: pointer; border-radius: 5px; border: 1px solid #ccc; background-color: #f0f0f0; }
        button:disabled { cursor: not-allowed; background-color: #e0e0e0; }
        #esg-report-panel { background-color: #e6f4ea; border-color: #b2d8b5; }
    </style>
</head>
<body>
    <h1>StarSon POS (AI-Powered)</h1>
    
    <div class="error-banner" id="error-banner" style="display: none;"></div>

    {% if not saf_api_available %}
        <div class="error-banner">WARNING: M-Pesa STK Push is not configured. Limited functionality.</div>
    {% endif %}

    <button onclick="startNewSTKPush()" {% if not saf_api_available %}disabled{% endif %}>New M-Pesa STK Push</button>
    <button onclick="startNewQRTransaction()" {% if not saf_api_available %}disabled{% endif %}>New QR Code Payment</button>
    <button onclick="startNewManual()">Log a Manual Payment</button>
    <button onclick="getDailySummary()" id="summary-btn">Get Apillo's Daily Summary</button>
    <button onclick="getEsgReport()" id="esg-btn">Generate ESG Impact Report</button>

    <div id="apillo-summary-panel" class="transaction-panel" style="display:none; background-color: #f0f8ff;"></div>
    <div id="esg-report-panel" class="transaction-panel" style="display:none;"></div>
    <div id="active-transactions"></div>

<script>
    // Functions for starting transactions are unchanged
    // ...

    async function getDailySummary() {
        const btn = document.getElementById('summary-btn');
        const panel = document.getElementById('apillo-summary-panel');
        btn.disabled = true;
        btn.innerText = "Apillo is analyzing...";
        try {
            const response = await fetch('/apillo/daily_summary');
            const report = await response.json();
            if (!response.ok) throw new Error(report.error || 'Failed to get summary.');

            panel.innerHTML = `<h3>${report.summary_title}</h3>
                               <p><b>${report.key_metric}</b></p>
                               <p><b>Actionable Insight:</b> ${report.actionable_insight}</p>`;
            panel.style.display = 'block';

        } catch (error) {
            document.getElementById('error-banner').innerText = error.message;
            document.getElementById('error-banner').style.display = 'block';
        } finally {
            btn.disabled = false;
            btn.innerText = "Get Apillo's Daily Summary";
        }
    }

    async function getEsgReport() {
        const btn = document.getElementById('esg-btn');
        const panel = document.getElementById('esg-report-panel');
        btn.disabled = true;
        btn.innerText = "Calculating Impact...";
        try {
            const response = await fetch('/apillo/esg_report');
            const report = await response.json();
            if (!response.ok) throw new Error(report.error || 'Failed to get ESG report.');

            panel.innerHTML = `<h3>Apillo's ESG Impact Report</h3>
                               <p>Based on today's transactions:</p>
                               <ul>
                                   <li><b>Digital Receipts Issued:</b> ${report.environmental_impact.digital_receipts}</li>
                                   <li><b>Estimated Trees Saved:</b> ${report.environmental_impact.trees_saved_estimate}</li>
                                   <li><b>Estimated Carbon Reduction:</b> ${report.environmental_impact.estimated_carbon_reduction_kg} kg CO2e</li>
                               </ul>
                               <p><b>Sustainability Insight:</b> ${report.sustainability_insight.esg_insight}</p>`;
            panel.style.display = 'block';

        } catch (error) {
            document.getElementById('error-banner').innerText = error.message;
            document.getElementById('error-banner').style.display = 'block';
        } finally {
            btn.disabled = false;
            btn.innerText = "Generate ESG Impact Report";
        }
    }
</script>
</body>
</html>
    ''', saf_api_available=(saf_api is not None))

# --- Payment Endpoints ---

# This endpoint remains the same
@app.route('/initiate_payment', methods=['POST'])
def initiate_payment_route():
    data = request.get_json()
    provider = data.get("provider")

    if provider in PAYMENT_PROVIDERS:
        # Code for M-Pesa STK push is unchanged
        pass
    elif provider == 'manual':
        txn_id = data.get("txn_id")
        transactions[txn_id] = {
            "status": "pending", 
            "provider": "manual", 
            "amount": data.get('amount'),
            "details": {"method": data.get("method", "unknown")}
        }
        return jsonify({"message": "Manual transaction logged"})
    
    return jsonify({"error": "Invalid provider"}), 400

# All other payment endpoints (QR, callback, confirmation) are unchanged
@app.route('/confirm_manual_payment', methods=['POST'])
def confirm_manual_route():
    data = request.get_json()
    txn_id = data.get("txn_id")
    if not txn_id or txn_id not in transactions:
        return jsonify({"error": "Transaction not found"}), 404
    
    transactions[txn_id]['status'] = 'completed'
    transactions[txn_id]['details']['confirmation_time'] = datetime.datetime.now().isoformat()
    transactions[txn_id]['details']['confirmed_by'] = 'manual_cashier'

    return jsonify({"status": "confirmed", "details": transactions[txn_id]['details']})

# --- Apillo AI Agent Endpoints ---

@app.route('/apillo/daily_summary')
def get_daily_summary_route():
    try:
        # Use the Apillo class method
        report = apillo_agent.generate_daily_summary(transactions)
        return jsonify(report)
    except Exception as e:
        print(f"Apillo Summary Error: {e}")
        return jsonify({"error": "Apillo encountered an error generating the summary."}), 500

@app.route('/apillo/esg_report')
def get_esg_report_route():
    """
    This endpoint demonstrates Apillo's independent ESG capability.
    An external system could call this with its own transaction data.
    """
    try:
        # 1. Calculate the core environmental metrics
        environmental_impact = apillo_agent.calculate_environmental_impact(transactions)
        
        # 2. Get an intelligent insight based on those metrics
        sustainability_insight = apillo_agent.get_sustainability_insights(environmental_impact)

        return jsonify({
            "environmental_impact": environmental_impact,
            "sustainability_insight": sustainability_insight
        })
    except Exception as e:
        print(f"Apillo ESG Error: {e}")
        return jsonify({"error": "Apillo encountered an error generating the ESG report."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True)
