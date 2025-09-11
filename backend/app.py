from flask import Flask, send_from_directory, request, jsonify
from backend.auth.firebase_auth import verify_user_token
from routes.serve_pdf import serve_pdf_bp
from routes.ai_routes import ai_bp
from routes.admin import admin_bp
import json

app = Flask(__name__)

# Register the blueprints
app.register_blueprint(serve_pdf_bp)
app.register_blueprint(ai_bp)
app.register_blueprint(admin_bp)

@app.route('/')
def home():
    return 'Backend Running'

@app.route('/sms-gateway')
def sms_gateway_page():
    return send_from_directory('../frontend/gui/sms_gateway', 'index.html')

@app.route('/api/inventory/update', methods=['POST'])
def update_inventory():
    # 1. Verify the user is authenticated and approved
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Authorization token is missing or invalid'}), 401

    id_token = auth_header.split('Bearer ')[1]
    user = verify_user_token(id_token)

    if not user:
        return jsonify({'error': 'Invalid token'}), 403

    # Check for custom claims
    if user.get('status') != 'approved':
        return jsonify({'error': 'Account not approved'}), 403

    # 2. Proceed with the original inventory update logic
    data = request.get_json()
    inventory_json_str = data.get('inventory_json', '{}')

    print("Received inventory JSON string:", inventory_json_str)

    try:
        if inventory_json_str.startswith("```json"):
            inventory_json_str = inventory_json_str[7:-3].strip()
        
        inventory_data = json.loads(inventory_json_str)
        
        print("Updating inventory with:", inventory_data)
        for item, quantity in inventory_data.items():
            # In a real application, you would update your database here.
            print(f"Updating {item} to quantity {quantity}")
        
        return jsonify({"status": "success", "message": "Inventory updated"}), 200
    except json.JSONDecodeError as e:
        print("JSON Decode Error:", e)
        return jsonify({"status": "error", "message": "Invalid JSON format from Gemini"}), 400
    except Exception as e:
        print("An error occurred:", e)
        return jsonify({"status": "error", "message": "An internal error occurred"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
