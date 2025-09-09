
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
    # We will add Chart.js and update the ESG panel
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>StarSon POS (AI-Powered)</title>
    <!-- ** NEW: Added Chart.js for data visualization ** -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: sans-serif; margin: 2em; background-color: #f9f9f9; }
        h1, h2, h3 { color: #333; }
        .transaction-panel { background: white; border: 1px solid #ddd; border-radius: 8px; padding: 1.5em; margin-top: 1em; }
        .error-banner { background: #ffdddd; border: 1px solid #ff9999; color: #d8000c; padding: 1em; margin-bottom: 1em; border-radius: 8px; }
        button { padding: 10px 15px; font-size: 14px; cursor: pointer; border-radius: 5px; border: 1px solid #ccc; background-color: #f0f0f0; }
        button:disabled { cursor: not-allowed; background-color: #e0e0e0; }
        #esg-report-panel { background-color: #e6f4ea; border-color: #b2d8b5; }
        /* ** NEW: Styles for chart containers ** */
        .chart-container { width: 80%; max-width: 400px; margin: 1em auto; }
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
    <button onclick="getEsgReport()" id="esg-btn">Build ESG Dashboard</button>
    <button onclick="getCorporateEsgReport()" id="corp-esg-btn">Get Corporate ESG Report</button>

    <div id="apillo-summary-panel" class="transaction-panel" style="display:none; background-color: #f0f8ff;"></div>
    
    <!-- ** NEW: Updated ESG Panel with Canvas elements for charts ** -->
    <div id="esg-report-panel" class="transaction-panel" style="display:none;">
        <h3>Apillo's ESG Dashboard</h3>
        <p id="esg-summary-text"></p>
        <div style="display: flex; justify-content: space-around; align-items: center; flex-wrap: wrap;">
            <div class="chart-container">
                <h4>Environmental Impact</h4>
                <canvas id="environmentalChart"></canvas>
            </div>
            <div class="chart-container">
                <h4>Social Contribution</h4>
                <canvas id="socialChart"></canvas>
            </div>
        </div>
        <p><b>Apillo's Sustainability Insight:</b> <span id="esg-insight-text"></span></p>
    </div>

    <!-- ** NEW: Corporate ESG Panel ** -->
    <div id="corporate-esg-panel" class="transaction-panel" style="display:none; background-color: #e3f2fd;">
        <h3>Apillo's Corporate ESG Profile</h3>
        <div id="corporate-esg-content"></div>
    </div>
    
    <div id="active-transactions"></div>

<script>
    // Keep track of chart instances to destroy them before re-rendering
    let environmentalChartInstance = null;
    let socialChartInstance = null;

    // Unchanged functions: startNewSTKPush, startNewQRTransaction, etc.
    // ...

    async function getDailySummary() {
        // This function is unchanged
        // ...
    }

    async function getEsgReport() {
        const btn = document.getElementById('esg-btn');
        const panel = document.getElementById('esg-report-panel');
        btn.disabled = true;
        btn.innerText = "Building Dashboard...";
        
        try {
            const response = await fetch('/apillo/esg_report');
            const report = await response.json();
            if (!response.ok) throw new Error(report.error || 'Failed to get ESG report.');

            // Update text elements
            document.getElementById('esg-summary-text').innerText = `Based on today's ${report.environmental_impact.digital_receipts} paperless transactions:`;
            document.getElementById('esg-insight-text').innerText = report.sustainability_insight.esg_insight;
            
            // --- ** NEW: Chart Rendering Logic ** ---

            // Destroy previous charts if they exist
            if (environmentalChartInstance) environmentalChartInstance.destroy();
            if (socialChartInstance) socialChartInstance.destroy();

            // 1. Environmental Impact Donut Chart
            const envCtx = document.getElementById('environmentalChart').getContext('2d');
            environmentalChartInstance = new Chart(envCtx, {
                type: 'doughnut',
                data: {
                    labels: ['CO2 Reduction (kg)', 'Water Saved (L)', 'Waste Diverted (kg)'],
                    datasets: [{
                        data: [
                            report.environmental_impact.estimated_carbon_reduction_kg,
                            report.environmental_impact.water_saved_liters,
                            report.environmental_impact.waste_diverted_kg
                        ],
                        backgroundColor: ['#4CAF50', '#2196F3', '#FFC107'],
                    }]
                },
                options: { responsive: true, maintainAspectRatio: true }
            });

            // 2. Social Impact Bar Chart
            const socialCtx = document.getElementById('socialChart').getContext('2d');
            socialChartInstance = new Chart(socialCtx, {
                type: 'bar',
                data: {
                    labels: ['Community Give-Back (KES)'],
                    datasets: [{
                        label: report.social_impact.program_description,
                        data: [report.social_impact.community_give_back_kes],
                        backgroundColor: ['#9C27B0']
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    scales: { y: { beginAtZero: true } },
                    plugins: { legend: { display: false } }
                }
            });

            panel.style.display = 'block';

        } catch (error) {
            document.getElementById('error-banner').innerText = error.message;
            document.getElementById('error-banner').style.display = 'block';
        } finally {
            btn.disabled = false;
            btn.innerText = "Rebuild ESG Dashboard";
        }
    }

    async function getCorporateEsgReport() {
        const btn = document.getElementById('corp-esg-btn');
        const panel = document.getElementById('corporate-esg-panel');
        const contentDiv = document.getElementById('corporate-esg-content');
        btn.disabled = true;
        btn.innerText = "Analyzing...";

        try {
            const response = await fetch('/apillo/corporate_esg_report');
            const report = await response.json();
            if (!response.ok) throw new Error(report.error || 'Failed to get corporate ESG report.');

            let content = '<h4>Supply Chain Transparency</h4>';
            content += `<p>${report.supply_chain_transparency.description}</p>`;
            content += `<p><b>Certified Fair-Trade:</b> ${report.supply_chain_transparency.certified_fair_trade_percentage}%</p>`;

            content += '<hr><h4>Diversity & Inclusion</h4>';
            content += `<p>${report.diversity_and_inclusion.description}</p>`;
            content += `<p><b>Average Ownership Diversity Score:</b> ${report.diversity_and_inclusion.average_ownership_diversity_score} / 10</p>`;

            contentDiv.innerHTML = content;
            panel.style.display = 'block';

        } catch (error) {
            document.getElementById('error-banner').innerText = error.message;
            document.getElementById('error-banner').style.display = 'block';
        } finally {
            btn.disabled = false;
            btn.innerText = "Get Corporate ESG Report";
        }
    }
</script>
</body>
</html>
    ''', saf_api_available=(saf_api is not None))

# --- All Backend Endpoints are unchanged ---

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

@app.route('/confirm_manual_payment', methods=['POST'])
def confirm_manual_route():
    data = request.get_json()
    txn_id = data.get("txn_id")
    if not txn_id or txn_id not in transactions:
        return jsonify({"error": "Transaction not found"}), 404
    
    transactions[txn_id]['status'] = 'completed'
    transactions[txn_id]['details']['confirmation_time'] = datetime.datetime.now().isoformat()
    transactions[txn_id]['details']['confirmed_by'] = 'manual_cashier'

    # --- NEW: Add corporate ESG data to transactions for simulation ---
    transactions[txn_id]['details']['supplier_certified'] = random.choice([True, False])
    transactions[txn_id]['details']['ownership_diversity_score'] = random.randint(1, 10)

    return jsonify({"status": "confirmed", "details": transactions[txn_id]['details']})

@app.route('/apillo/daily_summary')
def get_daily_summary_route():
    try:
        report = apillo_agent.generate_daily_summary(transactions)
        return jsonify(report)
    except Exception as e:
        print(f"Apillo Summary Error: {e}")
        return jsonify({"error": "Apillo encountered an error generating the summary."}), 500

@app.route('/apillo/esg_report')
def get_esg_report_route():
    try:
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

@app.route('/apillo/corporate_esg_report')
def get_corporate_esg_report_route():
    try:
        corporate_esg = apillo_agent.calculate_corporate_esg_profile(transactions)
        return jsonify(corporate_esg)
    except Exception as e:
        print(f"Apillo Corporate ESG Error: {e}")
        return jsonify({"error": "Apillo encountered an error generating the corporate ESG report."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True)
