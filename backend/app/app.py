
import os
import sys
from dotenv import load_dotenv

from flask import Flask, request, jsonify
from routes.admin_routes import admin_routes
from routes.receipt_routes import receipt_routes # Import the receipt blueprint
from routes.migration_routes import migration_bp # Import the migration blueprint

# from api.image_analyzer import analyze_image_for_inventory
from integrations.factory import get_revenue_service
from ai.apillo import Apillo

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.register_blueprint(admin_routes)
app.register_blueprint(receipt_routes) # Register the receipt blueprint
app.register_blueprint(migration_bp) # Register the migration blueprint

# Define a directory to store uploaded images
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

apillo = Apillo()

@app.route("/")
def home():
  return"StarSon POS Backend Running"

# @app.route("/api/analyze_image", methods=['POST'])
# def analyze_image_route():
#     if 'image' not in request.files:
#         return jsonify({"error": "No image file provided"}), 400
#
#     image_file = request.files['image']
#
#     if image_file.filename == '':
#         return jsonify({"error": "No selected file"}), 400
#
#     if image_file:
#         filename = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
#         image_file.save(filename)
#
#         inventory = analyze_image_for_inventory(filename)
#
#         # Clean up the uploaded file
#         os.remove(filename)
#
#         if inventory:
#             return jsonify(inventory)
#         else:
#             return jsonify({"error": "Failed to analyze image"}), 500

@app.route("/api/invoice", methods=['POST'])
def create_invoice_route():
    data = request.get_json()
    provider_name = data.get('provider_name')
    invoice_data = data.get('invoice_data')

    if not provider_name or not invoice_data:
        return jsonify({"error": "Missing provider_name or invoice_data"}), 400

    revenue_service = get_revenue_service(provider_name)

    if not revenue_service:
        return jsonify({"error": f"Revenue service provider '{provider_name}' not found"}), 404

    response = revenue_service.send_invoice(invoice_data)

    return jsonify(response)

@app.route('/api/apillo/insights', methods=['POST'])
def get_apillo_insights():
    transactions_dict = request.json
    if not transactions_dict:
        return jsonify({"error": "No transaction data provided"}), 400

    # Get environmental insights
    environmental_data = apillo.calculate_environmental_impact(transactions_dict)
    
    # Get social insights
    social_data = apillo.calculate_social_impact(environmental_data)

    # Get sustainability insights
    sustainability_insights = apillo.get_sustainability_insights(environmental_data, social_data)

    # Get operational insights
    daily_summary = apillo.generate_daily_summary(transactions_dict)

    return jsonify({
        "sustainability_insights": sustainability_insights,
        "daily_summary": daily_summary
    })

if __name__ == "__main__":
    app.run(debug=True, port=8080)
