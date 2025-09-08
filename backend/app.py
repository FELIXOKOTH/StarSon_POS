from flask import Flask, send_from_directory, request, jsonify
from routes.serve_pdf import serve_pdf_bp
import json

app = Flask(__name__)
app.register_blueprint(serve_pdf_bp)

@app.route('/')
def home():
    return 'Backend Running'

@app.route('/sms-gateway')
def sms_gateway_page():
    return send_from_directory('../frontend/gui/sms_gateway', 'index.html')

@app.route('/api/inventory/update', methods=['POST'])
def update_inventory():
    data = request.get_json()
    inventory_json_str = data.get('inventory_json', '{}')

    print("Received inventory JSON string:", inventory_json_str)

    try:
        # The string from Gemini might be a simple string, not a JSON object yet.
        # We need to parse it.
        # It might also have markdown characters like ```json ... ``` that need to be removed.
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
